from dataclasses import dataclass
from typing import List


class AbstractGate:
    """
    Abstract Gate
    """

    def __init__(self) -> None:
        pass


@dataclass
class SingleQubitGate(AbstractGate):
    """
    Class to represent single qubit gates
    All arguments are processed as strings and standard conversions will be applied. This is because the output will generated in OpenQASM

    """

    gate_name: str = None
    qubit_register: str = None
    gate_args: float = None
    num_qubit: int = 1


@dataclass
class TwoQubitGate(AbstractGate):
    """
    Class to reprensent two qubit gates.
    The first qubit is always the control
    """

    gate_name: str = None
    qubit_register: List[str] = None
    gate_args: float = None
    num_qubits: int = 2


@dataclass
class MultiQubitGate(AbstractGate):
    """
    Class to reprensent Multi gates.(>2 qubits)
    If multiple controls are present, always put them a beginning of the qubit_register
    """

    gate_name: str = None
    qubit_register: List[str] = None
    gate_args: float = None
    num_qubits: int = len(qubit_register) if not qubit_register is None else None
