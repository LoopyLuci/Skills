---
name: operating-system-concepts
description: "Use when implementing OS-level primitives and concepts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [operating-system, processes, memory, scheduler, IPC, syscalls]
    related_skills: [concurrency-parallelism, performance-optimization, compiler-interpreter-basics, distributed-systems-patterns]
---

# Operating System Concepts

Implementing and understanding OS-level concepts — processes, threads, memory management, scheduling, file systems, and inter-process communication in Python and Rust.

## When to Use

- Building system-level software that interacts with the OS directly
- Understanding process/thread lifecycle and synchronization
- Implementing custom schedulers, memory allocators, or IPC
- Debugging performance issues related to OS primitives
- Writing efficient concurrent or parallel code

## Process Management

### Fork and Exec

```python
import os
import signal
import sys

class ProcessManager:
    """Process creation and management patterns."""
    
    @staticmethod
    def spawn_worker(task_fn, *args):
        """Spawn a child process to run a task."""
        pid = os.fork()
        
        if pid == 0:
            # Child process
            try:
                result = task_fn(*args)
                os._exit(0 if result else 1)
            except Exception as e:
                print(f"Child error: {e}", file=sys.stderr)
                os._exit(1)
        else:
            # Parent process
            return pid
    
    @staticmethod
    def wait_for_children(timeout=None):
        """Wait for all child processes to complete."""
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    if timeout:
                        break
                    continue
                if os.WIFEXITED(status):
                    print(f"Process {pid} exited with code {os.WEXITSTATUS(status)}")
            except ChildProcessError:
                break
    
    @staticmethod
    def create_daemon():
        """Create a daemon process (double-fork pattern)."""
        pid = os.fork()
        if pid > 0:
            # First parent exits
            sys.exit(0)
        
        # Detach from terminal
        os.setsid()
        os.umask(0)
        
        # Second fork to prevent acquiring terminal
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        
        # Close file descriptors
        for fd in range(3):
            try:
                os.close(fd)
            except OSError:
                pass
        
        # Redirect stdin/stdout/stderr to /dev/null
        os.open('/dev/null', os.O_RDWR)  # stdin
        os.dup2(0, 1)  # stdout
        os.dup2(0, 2)  # stderr
```

## Thread Synchronization

### Mutex and Condition Variables (Rust)

```rust
use std::sync::{Arc, Mutex, Condvar};
use std::thread;

struct SharedQueue {
    items: Vec<i32>,
    max_size: usize,
}

fn bounded_queue_example() {
    let pair = Arc::new((Mutex::new(SharedQueue {
        items: Vec::new(),
        max_size: 10,
    }), Condvar::new()));
    let pair_clone = Arc::clone(&pair);
    
    // Producer
    thread::spawn(move || {
        let (lock, cvar) = &*pair_clone;
        for i in 0..100 {
            let mut queue = lock.lock().unwrap();
            while queue.items.len() >= queue.max_size {
                queue = cvar.wait(queue).unwrap();
            }
            queue.items.push(i);
            cvar.notify_all();
        }
    });
    
    // Consumer
    let (lock, cvar) = &*pair;
    for _ in 0..100 {
        let mut queue = lock.lock().unwrap();
        while queue.items.is_empty() {
            queue = cvar.wait(queue).unwrap();
        }
        let item = queue.items.remove(0);
        println!("Consumed: {}", item);
        cvar.notify_all();
    }
}
```

### Thread Pool (Python)

```python
from concurrent.futures import ThreadPoolExecutor
import threading
import queue

class CustomThreadPool:
    """Custom thread pool with work stealing."""
    
    def __init__(self, num_workers=None):
        self.num_workers = num_workers or os.cpu_count()
        self.tasks = queue.Queue()
        self.workers = []
        self._running = True
        
        for _ in range(self.num_workers):
            t = threading.Thread(target=self._worker_loop)
            t.daemon = True
            t.start()
            self.workers.append(t)
    
    def submit(self, fn, *args, **kwargs):
        """Submit a task to the pool."""
        result = queue.Queue()
        self.tasks.put((fn, args, kwargs, result))
        return result
    
    def _worker_loop(self):
        """Worker thread: pull tasks from queue and execute."""
        while self._running:
            try:
                fn, args, kwargs, result = self.tasks.get(timeout=1)
                try:
                    r = fn(*args, **kwargs)
                    result.put(r)
                except Exception as e:
                    result.put(e)
            except queue.Empty:
                continue
    
    def shutdown(self):
        self._running = False
        for w in self.workers:
            w.join(timeout=1)
```

