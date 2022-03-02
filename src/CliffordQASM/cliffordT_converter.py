import subprocess
from typing import Dict, List, Tuple, Union
import numpy as np
from CliffordQASM.gates import AbstractGate, MultiQubitGate, SingleQubitGate, TwoQubitGate
import warnings

# from CliffordQASM.qasm_parser import GATES_TO_CONVERT

ROTATION_GATES_T0_Z_BASIS: Dict[str, List[str]] = {
    "rx": ["h", "rz", "h"],
    "ry": ["s", "h", "rz", "h", "sdg"],
    "rz": ["rz"],
}  # Need this for proper application of the gridsynth.

CCX_TO_CLIFFORDT = (
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
    n: float = np.pi / angle
    phase_gate_angle: str = f"pi/{n}" if n else f"0"
    command_output = subprocess.check_output(f"gridsynth {phase_gate_angle}", shell=True).decode(
        "utf-8"
    )
    clifford_sequence = command_output.replace("W", "")  # drop the global phase
    clifford_sequence = clifford_sequence[::-1].strip()  # reverse string for gate order

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
                if clifford == "i":
                    continue  # ignore identities
                new_gates.append(
                    SingleQubitGate(gate_name=clifford, qubit_register=gate.qubit_register)
                )

        else:
            new_gates.append(SingleQubitGate(gate_name=gn, qubit_register=gate.qubit_register))

    return new_gates


def two_qubit_gate_to_CliffordT(gate: TwoQubitGate) -> List[Union[SingleQubitGate, TwoQubitGate]]:
    warnings.warn("Two Qubit gates not supported yet! Returns the same gate", UserWarning)
    return [gate]


def toffoli_to_CliffordT(gate: MultiQubitGate) -> List[Union[SingleQubitGate, TwoQubitGate]]:
    """
    Decomposition from arxiv://1210.0974 - circuit (3) to minimse T-depth: T-depth = 4
    """
    assert isinstance(gate, MultiQubitGate), "gate must be of type MultiQubitGate"
    if gate.gate_name not in GATES_THAT_CAN_BE_CONVERTED:
        raise NotImplementedError("Only Toffoli/ccx gate supported now!")

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
        self.gate: AbstractGate = None  # change to gate local gate representation
        self._process_instruction(instruction)

    def _process_instruction(self, instruction) -> None:
        """
        Converts instruction to local gate represetation
        """
        gate_name = list(
            filter(lambda nc_gate: nc_gate in instruction, GATES_THAT_CAN_BE_CONVERTED)
        )[0]
        gate_args = None
        if "(" in instruction:
            gate_args_string = instruction[instruction.find("(") + 1 : instruction.find(")")]
            if "pi" in gate_args_string:
                gate_args = float(gate_args_string[gate_args_string.find("/") + 1 :].strip())
                gate_args = np.pi / gate_args
            else:
                gate_args = float(
                    gate_args_string
                )  # TODO: this can be a potential bug in the future
        if ")" in instruction:
            registers = instruction[instruction.find(")") + 1 :].strip()
        else:
            registers = instruction[len(gate_name) :].strip()

        qubit_regs = [reg.strip() for reg in registers.split(",")]
        if len(qubit_regs) == 1:
            self.gate = SingleQubitGate(
                gate_name=gate_name, qubit_register=qubit_regs, gate_args=gate_args
            )
        elif len(qubit_regs) == 2:
            self.gate = TwoQubitGate(
                gate_name=gate_name, qubit_register=qubit_regs, gate_args=gate_args
            )
        else:
            self.gate = MultiQubitGate(
                gate_name=gate_name, qubit_register=qubit_regs, gate_args=gate_args
            )

    def _get_qasm_instructions(self) -> List[str]:
        if self.gate.num_qubits == 1:
            new_gates = single_qubit_gate_to_CliffordT(self.gate)
        elif self.gate.num_qubits == 2:
            new_gates = two_qubit_gate_to_CliffordT(self.gate)
        else:
            new_gates = toffoli_to_CliffordT(self.gate)

        qasm_op = map(lambda gate: gate.to_qasm(), new_gates)
        return qasm_op
