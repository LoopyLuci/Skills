---
name: windows-hyperv-vm
description: Use when setting up a Linux VM on Windows via Hyper-V — creating the VM, unattended installs via cidata cloud-init (Omarchy), and GPU acceleration limits on Windows 10/11 Pro.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [windows, general]
---

-
# Windows Hyper-V VM Setup

## When to use

- Setting up a Linux VM on Windows using Hyper-V (Generation 2, UEFI)
- Unattended installs via cidata cloud-init drive (Omarchy, and any distro with NoCloud support)
- Creating ISOs on Windows when `genisoimage`/`mkisofs`/`xorriso` are not available
- Figuring out GPU acceleration options for a Linux VM on Windows 10/11 Pro

## VM creation (single PowerShell call)

All steps below compose into one script. Run from **elevated PowerShell** (Run as Administrator).

```powershell
$vmName  = "vm-name"
$vmPath  = "C:\Users\Server\Virtual Machines"
$isoPath = "C:\path\to\os.iso"
$cidatPath = "C:\path\to\cidata.iso"  # if using unattended install

# 1. Create VM
New-VM -Name $vmName `
    -Path $vmPath `
    -MemoryStartupBytes 16GB `
    -Generation 2 `
    -SwitchName "Default Switch" `
    -NoVHD | Out-Null

# 2. Configure resources
Set-VM -Name $vmName -DynamicMemoryEnabled $false          # static RAM (recommended for Linux)
Set-VMProcessor -VMName $vmName -Count 8                    # vCPUs: half of 12-thread host
Set-VMFirmware -VMName $vmName -EnableSecureBoot Off        # REQUIRED by Omarchy and most Linux

# 3. Attach ISOs (OS first, cidata second for unattended)
Add-VMDvdDrive -VMName $vmName -Path $isoPath -ErrorAction Stop
Add-VMDvdDrive -VMName $vmName -Path $cidataPath -ErrorAction Stop

# 4. Create 64 GB dynamic VHDX
$diskPath = Join-Path $vmPath "$vmName.vhdx"
New-VHD -Path $diskPath -SizeBytes 64GB -Dynamic | Out-Null
Add-VMHardDiskDrive -VMName $vmName -Path $diskPath -ControllerType SCSI

# 5. Boot order: disk first (falls through to ISO on first boot)
$diskDrive = Get-VMHardDiskDrive -VMName $vmName -ControllerType SCSI | Select-Object -First 1
Set-VMFirmware -VMName $vmName -BootOrder $diskDrive

# 6. Start
Start-VM -Name $vmName
vmconnect localhost $vmName
```

### Resource allocation decision points

| Resource | Recommendation | Rationale |
|----------|---------------|-----------|
| vCPUs | 6–8 (of 12 host threads) | Leave 4–6 threads for Windows host. More than 8 starves the host and Hyper-V time-slices anyway. |
| RAM | 16 GB (of 32 GB host) | Sweet spot for responsive host + well-powered guest. |
| Disk | 64 GB dynamic VHDX | Uses only what the guest writes. Static disk wastes space upfront. |
| Generation | 2 (UEFI) | Required for modern Linux distros including Omarchy. |
| Secure Boot | **Off** | Omarchy and most Linux distros require this. |
| Network | Default Switch (NAT) | Works out of the box, no extra switch configuration needed. |

## Unattended install via cidata (Omarchy)

Omarchy supports unattended installs via a `cidata` cloud-init drive (NoCloud datasource). When the installer finds a second drive labeled `cidata`, it copies config files, skips the setup wizard, and reboots into the finished system.

### Config files

| File | Required | Purpose |
|------|----------|---------|
| `user_configuration.json` | Yes | Hostname, timezone, keyboard layout, disk encryption |
| `user_credentials.json` | Yes | Username + SHA-512 crypt password hash |
| `user_full_name.txt` | No | Git full name |
| `user_email_address.txt` | No | Git email |
| `authorized_keys` | No | SSH public keys, one per line |
| `tailscale_authkey` | No | Tailscale auth key for tailnet join on first boot |
| `user_encrypt_installation.txt` | No | `true` when `disk_encryption` is set |

**Critical:** All files must be in a directory, and the ISO volume label MUST be `cidata` (case-sensitive).

### user_configuration.json

```json
{
  "hostname": "omarchy-vm",
  "timezone": "America/New_York",
  "keyboard_layout": "us",
  "disk": {
    "encryption": true
  }
}
```

### user_credentials.json

Password hash via SHA-512 crypt:

```powershell
openssl passwd -6 "YourPassword"
```

Output is a `$6$salt$hash...` string. Placement:

```json
{
  "username": "OmarchyVM",
  "password_hash": "$6$...hash..."
}
```

### Creating the cidata ISO on Windows

When `genisoimage`, `mkisofs`, or `xorriso` are not available (the common case on Windows), use `pycdlib`:

```python
# Save as gen_cidata.py and run with the Hermes venv python
import io, os, pycdlib

CIDATA_DIR = r"C:\Projects\Omarchy\vm-setup\cidata"
OUTPUT_ISO = r"C:\Projects\Omarchy\vm-setup\cidata.iso"

iso = pycdlib.PyCdlib()
iso.new(vol_ident="cidata")

for root, dirs, files in os.walk(CIDATA_DIR):
    for fname in files:
        fpath = os.path.join(root, fname)
        relname = os.path.relpath(fpath, CIDATA_DIR)
        if relname.startswith("./"):
            relname = relname[2:]
        with open(fpath, "rb") as f:
            data = f.read()
        iso.add_fp(io.BytesIO(data), len(data), f"/{relname}")

