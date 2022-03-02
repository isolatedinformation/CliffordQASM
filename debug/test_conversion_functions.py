from tokenize import Single
from CliffordQASM.cliffordT_converter import (
    generate_clifford_T_approximation_from_rz_gate,
    single_qubit_gate_to_CliffordT,
    toffoli_to_CliffordT,
)
from CliffordQASM.gates import MultiQubitGate, SingleQubitGate
import numpy as np

# toff = MultiQubitGate(gate_name="ccx", qubit_register=["a", "b", "c"])
# new_gates = toffoli_to_CliffordT(toff)

# string = map(lambda gate: gate.to_qasm(), new_gates)

rz = SingleQubitGate(gate_name="ry", gate_args=np.pi / 3, qubit_register="a")
new_gates = single_qubit_gate_to_CliffordT(rz)
string = map(lambda gate: gate.to_qasm(), new_gates)
print("\n".join(string))

# cliff_string = generate_clifford_T_approximation_from_rz_gate(np.pi)
# print(len(cliff_string))
