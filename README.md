# CliffordT conversion of OpenQASM 3.0 Circuits
Developed as a part of the submission to the QOSF March Cohort application.   
Install package using `pip install -e .` after cloning the repo locally. Preferably create a virtual environment for this!

This package takes `.qasm` file and generates a file a new `.qasm` file that converts operations to the Clifford+T basis. For examples outputs look at the `cliffordT_qasm_circuits` folder. The output was generated using `debug/test_clifford.py` See [Usage](#Usage) below for more details

For a detailed explanation of the work flow of the QASMParser and gates that are supported for conversion to Clifford+T circuits, take a look at [About section](#About-the-QASM-Parser)


### Dependencies
1. `newsynth` -- Haskell Package to convert Rz rotation to a sequence of H,S and T gates

### References
1. https://threeplusone.com/pubs/on_gates.pdf - Good resource on Quantum Gates
2. https://qiskit.org/textbook/ch-gates/more-circuit-identities.html - Qiskit documentation on circuit identities
3. https://www.mathstat.dal.ca/~selinger/newsynth/ - Exact and approximate synthesis of Quantum Circuits
4. https://www.nature.com/articles/s41598-018-23764-x.pdf?origin=ppub - Decomposition of controlled Phase gates

# About the QASM Parser

## What does this package do?
This is package intended to take OpenQASM 3.0 circuits and convert them to the Clifford+T basis. Converting an arbitary gate to series of Clifford operations is not a trivial task. In this package, we take advantage of `newsynth` which is Haskell package which approximates RZ(theta) gates as series of {H,S,T} gates. The conversion relies on this package which based paper by Ross and Seilinger. 

## What does this package not do?
Right now not all gates are supported to the Clifford+T basis. We only support the standard gates in OpenQASM 3.0 as of now. Even not all the gates in this are supported for conversion to the clifford+t group.(See below for list of supported gates
### Supported Gates for Conversion
The following gates are supported that are converted to the Clifford Group
`SingleQubitClifford` = {I, X, Y, Z, S, Sdag, H, sqrtX, sqrtXdag}
`TwoQubitClifford` = {CX,CY,CZ,SWAP}
`SingleQubitGates` = {rx, ry, rz, phase}
`TwoQubitGates` = {ch}
`MultiQubitGates`  = {toffoli}
These are the standard gates from OpenQASM that are not supported yet. 
`GatesNotSupported` = {crx, cry, crz, cphase, ccz, cswap, cu}

One approach would be to approximate arbitrary gates as  aprroximations of Clifford+T gates. 
This does not unroll any control flow operators leaving them as it is. If a non-clifford standard gate is encountered, that is converted to a Clifford+T representation.

## Usage
After installing following the steps in [README](../README.md)
```python
import CliffordQASM.QASMPasrer
filepath = "path/to/qasm/file"
parser = QASMParser(filepath= filepath)
parser.generate_cliffordT_qasm_file() # This will generate new file the name cliffordT_oldname.qasm
```
You can play with `debug/test_clifford.py` with your own `qasm` file. The output will be generated in the folder `cliffordT_qasm_circuits`

## Comments on unsupported gates
The unsupported gates can be broken down into clifford+T rotations, however the parser at this stage would generate absurdly long gate sequences as everything is unrolled when generating the qasm output. One can take advantage of the control flow features in `OPENQasm 3.0` to generate a more succint representation. Nonetheless, this would not change the fundamental constraint that gates sequences generated using `gridsynth` are absurdly long that may go beyond capabilities of current hardware. 

For instance, in reference 4, one can find a decomposition of controlled-RZ gate, which is recursive in nature. This can be converted to a recursive fucntion in `OPENQasm 3.0`. This would ideally be the next step in the development of this package, if continued, changing to a transpiler from a mere parser. 