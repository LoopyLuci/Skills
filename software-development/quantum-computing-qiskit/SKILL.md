---
name: quantum-computing-qiskit
description: "Use when implementing quantum algorithms with Qiskit."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [quantum-computing, Qiskit, quantum-algorithms, qubits, gates, circuits]
    related_skills: [algorithm-design-techniques, cryptography-implementation-patterns, compiler-interpreter-basics]
---

# Quantum Computing with Qiskit

Implementing quantum algorithms with IBM Qiskit — from qubits and quantum gates through Grover's search, Shor's algorithm, and variational quantum eigensolvers.

## When to Use

- Learning quantum computing concepts
- Implementing quantum algorithms on simulators or real hardware
- Exploring quantum advantage for specific problems
- Building hybrid quantum-classical algorithms

## Quantum Computing Basics

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Bell state: entanglement
qc = QuantumCircuit(2, 2)
qc.h(0)          # Hadamard gate on qubit 0
qc.cx(0, 1)      # CNOT gate (control=0, target=1)
qc.measure([0, 1], [0, 1])

# Run on simulator
simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()
# Expected: {'00': ~512, '11': ~512} — entanglement!

# Grover's search: unsorted database search O(√N)
def grover_search(n_qubits: int, target: str):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(range(n_qubits))  # Superposition
    # Oracle + diffusion (repeated √N times)
    # ...
    return qc
```

## Verification Checklist

- [ ] Quantum circuit designed for target algorithm
- [ ] Simulator tests pass (statevector or AerSimulator)
- [ ] Circuit depth and gate count optimized
- [ ] Error mitigation considered for real hardware
- [ ] Results statistically significant (enough shots)
- [ ] Classical hybrid integration working (if VQE/QAOA)
- [ ] Algorithm complexity understood (quantum speedup)
