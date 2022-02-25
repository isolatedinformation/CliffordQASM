import subprocess
from typing import Dict, List, Tuple
import numpy as np
from CliffordQASM.gates import MultiQubitGate, SingleQubitGate, TwoQubitGate
from qasm_parser import GATES_TO_CONVERT

ROTATION_GATES_T0_Z_BASIS: Dict[str, Tuple[str]] = {
    "RX": ["H", "RZ", "H"],
    "RY": ["S", "H", "RZ", "H", "Sdag"],
    "RZ": ["RZ"],
}  # Need this for proper application of the gridsynth.


SINGLE_QUBIT_CLIFFORDT_BASIS: Tuple = ("I", "X", "Y", "Z", "H", "S", "Sdag", "T")
TWO_QUBIT_CLIFFORDT_BASIS: Tuple = ("CNOT", "CX", "CY", "CZ")
GATES_THAT_CAN_BE_CONVERTED = ("RX", "RY", "RZ")


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

    if gate.gate_name in SINGLE_QUBIT_CLIFFORDT_BASIS:
        return [gate]

    if gate.gate_name not in GATES_THAT_CAN_BE_CONVERTED:
        raise NotImplementedError("Custom gates are not supported yet!")

    new_gates = list()

    for gate_name in ROTATION_GATES_T0_Z_BASIS[gate.gate_name]:
        if gate_name == "RZ":
            for clifford in generate_clifford_T_approximation_from_rz_gate(gate.gate_args):
                pass


class CliffordInstructionGenerator:
    """
    Class to convert Non-Cliiford instructions as Sequence of Clifford Operations.
    """

    def __init__(self, instruction: str = None) -> None:
        self.instruction: str = None
        self.instruction_prefix: str = None
        self.instruction_suffix: str = None
        self._process_instruction(instruction)

    def _process_instruction(self) -> None:
        pass

    def gate(self):
        pass

    def get_qasm_instructions(self) -> List[str]:
        if not any(non_cliff in self.instruction for non_cliff in GATES_TO_CONVERT):
            return [self.instruction]
        else:
            prefix = None
            suffix = None

    def _convert_ccz_to_cx(self):
        pass

    def _convert_PauliGates_to_ZBasis(self):
        pass

    def _generate_qasm_output(self):
        for instruction in self.circuit:
            pass

    def maintain_suffixes_and_prefixes(self):
        pass
