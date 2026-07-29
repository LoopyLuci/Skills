---
name: evasion-techniques-av-bypass
description: "Use when bypassing AV/EDR detection."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [AV-bypass, EDR-evasion, shellcode, process-injection, syscall, XOR-encrypt]
    related_skills: [exploit-development-basics, command-control-c2-infrastructure, binary-exploitation-rop, red-team-operations]
---

# Evasion Techniques and AV Bypass

Bypassing antivirus and EDR detection — from shellcode encryption and process injection through syscall invocation, AMSI bypass, and living-off-the-land.

## When to Use

- Evading AV detection for red team operations
- Bypassing Windows Defender, CrowdStrike, SentinelOne, Carbon Black
- Implementing process injection without detection
- AMSI bypass for PowerShell execution

## Evasion Methods

```python
EVASION_TECHNIQUES = {
    'shellcode_encryption': 'XOR, AES, RC4 encrypt shellcode, decrypt at runtime',
    'callbacks': 'Execute shellcode via callbacks (EnumWindowProc, CertEnumSystemStore)',
    'syscall_invocation': 'Direct syscalls instead of Win32 API — bypass userland hooks',
    'dll_hollowing': 'Replace loaded DLL in memory (known-good DLL)',
    'process_hollowing': 'Create suspended process of legit binary, replace memory, resume',
    'etw_patching': 'Patch Event Tracing for Windows to disable telemetry',
    'amsi_patching': 'Patch AmsiScanBuffer to return AMSI_RESULT_CLEAN',
    'signed_driver': 'Load signed but vulnerable driver (Bring Your Own Vulnerable Driver)',
    'living_off_land': 'Use built-in tools (PowerShell, WMI, certutil, bitsadmin) to appear benign',
}

# Shellcode XOR encoder
XOR_SHELLCODE_PY = """
def xor_shellcode(sc: bytes, key: bytes) -> bytes:
    return bytes(sc[i] ^ key[i % len(key)] for i in range(len(sc)))

encoded = xor_shellcode(shellcode, b'secret_key')
# decoder stub (asm): loop: lodsb; xor al, key; stosb; loop loop
"""
```

## Verification Checklist

- [ ] Shellcode obfuscated (XOR, AES, or RC4 encrypted)
- [ ] Process injection method chosen (CreateRemoteThread, APC, ThreadHijacking)
- [ ] Direct syscall or indirect syscall for critical APIs (NtCreateThreadEx, NtAllocateVirtualMemory)
- [ ] AMSI bypass tested (registry patching, DLL patch, or reflection)
- [ ] ETW patched or disabled
- [ ] Payload tested against target AV/EDR
- [ ] Traffic encrypted (HTTPS) — not plaintext C2
- [ ] OPSEC: delayed execution, sandbox detection, no suspicious strings
- [ ] Malware analysis sandbox evasion (sleep bypass, wrong OS, no GUI)
