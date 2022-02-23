from dataclasses import dataclass


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


@dataclass
class TwoQubitGate(AbstractGate):
    gate_name: str = None
    qubit_register: str = None
    gate_args: str = None
