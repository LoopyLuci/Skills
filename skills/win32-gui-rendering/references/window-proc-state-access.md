# Window Proc State Access Pattern

Window procs in Win32 are `unsafe extern "system" fn` — they have no `self`. All state must be accessed through `GWLP_USERDATA`.

## The Pattern

```rust
// In WM_CREATE: store the state pointer
let state = (*lpcs).lpCreateParams as *mut AppState;
SetWindowLongPtrW(hwnd, GWLP_USERDATA, state as isize);

// In every other message handler: retrieve and use it
unsafe extern "system" fn window_proc(
    hwnd: HWND, msg: u32, wparam: usize, lparam: isize,
) -> isize {
    match msg {
        WM_LBUTTONDOWN => {
            let state_ptr = GetWindowLongPtrW(hwnd, GWLP_USERDATA) as *mut AppState;
            if state_ptr.is_null() { return 0; }
            let state = &mut *state_ptr;
            state.handle_click(lparam);
            0
        }
        _ => DefWindowProcW(hwnd, msg, wparam, lparam),
    }
}
```

## Rules

1. **Null-check the pointer.** `GetWindowLongPtrW` returns 0 before `WM_CREATE` completes or if the window was created without `lpCreateParams`. Always null-check before dereferencing.

2. **Use `&mut *ptr` not `*ptr.field`.** `*ptr.field` tries to move out of a dereference, which Rust rejects for non-Copy types. Use `(*ptr).field` for field access or `&mut *ptr` for method calls.

3. **Mutating state requires `&mut`.** If the handler needs to write, cast as `*mut AppState` and use `&mut *state_ptr`. If it only reads, `*state_ptr` is sufficient.

4. **The pointer is valid for the window's lifetime.** `WM_CREATE` stores it, `WM_DESTROY` should clean it up. Never store a pointer to a stack local — it will dangle after the create function returns.

## Common Compile Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `cannot find value self` | Using `self` in a window proc | Use `GetWindowLongPtrW` pattern |
| `cannot move out of dereference` | `*ptr.field` on non-Copy type | Use `(*ptr).field` |
| `cannot borrow as mutable` | `*ptr` used for mutation | Cast as `*mut T`, use `&mut *ptr` |
| `lifetime does not live long enough` | Storing stack local pointer | Allocate on Box, store raw pointer |