## Memory Management

### Arena Allocator (Rust)

```rust
struct Arena {
    buffer: Vec<u8>,
    offset: usize,
}

impl Arena {
    fn new(capacity: usize) -> Self {
        Arena {
            buffer: vec![0; capacity],
            offset: 0,
        }
    }
    
    fn alloc<T>(&mut self, value: T) -> &mut T {
        let size = std::mem::size_of::<T>();
        let align = std::mem::align_of::<T>();
        
        // Align offset
        let aligned_offset = (self.offset + align - 1) & !(align - 1);
        
        assert!(aligned_offset + size <= self.buffer.len(), "Arena full");
        
        let ptr = &mut self.buffer[aligned_offset] as *mut u8 as *mut T;
        self.offset = aligned_offset + size;
        
        unsafe {
            ptr.write(value);
            &mut *ptr
        }
    }
}
```

## IPC (Inter-Process Communication)

### Unix Domain Sockets

```python
import socket
import os
import struct

class IPCHandler:
    """IPC using Unix domain sockets (fastest local IPC)."""
    
    SOCKET_PATH = '/tmp/myapp.sock'
    
    @staticmethod
    def start_server():
        """Start IPC server."""
        if os.path.exists(IPCHandler.SOCKET_PATH):
            os.unlink(IPCHandler.SOCKET_PATH)
        
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(IPCHandler.SOCKET_PATH)
        server.listen(5)
        
        while True:
            conn, addr = server.accept()
            data = conn.recv(4096)
            response = IPCHandler._handle_message(data)
            conn.send(response)
            conn.close()
    
    @staticmethod
    def send_message(data: bytes) -> bytes:
        """Send IPC message to server."""
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(IPCHandler.SOCKET_PATH)
        client.send(data)
        response = client.recv(4096)
        client.close()
        return response
```

### Shared Memory (Python)

```python
import mmap
import struct
import os

class SharedMemoryRingBuffer:
    """Lock-free ring buffer in shared memory."""
    
    def __init__(self, name, size=4096):
        self.size = size
        self.mmap = mmap.mmap(-1, size, tagname=name)
    
    def write(self, data: bytes):
        """Write to ring buffer (single producer)."""
        head = struct.unpack('I', self.mmap[:4])[0]
        data_len = len(data)
        total_size = 4 + data_len + 4  # header + data + footer
        
        # Write header (length)
        self.mmap[head:head+4] = struct.pack('I', data_len)
        # Write data
        self.mmap[head+4:head+4+data_len] = data
        # Write footer (for consumer validation)
        self.mmap[head+4+data_len:head+8+data_len] = struct.pack('I', data_len)
        
        # Update head
        new_head = (head + total_size) % self.size
        self.mmap[:4] = struct.pack('I', new_head)
    
    def read(self) -> bytes:
        """Read from ring buffer (single consumer)."""
        tail = struct.unpack('I', self.mmap[4:8])[0]
        
        data_len = struct.unpack('I', self.mmap[tail:tail+4])[0]
        if data_len == 0:
            return None
        
        data = self.mmap[tail+4:tail+4+data_len]
        
        # Update tail
        new_tail = (tail + 4 + data_len + 4) % self.size
        self.mmap[4:8] = struct.pack('I', new_tail)
        
        return bytes(data)
```

## Common Pitfalls

1. **Zombie processes** — children aren't waited on; use `waitpid()` or double-fork for daemons
2. **Race conditions** — unsynchronized shared state; always use locks, atomics, or channels
3. **Deadlock** — locks acquired in different orders; enforce a lock ordering
4. **Priority inversion** — low-priority task holds a lock needed by high-priority; use priority inheritance
5. **False sharing** — multiple threads writing to adjacent memory locations; pad cache lines
6. **mmap size limitations** — 32-bit processes can't mmap >4GB; use 64-bit or file-based IPC

## Verification Checklist

- [ ] Processes/threads clean up resources (no leaks of fds, memory, or PIDs)
- [ ] Synchronization primitives prevent races (prove with thread sanitizer)
- [ ] IPC works correctly across processes (test with crash recovery)
- [ ] Memory allocation is bounded (no unbounded growth)
- [ ] Signal handlers are reentrant (safe inside signal context)
- [ ] No busy-waiting (use condition variables or blocking I/O)

## See Also

- concurrency-parallelism — concurrent programming patterns
- performance-optimization — profiling OS-level performance
- distributed-systems-patterns — distributed IPC patterns
