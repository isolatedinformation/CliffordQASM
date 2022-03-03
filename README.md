# CliffordT conversion of OpenQASM 3.0 Circuits
Developed as a part of the submission to the QOSF March Cohort application.   
Install package using `pip install -e .` after cloning the repo locally.

For a detailed explanation of the work flow of the QASMParser and gates that are supported for conversion to Clifford+T circuits, take a look at [this file](docs/NOTES.md)

- [ ] Figure out what to do with phase gate that is equivalent to the RZ Gates.

### Dependencies
1. `newsynth` -- Haskell Package to convert Rz rotation to a sequence of H,S and T gates

### Notes
- Controlled Hadamard is not in the Clifford Group --> QC Stack Exchange
- Decompsition of the Controlled Hadarmard Gate is available on Qiskit documentation
- https://threeplusone.com/pubs/on_gates.pdf - Good resource on Quantum Gates
- https://qiskit.org/textbook/ch-gates/more-circuit-identities.html - Qiskit documentation on circuit identities
- 