from CliffordQASM.qasm_parser import QASMParser

filepath = "qasm_circuits/scqec.qasm"

parser = QASMParser(filepath=filepath)

parser.generate_cliffordT_qasm_file()
