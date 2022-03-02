from ctypes import Union
import subprocess
from typing import Dict, List, Tuple
from cirq import CCX
import numpy as np
from CliffordQASM.gates import AbstractGate, MultiQubitGate, SingleQubitGate, TwoQubitGate
from pyrsistent import T

# from CliffordQASM.qasm_parser import GATES_TO_CONVERT

ROTATION_GATES_T0_Z_BASIS: Dict[str, List[str]] = {
    "rx": ["h", "rz", "h"],
    "ry": ["s", "h", "rz", "h", "sdg"],
    "rz": ["rz"],
}  # Need this for proper application of the gridsynth.

CCX_TO_CLIFFORDT: Tuple[Tuple[str, Union[List[int], int]]] = (
    ("h", 2),
    ("tdg", 0),
    ("t", 1),
    ("t", 2),
    ("cx", [0, 1]),
    ("cx", [2, 0]),
    ("cx", [1, 2]),
    ("tdg", 0),
    ("cx", [1, 0]),
    ("tdg", 0),
    ("tdg", 1),
    ("t", 2),
    ("cx", [2, 0]),
    ("s", 0),
    ("cx", [1, 2]),
    ("cx", [0, 1]),
    ("h", 2),
)

SINGLE_QUBIT_CLIFFORDT_BASIS: Tuple = ("id", "x", "y", "z", "h", "s", "sdg", "t")
TWO_QUBIT_CLIFFORDT_BASIS: Tuple = ("cx", "cy", "cz", "swap")
GATES_THAT_CAN_BE_CONVERTED: Tuple = ("rx", "ry", "rz", "ccx")


def generate_clifford_T_approximation_from_rz_gate(angle: float) -> str:
    n: float = angle / np.pi
    phase_gate_angle: str = f"pi/{n}"
    command_output = subprocess.check_output(f"gridsynth {phase_gate_angle}", shell=True).decode(
        "utf-8"
    )
    clifford_sequence = command_output.replace("W", "")  # drop the global phase
    clifford_sequence = clifford_sequence[::-1]  # reverse to go from operator to circuit form

    return clifford_sequence.lower()  # return in lowercase to keep with OpenQASM spec


def single_qubit_gate_to_CliffordT(gate: SingleQubitGate) -> List[SingleQubitGate]:
    """
    Function to convert a Gate to convert to a Clifford Basis
    """
    if not isinstance(gate, SingleQubitGate):
        raise TypeError("Please ensure gate is of type SingleQubitGate")

    if gate.gate_name in SINGLE_QUBIT_CLIFFORDT_BASIS:
        return [gate]

    if gate.gate_name not in GATES_THAT_CAN_BE_CONVERTED:
        raise NotImplementedError("Only rotation gates are supported now!")

    new_gates = list()

    for gn in ROTATION_GATES_T0_Z_BASIS[gate.gate_name]:
        if gn == "rz":
            for clifford in generate_clifford_T_approximation_from_rz_gate(gate.gate_args):
                new_gates.append(
                    SingleQubitGate(gate_name=clifford, qubit_register=gate.qubit_register)
                )
        else:
            new_gates.append(SingleQubitGate(gate_name=gn, qubit_register=gate.qubit_register))

    return new_gates


def two_qubit_gate_to_CliffordT(gate: TwoQubitGate) -> List[Union[SingleQubitGate, TwoQubitGate]]:
    raise NotImplementedError


def toffoli_to_CliffordT(gate: MultiQubitGate) -> List[Union[SingleQubitGate, TwoQubitGate]]:
    """
    Decomposition from arxiv://1210.0974 - circuit (3) to minimse T-depth: T-depth = 4
    """
    assert isinstance(gate, MultiQubitGate), "gate must be of type MultiQubitGate"
    new_gates = list()

    for gn, reg_index in CCX_TO_CLIFFORDT:
        if isinstance(reg_index, int):
            new_gates.append(
                SingleQubitGate(gate_name=gn, qubit_register=gate.qubit_register[reg_index])
            )
        else:
            registers = [gate.qubit_register[reg_index[0]], gate.qubit_register[reg_index[1]]]
            new_gates.append(TwoQubitGate(gate_name=gn, qubit_register=registers))

    return new_gates


class CliffordInstructionGenerator:
    """
    Class to convert Non-Cliiford instructions as Sequence of Clifford Operations.
    """

    def __init__(self, instruction: str = None) -> None:
        self.instruction: str = None
        self._instruction_prefix: str = None
        self._instruction_suffix: str = None
        self._gate: AbstractGate = None  # change to gate local gate representation
        self._process_instruction(instruction)

    def _process_instruction(self, instruction) -> None:
        """
        This functions processes the given non-clifford instruction and saves the
        prefix and suffix of the non-clifford instructions. It also converts the
        instruction to internal gate representation.
        """
        if instruction[-1] is "{":
            # case to cover statements in "gate ...  {"
            self.instruction = instruction
        elif instruction[-1] is "}" and len(instruction) == 1:
            self.instruction = instruction

    def _get_qasm_instructions(self) -> List[str]:
        if not any(non_cliff in self.instruction for non_cliff in GATES_THAT_CAN_BE_CONVERTED):
            return [self.instruction]
        else:
            prefix, suffix = self.get_suffixes_and_prefixes()

    def _convert_toffoli_to_cx(self):
        pass

    def _generate_qasm_output(self):
        pass

    def get_suffixes_and_prefixes(self) -> Tuple[str, str]:
        pass
