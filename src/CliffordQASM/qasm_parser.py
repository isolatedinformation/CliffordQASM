# import openqasm3
from h11 import Data
from qiskit.circuit import QuantumCircuit

QuantumCircuit.from_qasm_file


class QASMParser:
    def __init__(self, filepath: str = "qasm_circuits/qft.qasm") -> None:
        with open(filepath) as f:
            self.circuit_string = self._remove_comments_from_qasm_str(f.read())

    def _remove_comments_from_qasm_str(self, s: str, strict: bool = True):
        """
        Function to break to down QASM file a list of strings of each line of the file
        """
        lines = s.splitlines()
        r = []
        # remove comments
        for s in lines:
            if s.find("//") != -1:
                t = s[0 : s.find("//")].strip()
            elif s.find("*") != -1:  # remove multi line comments
                t = False
            else:
                t = s.strip()
            if t:
                r.append(t)

        print(r[0])
        if r[0].startswith("OPENQASM"):
            r.pop(0)
        elif strict:
            raise TypeError("File does not start with OPENQASM descriptor")

        if r[0].startswith('include "stdgates.inc";'):
            r.pop(0)
        elif strict:
            raise TypeError("File is not importing standard library")

        return r

    def _parse_standard_gates(self):
        """
        Internal method to gates that are available in `stdgates.inc`
        """
        pass

    def _parse_custom_gate(self):
        """
        Internal method to parse gates that are created by the user.
        """
        pass

    @staticmethod
    def parse(self):
        pass


# def parse_custom_gate():
# # print(parse(circuit_string))
