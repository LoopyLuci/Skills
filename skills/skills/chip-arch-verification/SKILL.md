---
name: chip-arch-verification
description: "Use when verifying chip arch. UVM, formal, assertions."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [chip, arch-verification, uvm, formal, assertions]
    related_skills: [rtl-design-verilog, timing-analysis-digital]
---

# Chip Architecture Verification

## Overview
Verify semiconductor chip architectures using UVM methodology, formal verification, and assertion-based verification. Covers testbench infrastructure, constrained random stimulus, coverage closure, and debug workflows for complex SoC designs.

## When to Use
- "Set up UVM testbench for chip verification"
- "Verify chip architecture components"
- "Achieve coverage closure on RTL"
- "Debug assertion failures in simulation"
- "Perform formal verification of critical blocks"

## UVM Testbench Template
```systemverilog
class arch_verification_env extends uvm_env;
    bus_agent bus_agent;
    mem_agent mem_agent;
    arch_scoreboard scoreboard;
    
    `uvm_component_utils(arch_verification_env)
    
    function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        bus_agent = bus_agent::type_id::create("bus_agent", this);
        mem_agent = mem_agent::type_id::create("mem_agent", this);
        scoreboard = arch_scoreboard::type_id::create("scoreboard", this);
    endfunction
    
    function void connect_phase(uvm_phase phase);
        bus_agent.monitor.ap.connect(scoreboard.bus_in);
        mem_agent.monitor.ap.connect(scoreboard.mem_in);
    endfunction
endclass
```

## Assertion Patterns
```systemverilog
// No deadlock in arbiter
property no_deadlock_p;
    @(posedge clk) disable iff (!rst_n)
    (!grant_all |-> ##1 (!grant_all)[*1:$]);
endproperty
```

## Formal Verification Setup
```tcl
dut -gate -auto-wire
clock -exp 'posedge clk' -rst -exp '!rst_n'
set_max_time 300
prove -all
```

## Coverage Targets
- Code coverage: ≥95% lines, ≥90% branches
- Functional coverage: ≥100% on critical paths
- Assertion coverage: ≥100%

## Common Pitfalls
1. Assertions too strict — account for pipeline delays
2. Incomplete constraints — waste coverage points
3. No disable iff in assertions — false failures during reset
4. Insufficient coverage models
5. Formal proof timeouts — over-constrain
6. X propagation in simulators

## Verification Checklist
- [ ] UVM agents for all interfaces implemented
- [ ] Scoreboard validates against reference model
- [ ] ≥95% line coverage achieved
- [ ] ≥90% branch coverage achieved
- [ ] Functional coverage ≥100% on critical paths
- [ ] Formal verification passes on critical blocks
- [ ] All assertions covered in at least one test
- [ ] Coverage closure report generated
- [ ] Random stimulus ≥1000 sequences