from CliffordQASM.qasm_parser import QASMParser

fp = "qasm_circuits/toffoli.qasm"

parser = QASMParser(filepath=fp)
# print(parser.generate_cliffordTCircuit())
# print(parser.generate_cliffordTCircuit())

print("\n".join(parser.generate_cliffordTCircuit()))
