# Notes about the QASM Parser that is built here

### What does this package do?
This is package intended to take OpenQASM 3.0 circuits and convert them to the Clifford+T basis. Converting an arbitary gate to series of Clifford operations is not a trivial task. In this package, we take advantage of `newsynth` which is Haskell package which approximates RZ(theta) gates as series of {H,S,T} gates. The conversion relies on this package which based paper by Ross and Seilinger. 

### What does this package not do?
Right now not all gates are supported to the Clifford+T basis. We only support the standard gates in OpenQASM 3.0 as of now. Even not all the gates in this are.
One approach would be to approximate arbitrary gates as  aprroximations of Clifford+T gates. 
This does not unroll any control flow operators leaving them as it is. If a non-clifford standard gate is encountered, that is converted to a Clifford+T representation.

### What are the gates in that are considered to be in the Clifford+T set in this parser?
In literature, {H,S and CNOT} are considered to be the generators of the Clifford Group. Here we do not convert all the gates to the generating set of gates. I consider a larger set of Clifford Gates, thus allowing the list of instructions to be minimal. This is an issues because approximation of RZ(theta) can be a very long string of gates.
The basis set considered here is the following:
`SingleQubitClifford` = {I, X, Y, Z, S, Sdag, H, sqrtX, sqrtXdag}
`TwoQubitClifford` = {CX,CY,CZ,SWAP}

### What are the standard gates that need to be converted to the Clifford+T group?
The following gates are supported that are converted to the Clifford Group
`SingleQubitGates` = {rx, ry, rz}
`TwoQubitGates` = {}
`MultiQubitGates`  = {toffoli, ccz}
These are the standard gates from OpenQASM that are not supported yet. 
`GatesNotSupported` = {ch, cswap, cu}

