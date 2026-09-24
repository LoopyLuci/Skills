# Hardware Abstraction Layer (HAL)

This reference covers building a multi-threading + multi-GPU hardware abstraction layer for PyQt5 desktop apps.

## Architecture

```
webbuilder/hardware/
├── __init__.py          # Re-exports + global instances
├── detector.py          # HardwareDetector — CPU/GPU/memory detection
├── gpu.py               # GPUManager — device assignment, load tracking
├── scheduler.py         # TaskScheduler — distribute work across threads + GPUs
├── pool.py              # ComputePool — dynamic worker scaling
└── workstealing.py      # WorkStealingQueue — optimal load balancing
```

## Hardware Detection

```python
@dataclass
class CPUInfo:
    cores_physical: int
    cores_logical: int
    is_big_lITTLE: bool      # Apple Silicon, Intel 12th+ gen
    big_cores: int
    little_cores: int
    supports_avx512: bool
    
    @property
    def optimal_thread_count(self) -> int:
        if self.is_big_lITTLE:
            return self.big_cores * 2 + self.little_cores
        return self.cores_logical

@dataclass
class GPUInfo:
    index: int
    name: str
    vendor: str              # NVIDIA, AMD, Intel, Apple
    vram_total_mb: int
    supports_cuda: bool
    supports_rocm: bool
    supports_opencl: bool
    supports_metal: bool
    compute_capability: tuple[int, int]
    temperature_c: int
    power_draw_watts: int
    
    @property
    def compute_score(self) -> float:
        # Relative compute capability score
        ...

class HardwareDetector:
    def detect(self) -> HardwareInfo:
        # 1. NVIDIA via pynvml (NVML) → fallback to nvidia-smi subprocess
        # 2. AMD via rocm-smi subprocess
        # 3. Intel via platform detection
        # 4. Apple Silicon via platform.system() == 'Darwin' and platform.machine() == 'arm64'
        # 5. Memory via psutil
        # 6. Power via psutil.sensors_battery()
```

## Task Scheduler

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class TaskScheduler:
    def __init__(self):
        info = get_hardware_info()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=info.cpu.optimal_thread_count,
            thread_name_prefix="wb_worker"
        )
        self._process_pool = ProcessPoolExecutor(
            max_workers=max(1, info.cpu.cores_physical - 1)
        )
    
    def submit(self, callback, use_gpu=False, **kwargs) -> Future:
        if use_gpu and gpu_manager.has_gpu:
            return self._thread_pool.submit(self._execute_gpu_task, ...)
        return self._thread_pool.submit(self._execute_cpu_task, ...)
    
    def submit_cpu_bound(self, callback, *args) -> Future:
        # CPU-bound isolated tasks → process pool
        return self._process_pool.submit(callback, *args)
```

## Work-Stealing Queue

```python
class WorkStealingQueue:
    def __init__(self):
        self._queues: dict[int, deque[WorkItem]] = {}  # per-worker local queues
        self._global_queue: queue.PriorityQueue = ...   # overflow
    
    def new_queue(self) -> int:
        # Register worker, return queue ID
    
    def submit(self, item: WorkItem, queue_id: Optional[int] = None):
        # Submit to specific queue or global
    
    def pop(self, queue_id: int) -> Optional[WorkItem]:
        # 1. Try local queue
        # 2. Try steal from other workers' queues (from the end)
        # 3. Try global queue
        # 4. Return None if all empty
```

## Compute Pool

```python
class ComputePool:
    def __init__(self, min_workers=2, max_workers=None):
        info = get_hardware_info()
        self._max_workers = max_workers or info.cpu.cores_logical
        # Start with min_workers, scale up when queue backs up
    
    def submit(self, callback, args=(), kwargs=None, timeout=60.0) -> str:
        # Submit work, auto-scale workers if needed
    
    def submit_and_wait(self, callback, args=(), timeout=60.0) -> Any:
        # Submit and block until done (for synchronous callers)
```

## PyQt5 Integration

```python
# In WebBuilderWindow.__init__()
from webbuilder.hardware import get_hardware
self._hardware_info = get_hardware()

# In setup_menu()
hardware_action = QAction("Hardware Info...", self)
hardware_action.triggered.connect(self._open_hardware_info)
help_menu.addAction(hardware_action)

# Handler
def _open_hardware_info(self):
    from webbuilder.gui.hardware_dialog import HardwareInfoDialog
    dialog = HardwareInfoDialog(self)
    dialog.exec_()
```

## Hardware Info Dialog

```python
class HardwareInfoDialog(QDialog):
    # Tab 1: System overview (OS, hostname, battery)
    # Tab 2: CPU info (cores, threads, AVX, architecture)
    # Tab 3: GPU table (name, VRAM, compute capabilities, load %)
    # Tab 4: Memory (total, available, swap)
    
    def _populate_info(self):
        info = get_hardware_info()
        gm = get_gpu_manager()
        # Fill tables with detected hardware
```

## Pitfalls

1. **Process pool isolation** — ProcessPoolExecutor workers are separate processes. They CANNOT access module-level singletons from the main app. Pass all data explicitly as function arguments.

2. **GPU detection order** — Always try NVML first (most detailed), then fall back to nvidia-smi subprocess. NVML provides temperature, power draw, fan speed; nvidia-smi provides basic info.

3. **big.LITTLE detection** — Apple Silicon and Intel 12th+ gen have asymmetric cores. Use `big_cores * 2 + little_cores` for optimal thread count (P-cores have hyperthreading, E-cores don't).

4. **Thread pool sizing** — Don't use `os.cpu_count()` directly. For I/O-bound tasks, use `cpu_count * 2`. For CPU-bound tasks, use `cpu_count`. For mixed, use `cpu_count + 1`.

5. **Work-stealing overhead** — Work-stealing has overhead for small task counts. Only use when task count > 100 or task duration varies significantly.

6. **GPU memory tracking** — VRAM reported by NVML is total physical VRAM. Usable VRAM is ~90% (leave headroom for driver). Don't allocate models larger than `vram_free_mb * 0.9`.

7. **Temperature throttling** — Check GPU temperature before assigning workloads. If > 85°C, reduce load or pause until cooled.

8. **Battery awareness** — On battery power, reduce thread count by 50% and avoid GPU-intensive tasks to preserve battery life.

## Testing Hardware Layer

```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from webbuilder.hardware import get_hardware_info, get_scheduler, get_gpu_manager

info = get_hardware_info()
assert info.cpu.cores_logical > 0
assert info.memory.total_gb > 0

scheduler = get_scheduler()
assert scheduler.thread_count > 0

gm = get_gpu_manager()
assert gm.gpu_count >= 0  # 0 is valid (CPU-only)

# Test work submission
from webbuilder.hardware.workstealing import submit_work
item = submit_work(lambda: 42)
import time
time.sleep(0.5)
assert item.result == 42
```

## Performance Guidelines

| Task Type | Pool | Workers | Notes
|-----------|------|---------|-------
| AI inference | Thread | cpu_count | GPU if available
| File I/O | Thread | cpu_count * 2 | I/O bound
| Image processing | Process | cpu_count | CPU bound
| Export generation | Process | cpu_count | CPU bound
| Model fetching | Thread | 4-8 | Network bound
| Canvas rendering | Thread | 2-4 | GUI-bound