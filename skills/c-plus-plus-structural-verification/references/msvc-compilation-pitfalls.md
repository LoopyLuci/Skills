# MSVC Compilation Pitfalls — Reference

## Error Catalog (C++20 / MSVC 19.44 / Vulkan 1.4)

### C2672: 'std::construct_at': no matching overloaded function found
- **Cause**: `std::vector` or `std::unique_ptr` trying to copy-construct a non-copyable type (e.g., containing `std::atomic`)
- **Root cause chain**: `std::atomic<bool>` → deleted copy ctor → `MipResidencyState` non-copyable → `std::vector<MipResidencyState>` fails on resize because `std::construct_at` needs copy or move
- **Fix**: Replace `std::vector<NonCopyableType>` with `std::unique_ptr<NonCopyableType[]>`. Add explicit move ctor and delete copy ctor on the element type.
- **Full fix pattern**:
  ```cpp
  struct MipResidencyState {
      MipResidencyState() = default;
      MipResidencyState(MipResidencyState&&) = default;
      MipResidencyState& operator=(MipResidencyState&&) = default;
      MipResidencyState(const MipResidencyState&) = delete;
      MipResidencyState& operator=(const MipResidencyState&) = delete;
      std::atomic<bool> is_resident{false};
      std::atomic<uint64_t> dma_fence_id{0};
  };
  // In parent struct:
  std::unique_ptr<MipResidencyState[]> residency;
  // Allocation:
  residency = std::make_unique<MipResidencyState[]>(mip_count);
  ```

### C2220: warning treated as error
- **Cause**: `/WX` flag in CMakeLists.txt
- **Fix**: Remove `/WX` during initial development, or suppress specific warnings with `/w4NNNN`

### C2065: undeclared identifier
- **Cause**: Missing `#include` or namespace not imported
- **Common cases**: `VkCommandBuffer`, `PFN_vkCmdDrawIndexed`, `std::vector` in headers that assume transitive includes
- **Fix**: Add the missing `#include` to the header, not just the .cpp

### C2825: must be a class or namespace when followed by '::'
- **Cause**: Class declaration not visible (header parse failed earlier in include chain)
- **Fix**: Find the FIRST error in the include chain, not the last. Compile headers individually.

### C2248: cannot access private member
- **Cause**: Member used in public method but declared in private section
- **Fix**: Move the member/type to public, or add a public accessor

### C2027: use of undefined type
- **Cause**: Forward declaration only; full definition needed for method calls
- **Fix**: Include the full header, not just forward-declare

### C2198: too few arguments for call
- **Cause**: Function pointer type mismatch (e.g., `PFN_vkCmdPushConstants` expects 6 args, call passes 5)
- **Fix**: Match the exact signature from the Vulkan spec — `PFN_vkCmdPushConstants` has `stageFlags` as the 3rd parameter

### C4010: single-line comment contains line-continuation
- **Cause**: `\\` at end of comment line (artifact of copy-paste from markdown)
- **Fix**: Remove trailing `\\` from comment lines

### C4324: structure was padded due to alignment specifier
- **Cause**: `alignas(kCacheLineSize)` on atomics
- **Severity**: Warning only, safe to suppress with `/w44324`

### C4100: unreferenced formal parameter
- **Cause**: Parameter named but unused in function body
- **Severity**: Warning only, suppress with `/w44100` or use `(void)param`

### C4996: getenv may be unsafe
- **Cause**: MSVC deprecation of `std::getenv`
- **Fix**: Add `_CRT_SECURE_NO_WARNINGS` compile definition via `add_compile_definitions()` in CMakeLists.txt

## DLL Export for Vulkan Implicit Layers

`VKAPI_ATTR` expands to nothing on Windows (`#define VKAPI_ATTR`). Vulkan layer entry points must be explicitly exported:

```cpp
#ifdef _WIN32
#define SYNAPSE_EXPORT __declspec(dllexport)
#else
#define SYNAPSE_EXPORT
#endif

extern "C" {
SYNAPSE_EXPORT VKAPI_ATTR PFN_vkVoidFunction VKAPI_CALL
SynapseLayer_vkGetInstanceProcAddr(VkInstance instance, const char* pName);
}
```

## CMake WINDOWS_EXPORT_ALL_SYMBOLS

Must be a **CMake variable**, not a target property:
```cmake
# Correct — VS generator respects this
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# Wrong — ignored by VS generator
set_target_properties(MyLib PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)
```

## Cross-Platform Inline Assembly

```cpp
#ifdef _MSC_VER
#include <intrin.h>
#define compiler_barrier() _ReadWriteBarrier()
#else
#define compiler_barrier() asm volatile("" ::: "memory")
#endif
```

## Docker Desktop on Windows

- Docker Desktop WSL2 backend may fail to start if WSL2 distribution is stopped
- `docker info` hangs (no daemon response) — kill Docker processes and restart
- Fall back to local MSVC build when Docker unavailable
- `cmd.exe /c "batch_file.bat"` is the correct way to run batch files from bash/MSYS2

## Struct-Before-Use Ordering in Classes

MSVC requires that a nested struct/typedef be defined before it's used in a member declaration, even within the same class. GCC/Clang are more lenient.

```
error C3646: 'hai_builder_': unknown override specifier
error C4430: missing type specifier - int assumed
```

**Cause**: `struct JITStutterStats` defined at line 140 but used at line 46 as a return type.

**Fix**: Move the struct definition above its first use. In a class body, declaration order matters — unlike .cpp files where forward declarations suffice.

## `_CRT_SECURE_NO_WARNINGS` as Compile Definition

The `getenv` warning (C4996) must be suppressed via CMakeLists.txt, not just `#define` in source:

```cmake
# Correct: compile definition propagates to all translation units
add_compile_definitions(_CRT_SECURE_NO_WARNINGS)

# Wrong: only affects the single file where #define appears
# (adding #define _CRT_SECURE_NO_WARNINGS at top of platform_config.h)
```

## Vulkan SDK without Installer

Download from `https://raw.githubusercontent.com/KhronosGroup/Vulkan-Headers/main/include/`:

**Core headers** (4 files):
- `vulkan/vulkan.h`, `vulkan/vulkan_core.h`, `vulkan/vk_platform.h`, `vulkan/vk_layer.h`

**Video codec headers** (11 files in `vk_video/`):
- `vulkan_video_codecs_common.h` (REQUIRED — included by all codec headers)
- `vulkan_video_codec_h264std.h`, `vulkan_video_codec_h264std_encode.h`, `vulkan_video_codec_h264std_decode.h`
- `vulkan_video_codec_h265std.h`, `vulkan_video_codec_h265std_encode.h`, `vulkan_video_codec_h265std_decode.h`
- `vulkan_video_codec_av1std.h`, `vulkan_video_codec_av1std_encode.h`, `vulkan_video_codec_av1std_decode.h`
- `vulkan_video_codec_vp9std.h`, `vulkan_video_codec_vp9std_decode.h`

**C++ bindings**: `vulkan/vulkan_raii.hpp`

**URL pattern**: `https://raw.githubusercontent.com/KhronosGroup/Vulkan-Headers/main/include/<path>`

**Library**: copy `vulkan-1.dll` from `C:\Windows\System32\` to `vulkan_sdk/bin/`, and `vulkan-1.lib` from any installed Vulkan loader to `vulkan_sdk/lib/`

**CMake**: set `VULKAN_SDK` env var pointing to the parent directory (containing `include/`, `lib/`, `bin/`)
