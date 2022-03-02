from dataclasses import dataclass
from typing import List

# TODO: Strength of truncation of string while using f-strings
# Q: Would it better to use Fractions instead of floats for arbitrary precision?


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
    qubit_register: List[str] = None
    gate_args: float = None  # represents the denominator of the angle pi/gate_args
    num_qubits: int = 1

    def to_qasm(self):
        if self.gate_args is not None:
            return f"{self.gate_name}({self.gate_args}) {self.qubit_register[0]};"
        return f"{self.gate_name} {self.qubit_register[0]};"


@dataclass
class TwoQubitGate(AbstractGate):
    """
    Class to reprensent two qubit gates.
    The first qubit is always the control
    """

    gate_name: str = None
    qubit_register: List[str] = None
    gate_args: List[float] = None
    num_qubits: int = 2

    def to_qasm(self):
        if self.gate_args is not None:
            args = ""
            for arg in self.gate_args:
                args.append(f"{arg}, ")
            return (
                f"{self.gate_name}({args[:-2]}) {self.qubit_register[0]}, {self.qubit_register[1]};"
            )
        return f"{self.gate_name} {self.qubit_register[0]}, {self.qubit_register[1]};"


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

    def to_qasm(self):
        qubits = ""
        for qubit in self.qubit_register:
            qubits.append(f"{qubit}, ")

        if self.gate_args is not None:
            args = ""
            for arg in self.gate_args:
                args.append(f"{arg}, ")
            return f"{self.gate_name}({args[:-2]}) {qubits[:-2]}"
        return f"{self.gate_name} {qubits[:-2]};"