iso.write(OUTPUT_ISO)
iso.close()
print(f"Created: {OUTPUT_ISO}")
```

Run with the Hermes Agent venv python (`C:\Users\Server\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`), which has pycdlib installed.

**Pitfall:** ISO9660 level 1 filenames are 8.3 format (uppercase A-Z, 0-9, _ only). pycdlib defaults to level 1 and will reject longer filenames. The cloud-init/NoCloud datasource reads files by their full path on the filesystem, so the ISO9660 names must match what the installer expects. Use `vol_ident="cidata"` (the volume label) — the installer checks this, not the filename.

### Alternative: genisoimage via MSYS2

If MSYS2 is installed, `genisoimage` is available:

```bash
pacman -S genisoimage
genisoimage -o cidata.iso -volid cidata -joliet -rock cidata/
```

## GPU acceleration — what works and what doesn't

### The hard limit: DDA is not on Windows 10/11 Pro

**Discrete Device Assignment (DDA)** — full GPU passthrough — is available ONLY on Windows Server and Windows Enterprise. Windows 10/11 Pro cannot do it. This is a platform limitation, not a configuration issue.

### GPU-PV (GPU Paravirtualization) — exists but unreliable for Linux

GPU-PV partitions the host GPU and shares it with VMs via a paravirtualized interface. Available on Windows 10/11 client. Setup:

```powershell
Set-VM -VMName "vm-name" -GuestControlledCacheTypes $true `
    -LowMemoryMappedIoSpace 3072MB -HighMemoryMappedIoSpace 30720MB
Set-VMGpuPartitionAdapter -VMName "vm-name"
```

**Reality for Linux guests:** GPU-PV was designed for Windows guests. Community reports (2023–2025) consistently show:
- Linux guests see the GPU in Device Manager but it often doesn't function
- `glxgears` and other OpenGL tests frequently crash the desktop compositor
- Some setups work partially; many don't work at all
- GPU-PV + a passed-through PCIe device (DDA) is known to conflict
- The feature is unstable across Windows cumulative updates

**Verdict:** Do not rely on GPU-PV for a Linux VM on Windows 10/11 Pro. It may work for basic 2D acceleration, but expect instability.

### What actually works

| Approach | Setup | Linux GPU support | Best for |
|----------|--------|-------------------|----------|
| **Software rendering (default)** | Nothing | Fine for CLI, terminals, light desktop | Most VM use cases |
| **QEMU + WHPX + virtio-gpu/virgl** | Install QEMU on Windows separately | Good OpenGL via virglrenderer (Linux 6.13+, virgl 1.0+) | When you need real GPU acceleration on Windows |
| **KVM + VFIO (Linux host)** | Reboot to Linux | Full GPU passthrough | When GPU passthrough is required |

**QEMU+WHPX alternative:** Omarchy's own `try-omarchy-windows` project uses QEMU with WHPX acceleration and virtio-gpu/virgl for GPU-accelerated Linux VMs on Windows. The approach uses:
- `qemu-system-x86_64w.exe` (Windows QEMU build)
- `-machine q35,accel=whpx` (Windows Hypervisor Platform acceleration)
- `-device virtio-vga-gl` with Venus Vulkan for GPU mode (when WINQ-EMU is installed)
- Falls back to `-device virtio-gpu-pci` with llvmpipe CPU rendering when no GPU backend is available

This is a heavier setup (requires QEMU install, WHPX enabled, most likely a patched QEMU build), but it's the proven path for GPU-accelerated Linux VMs on Windows.

### Practical recommendation for this system

Given dual Radeon RX Vega GPUs, 12 threads, 32 GB RAM, Windows 10 Pro:

1. **For the Omarchy VM:** Accept software rendering. Omarchy's Hyprland compositor will run, but without GPU acceleration it'll be less smooth. For CLI work, terminal, editor, and web browsing, this is perfectly fine.
2. **If GPU acceleration is needed later:** Install QEMU for Windows and use the `try-omarchy-windows` approach (virtio-gpu with WHPX). This is more setup work but gives real GPU acceleration.
3. **For full GPU passthrough:** Not possible on Windows 10 Pro. Would need Windows Server, or a Linux host with KVM/VFIO.

## Pitfalls

- **Secure Boot must be off** — check this first if the VM won't boot. Many Linux distros (including Omarchy) don't support Secure Boot in the VM context.
- **Don't over-allocate vCPUs.** 8 vCPUs on a 12-thread host leaves only 4 for Windows. Windows becomes sluggish and the VM doesn't benefit because Hyper-V time-slices.
- **Dynamic memory on Linux** can cause performance jitter. Use static allocation.
- **cidata volume label must be exactly `cidata`** — case-sensitive. Wrong label = interactive installer, not unattended.
- **ISO checksums:** Always verify after download. Omarchy publishes SHA-256 at `https://iso.omarchy.org/omarchy-<version>.iso.sha256`.
- **After unattended install completes:** eject both ISOs. The VM will try to boot from the ISO if attached.
- **IMAPI2 COM (`IMAPI2.ISOImageBuilder`) frequently fails** with `80040154 Class not registered` in non-interactive PowerShell sessions. Don't rely on it — use `pycdlib` or `genisoimage` instead.
- **pycdlib ISO9660 filename restrictions:** Default interchange level 1 enforces 8.3 uppercase filenames. For config files with longer names (like `user_configuration.json`), use Joliet extension or accept the 8.3-shortened names — cloud-init reads by filesystem path, so the volume label and directory structure matter more than individual filename length in the ISO9660 namespace.

## References

- [[omarchy-cidata]] — Omarchy unattended install: full config file reference, password hashing, cidata structure
- [[iso-creation-pycdlib]] — Creating ISOs on Windows using pycdlib when genisoimage/mkisofs are unavailable
