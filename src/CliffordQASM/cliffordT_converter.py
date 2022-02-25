from dataclasses import dataclass
import subprocess
from typing import Dict, List, Tuple
import numpy as np
from CliffordQASM.gates import MultiQubitGate, SingleQubitGate, TwoQubitGate
from qasm_parser import QASMParser

RotationGates_to_Z_basis: Dict[str, Tuple[str]] = {
    "RX": ["H", "RZ", "H"],
    "RY": ["S", "H", "RZ", "H", "Sdag"],
    "RZ": ["RZ"],
}  # Need this for proper application of the gridsynth.

Single_Qubit_CliffordT_Basis: Tuple = ("I", "X", "Y", "Z", "H", "S", "Sdag", "T")
Two_Qubit_CliffordT_Basis: Tuple = ("CNOT",)

single_qubit_gates_that_can_be_converted = ("RX", "RY", "RZ")


def generate_clifford_T_approximation_from_rz_gate(angle: float) -> str:
    n: float = angle / np.pi
    phase_gate_angle: str = f"pi/{n}"
    command_output = subprocess.check_output(f"gridsynth {phase_gate_angle}", shell=True).decode(
        "utf-8"
    )
    clifford_sequence = command_output.replace("W", "")  # drop the global phase
    clifford_sequence = clifford_sequence[::-1]  # reverse to go from operator to circuit form

    return clifford_sequence


def single_qubit_gate_to_CliffordT(gate: SingleQubitGate) -> List[SingleQubitGate]:
    """
    Function to convert a Gate to convert to a Clifford Basis
    """
    if not isinstance(SingleQubitGate):
        raise TypeError("Please ensure gate is of type SingleQubitGate")

    if gate.gate_name in Single_Qubit_CliffordT_Basis:
        return [gate]

    if gate.gate_name not in single_qubit_gates_that_can_be_converted:
        raise NotImplementedError("Custom gates are not supported yet!")

    new_gates = list()

    for gate_name in RotationGates_to_Z_basis[gate.gate_name]:
        if gate_name == "RZ":
            for clifford in generate_clifford_T_approximation_from_rz_gate(gate.gate_args) 


class CliffordInstructionGenerator:
    def __init__(self, instruction: str = None) -> None:
        self.instruction: str = instruction
        self.clifford_circuit: List[str] = []

    def _convert_ccz_to_cx(self):
        pass

    def _convert_PauliGates_to_ZBasis(self):
        pass

    def _generate_qasm_output(self):
        for instruction in self.circuit:
            pass

    def maintain_suffixes_and_prefixes(self):
        pass