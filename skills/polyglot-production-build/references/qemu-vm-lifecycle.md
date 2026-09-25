---
name: qemu-vm-lifecycle
description: "Verify QEMU VM lifecycle: start, metrics streaming, stop — via server endpoints. Includes WHPX CPU model, display backend, and guest agent chardev fixes."
version: 1.0.0
author: VM-Harness
license: MIT
---

## When to Use

Use this reference after any QEMU/VM-related code change (patches to `gui/multi_vm.py`, `headless_server.py`, or VM config) when you need to verify that QEMU actually starts and runs, not just that the server reports it started.

## 1. Patch Verification

Check the three known patches are in effect in `gui/multi_vm.py`:

```python
import sys
sys.path.insert(0, 'C:/Projects/QEMU-MCP')
from gui.multi_vm import MultiVMManager
import inspect
src = inspect.getsource(MultiVMManager._build_qemu_args)

# Check 1: CPU model
assert '"-cpu", "qemu64"' in src, "CPU patch: still using host CPU (needs qemu64 for WHPX)"

# Check 2: Guest agent removed
assert 'Guest agent removed' in src, "Guest agent chardev still present (causes named-pipe bind failures)"

# Check 3: Display handling (config-driven, verify config)
m = MultiVMManager()
c = m.get_vm('<vm-name>')
assert c.display == 'none', f"VM display={c.display} — should be 'none' for headless QMP mode"
```

## 2. Full Lifecycle Test via Server

```python
import urllib.request, json, time, subprocess, socket

BASE = "http://127.0.0.1:8444"
VM = "test-vm"

# Start
req = urllib.request.Request(f"{BASE}/api/v1/vms/{VM}/start", method="POST")
with urllib.request.urlopen(req, timeout=15) as resp:
    start_result = json.loads(resp.read().decode())
    assert start_result["status"] == "ok", f"Start failed: {start_result}"
    pid = int(start_result["detail"].split("PID: ")[-1].strip(")"))

# Wait for QEMU to initialize
time.sleep(5)

# Verify QEMU process
result = subprocess.run([
    'tasklist', '/FI', 'IMAGENAME eq qemu-system-x86_64.exe',
    '/FO', 'CSV', '/NH'
], capture_output=True, text=True, timeout=5)
qemu_lines = [l for l in result.stdout.strip().split('\n')
              if 'qemu' in l.lower() and 'qemu-system' in l]
assert qemu_lines, "QEMU process not found after start"
print(f"QEMU running: {qemu_lines[0].strip()}")

# Verify QMP port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
r = sock.connect_ex(('127.0.0.1', 4445))
sock.close()
assert r == 0, f"QMP port 4445 not listening (error: {r})"
print("QMP port 4445: LISTENING")

# Verify metrics streaming
req = urllib.request.Request(
    f"{BASE}/v1/proto",
    data=json.dumps({"type": "vm_metrics", "vm_name": VM}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=5) as resp:
    metrics = json.loads(resp.read().decode())
    assert metrics["status"] == "ok"
    vm_data = metrics["metrics"]
    print(f"Metrics: cpu={vm_data['cpu_percent']}%, "
          f"mem={vm_data['memory_used_mb']}/{vm_data['memory_total_mb']}MB, "
          f"uptime={vm_data['uptime_seconds']}s")

# Stop
req = urllib.request.Request(f"{BASE}/api/v1/vms/{VM}/stop", method="POST")
with urllib.request.urlopen(req, timeout=15) as resp:
    stop_result = json.loads(resp.read().decode())
    assert stop_result["status"] == "ok"

time.sleep(2)

# Final: QEMU stopped
result = subprocess.run([
    'tasklist', '/FI', 'IMAGENAME eq qemu-system-x86_64.exe',
    '/FO', 'CSV', '/NH'
], capture_output=True, text=True, timeout=5)
qemu_after = [l for l in result.stdout.strip().split('\n')
             if 'qemu' in l.lower() and 'qemu-system' in l]
assert not qemu_after, "QEMU still running after stop"
print("VM lifecycle: PASS (start → metrics → stop)")
```

## 3. Direct QEMU Args Test (when server says started but QEMU isn't running)

```python
import subprocess, time, sys
sys.path.insert(0, 'C:/Projects/QEMU-MCP')
from gui.multi_vm import MultiVMManager

manager = MultiVMManager()
config = manager.get_vm('<vm-name>')
args = manager._build_qemu_args(config)

proc = subprocess.Popen(
    args,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    creationflags=0x08000000  # CREATE_NO_WINDOW
)
print(f"QEMU PID: {proc.pid}")
time.sleep(4)

poll = proc.poll()
if poll is None:
    print("QEMU RUNNING — args are valid")
    # Check QMP
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    r = sock.connect_ex(('127.0.0.1', config.qmp_port))
    sock.close()
    print(f"QMP port {config.qmp_port}: {'LISTENING' if r == 0 else 'NOT LISTENING'}")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except:
        proc.kill()
else:
    output, _ = proc.communicate(timeout=3)
    print(f"QEMU EXIT {poll}")
    print(f"ERROR: {output[:500]}")
    # Common errors and fixes:
    # "invalid accelerator kvm" → remove -enable-kvm, use -accel whpx or tcg
    # "CPU model 'host' requires KVM" → use -cpu qemu64
    # "Parameter 'type' does not accept value 'spice'" → use 'spice-app' or 'none'
    # "Failed to bind socket to //./pipe/qga-*" → remove guest agent chardev
    # "Could not open '*.fd'" → check EFI flash file paths
```

## 4. All VM Lifecycle Endpoints

```python
import urllib.request, json

BASE = "http://127.0.0.1:8444"
VM = "<vm-name>"

for action in ["start", "stop", "reset", "pause", "resume", "powerdown"]:
    try:
        req = urllib.request.Request(
            f"{BASE}/api/v1/vms/{VM}/{action}", method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            print(f"{action:12s}: {result['status']:5s} | {result.get('detail', '')[:80]}")
    except Exception as e:
        print(f"{action:12s}: ERROR — {e}")
```

## 5. EFI Flash Files (Windows)

QEMU on Windows needs EFI flash files for UEFI boot. If QEMU fails with "Could not open '*.fd'":

```bash
# Use search_files (target='files') to find EFI files in QEMU share
# Required for x86_64 UEFI:
# - edk2-x86_64-code.fd (exists in QEMU share)
# - edk2-x86_64-vars.fd (may NOT exist — use edk2-x86_64-secure-code.fd as fallback)
```

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Server says "started" but no QEMU process | Bad QEMU args (CPU, display, chardev) | Test args directly with Popen, read stderr |
| QEMU exits with "invalid accelerator kvm" | KVM not available, `-enable-kvm` or `-cpu host` used | Use `-accel whpx` (Windows) or `-accel tcg`, `-cpu qemu64` |
| QEMU exits with "CPU model 'host' requires KVM" | `-cpu host` without KVM | Use `-cpu qemu64` |
| QEMU exits with "Parameter 'type' does not accept value 'spice'" | QEMU build doesn't support `spice` display type | Use `spice-app`, `none`, `gtk`, or check `-display help` |
| QEMU exits with "Failed to bind socket to //./pipe/qga-*" | Named pipe guest agent chardev conflict | Remove guest agent chardev/device lines |
| QEMU exits with "Could not open '*.fd'" | Missing EFI flash files | Copy from QEMU share to writable location |
| QMP port not listening after start | QEMU exited before QMP initialized | Check QEMU stderr for the real error |
| `start_vm` returns ok but metrics show uptime=0 | QEMU not actually running, server has stale PID | Kill stale process, restart with verified args |
