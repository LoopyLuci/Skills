---
name: reverse-engineering-basics
description: "Use when reverse engineering binaries and malware."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [reverse-engineering, malware-analysis, Ghidra, IDA, disassembly, decompilation]
    related_skills: [exploit-development-basics, binary-exploitation-rop, evasion-techniques-av-bypass, threat-hunting-methods]
---

# Reverse Engineering Basics

Reverse engineering binaries — from static analysis (Ghidra, IDA) through dynamic analysis (x64dbg, GDB), malware triage, and protocol reversing.

## When to Use

- Analyzing malware samples
- Finding vulnerabilities in binaries for exploit development
- Understanding proprietary protocols
- Deobfuscating code
- Patching binaries for security research

## Reverse Engineering Workflow

```python
RE_PHASES = {
    'static_analysis': 'Strings, file type, entropy, PEiD, imported functions — quick triage',
    'disassembly': 'Ghidra/IDA — decompile to pseudo-C, identify functions, control flow',
    'dynamic_analysis': 'x64dbg/GDB — set breakpoints, trace execution, dump memory',
    'network_analysis': 'Wireshark/fakenet — capture and intercept network traffic',
    'deobfuscation': 'Unpack UPX/themida/VMProtect, deobfuscate strings, decode XOR',
}

PE_ANALYSIS_SECTIONS = {
    '.text': 'Executable code — main analysis target',
    '.rdata': 'Read-only data (imports, strings)',
    '.data': 'Read-write data (globals, configuration)',
    '.rsrc': 'Resources (icons, manifests, embedded binaries)',
    '.packed': 'Unusual names or high entropy indicate packing',
}

# Analyze with strings (Linux/macOS)
STRINGS_ANALYSIS = "strings -n 6 malware.exe | sort -u | grep -E 'http|http|\.com|\.exe|\.dll'"
```

## Verification Checklist

- [ ] File type identified (PE, ELF, Mach-O, script, document)
- [ ] Strings extracted and reviewed for IOC/IP/paths/registry
- [ ] Imports/exports analyzed (suspicious API calls?)
- [ ] Disassembled/decompiled (Ghidra, IDA, Binary Ninja)
- [ ] Control flow graph reviewed (anti-disassembly, obfuscated jumps)
- [ ] Packing detected and unpacked (UPX, ASPack, custom)
- [ ] Hardcoded secrets extracted (keys, passwords, C2 URLs)
- [ ] Dynamic analysis in sandbox (no production network)
- [ ] Network indicators extracted (domains, IPs, protocols)
- [ ] IOCs documented for detection engineering
