---
name: vulkan-development-windows
description: "Use when setting up or debugging Vulkan on Windows."
category: software-development
tags: [vulkan, windows, graphics, layers, sdk]
---
# Vulkan Development on Windows

Setting up Vulkan SDK, validation layers, and implicit layers on Windows.

## SDK Setup

```powershell
# Download from https://vulkan.lunarg.com/
# Or with winget
winget install -e --id KhronosGroup.VulkanSDK

# Environment variables set by SDK installer:
# VULKAN_SDK = C:\VulkanSDK\1.3.xxx
# PATH += %VULKAN_SDK%\Bin
# VK_LAYER_PATH = %VULKAN_SDK%\Bin
```

## Layer Configuration

```powershell
# Environment variables
$env:VK_INSTANCE_LAYERS = "VK_LAYER_KHRONOS_validation"
$env:VK_LOADER_LAYERS_ENABLE = "VK_LAYER_KHRONOS_validation"
$env:VK_LOADER_DEBUG = "all"          # loader debug output

# Layer files are at:
# %VULKAN_SDK%\Bin\VkLayer_khronos_validation.json
# %VULKAN_SDK%\Bin\VkLayer_khronos_validation.dll
```

## Implicit Layers (Ships with app)

```powershell
# An implicit layer in a JSON manifest:
# VkLayer_my_layer.json
{
  "file_format_version": "1.0.0",
  "layer": {
    "name": "VK_LAYER_SYNAPSE_shim",
    "type": "GLOBAL",
    "library_path": ".\\VkLayer_synapse.dll",
    "api_version": "1.3.250",
    "implementation_version": "1",
    "description": "Synapse iGPU shim layer",
    "functions": {
      "vkGetInstanceProcAddr": "vk_loader_layer_get_instance_proc_addr",
      "vkGetDeviceProcAddr": "vk_loader_layer_get_device_proc_addr"
    },
    "enable_environment": {
      "ENABLE_SYNAPSE": "1"
    },
    "disable_environment": {
      "DISABLE_SYNAPSE": "1"
    }
  }
}
```

## Testing Layers

```powershell
# Check layer is visible
vulkaninfo.exe | Select-String "Synapse"

# Verify layer enumeration
$env:VK_LOADER_DEBUG = "all"
.\my_vulkan_app.exe 2>&1 | Select-String "Synapse"

# Custom layer path
$env:VK_LAYER_PATH = "D:\Projects\iGPU_Shim\build\layer"
$env:ENABLE_SYNAPSE = "1"
.\my_vulkan_app.exe
```

## Vulkan SDK CMake

```cmake
find_package(Vulkan REQUIRED)
if(Vulkan_FOUND)
    target_include_directories(myapp PRIVATE ${Vulkan_INCLUDE_DIRS})
    target_link_libraries(myapp PRIVATE Vulkan::Vulkan)
endif()

# Or manual path
set(VULKAN_SDK "C:/VulkanSDK/1.3.283.0")
target_include_directories(myapp PRIVATE "${VULKAN_SDK}/Include")
target_link_libraries(myapp PRIVATE "${VULKAN_SDK}/Lib/vulkan-1.lib")
```

## Validation Layers

```bash
# Available validation layers:
# VK_LAYER_KHRONOS_validation (recommended)
# VK_LAYER_LUNARG_api_dump     (prints all API calls)
# VK_LAYER_LUNARG_monitor      (FPS/performance)
# VK_LAYER_LUNARG_screenshot   (capture frames)

# Enable via env var
export VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation
export VK_DEBUG_UTILS_MESSAGE_SEVERITY=verbose
export VK_DEBUG_UTILS_MESSAGE_TYPE=validation
```

## Pitfalls

- **VK_LAYER_PATH** must point to the directory containing the JSON manifest, not the DLL
- **enable_environment** in implicit layer manifests must match exactly -- case-sensitive
- **Loader reads all JSON** in VK_LAYER_PATH -- remove old manifests to avoid duplicates
- **32-bit vs 64-bit** -- layer DLL architecture MUST match the app
- **Vulkan SDK redist** -- deploy `vulkan-1.dll` and layer manifests with your app
