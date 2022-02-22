import subprocess
from turtle import st
from typing import List
from cirq import qasm
import numpy as np
from qasm_parser import QASMParser


def generate_clifford_T_approximation_from_rz_gate(angle: float):
    n = angle / np.pi
    phase_gate_angle = f"pi/{n}"
    command_output = subprocess.check_output(f"gridsynth {phase_gate_angle}", shell=True).decode(
        "utf-8"
    )
    clifford_sequence = command_output.replace("W", "")  # drop the global phase
    clifford_sequence = clifford_sequence[::-1]  # reverse to go from operator to circuit form

    return clifford_sequence


class CliffordCircuitGenerator:
    def __init__(self, input_qasm_str) -> None:
        self.circuit: List[str] = input_qasm_str.splitlines()
        self.clifford_circuit: List[str] = []

    def _convert_ccz_to_cx(self):
        pass

    def _convert_PauliGates_to_ZBasis(self):
        pass

    def _generate_qasm_output(self):
        for gate in self.circuit:
            pass
