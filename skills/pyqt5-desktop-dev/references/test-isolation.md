# Test Isolation for Integration Tests

## When to Use

Use when writing integration tests that create external resources (Kubernetes pods, Docker containers, VMs) and need to be idempotent — running the same test multiple times should always succeed.

## The Problem

Integration tests that create resources (pods, containers, VMs) often fail on re-run because the previous resource hasn't been fully deleted. The test creates a resource with a fixed name, deletes it at the end, but the next run starts before the deletion completes.

## Solution: Polling + Retry + Unique Names

### 1. Unique Resource Names

Use timestamp + UUID to ensure each test run uses a unique resource name:

```python
import uuid
from datetime import datetime

def _generate_pod_name() -> str:
    """Generate a unique pod name with timestamp + UUID."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    return f"vmharness-test-pod-{timestamp}-{unique_id}"
```

### 2. Wait for Deletion

Poll until the resource is gone, with a timeout:

```python
def _wait_for_pod_deleted(self, pod_name: str, timeout: int = 120, interval: int = 5) -> bool:
    """Wait until a pod is fully deleted. Returns True if deleted, False if timeout."""
    import time
    start = time.time()
    while time.time() - start < timeout:
        pods = self.backend.list_pods()
        names = [p.get("name", "") if isinstance(p, dict) else getattr(p, "name", "") for p in pods]
        if pod_name not in names:
            return True
        time.sleep(interval)
    return False
```

### 3. Delete with Retry

Retry the deletion with backoff:

```python
def _delete_pod_with_retry(self, pod_name: str, max_retries: int = 3) -> bool:
    """Delete a pod with retry logic. Returns True if deleted."""
    import time
    for attempt in range(max_retries):
        try:
            self.backend.delete_resource("pod", pod_name)
            if self._wait_for_pod_deleted(pod_name):
                return True
        except Exception:
            pass
        time.sleep(5)
    return False
```

### 4. Clean Up Before Test

Always clean up any leftover resource from a previous run:

```python
def test_04_pod_lifecycle(self):
    pod_name = _generate_pod_name()
    
    # Clean up any leftover pod from a previous run
    self._delete_pod_with_retry(pod_name)
    
    # Create pod
    self.backend.create_pod(pod_name, ...)
    
    # ... test logic ...
    
    # Clean up
    self._delete_pod_with_retry(pod_name)
    self.assertTrue(
        self._wait_for_pod_deleted(pod_name),
        f"Pod {pod_name} still exists after deletion"
    )
```

## Pitfalls

1. **Fixed resource names cause collisions** — If two test runs use the same name, the second run fails because the first pod is still terminating. Always use unique names.

2. **Fixed sleep is unreliable** — `sleep(30)` may not be enough for slow APIs (Kubernetes pod deletion can take 60s+). Poll instead.

3. **Test isolation requires cleanup at start AND end** — Clean up before the test (remove leftovers from previous runs) AND after the test (clean up for the next run).

4. **Async deletion returns immediately** — `delete_resource()` returns before the resource is actually gone. The resource may still appear in `list_pods()` for several seconds after deletion.

5. **Timeout must be generous** — Kubernetes pod deletion can take 60-120s. Set timeout to 120s with 5s polling interval.

6. **Assert deletion, don't assume it** — After calling `delete_resource()`, assert that the resource is actually gone with `self.assertTrue(self._wait_for_pod_deleted(name))`. Don't assume deletion succeeded.
