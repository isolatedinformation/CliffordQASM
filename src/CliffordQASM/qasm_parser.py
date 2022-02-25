from CliffordQASM.cliffordT_converter import CliffordInstructionGenerator

# Constant for the list of gates supported
IGNORED_INSTRUCTIONS = ["qubit", "bit", "reset", "barrier", "measure"]
IS_CLIFFORDT = [
    "x ",
    "y ",
    "z ",
    "h ",
    "s ",
    "sdg ",
    "t ",
    "tdg ",
    "sx ",
    "cx ",
    "cy ",
    "cz ",
    "swap ",
]
GATES_TO_CONVERT = ["rx(", "ry(", "rz(", "ccx ", "p("]
GATES_NOT_SUPPORTED = [
    "U",  # can be broken down into Clifford Gates
    "ch",  # not in CLifford
    "cswap",  # not in Clifford
    "cu",
    "crx",
    "cry",
    "crz",
    "cphase",  # Controlled phase gate
]


class QASMParser:
    """
    Class to Parse a QASM Circuit generating a circuit as a list of gate lines
    """

    def __init__(self, filepath: str = "../../qasm_circuits/qft.qasm") -> None:
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
                t = s[
                    0 : s.find("//")
                ]  # .strip() removing the strip operator so as to maintain identantion levels
            elif s.find("*") != -1:  # remove multi line comments
                t = False
            else:
                t = (
                    s.strip()
                )  # .strip() removing the strip operator so as to maintain identantion levels
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

        return r  # TODO: Detemine best data structure to represent this.

    def generate_cliffordTCircuit(self):
        new_circuit = list()
        flag = False

        index = 0
        while index < len(self.circuit_string):

            if any(non_cliff in self.circuit_string[index] for non_cliff in GATES_TO_CONVERT):
                # Condition to process supported gates that can be converted to the Clifford basis
                new_lines = CliffordInstructionGenerator(self.circuit_string[index])
                new_circuit.extend(new_lines)
                index += 1

            elif self.circuit_string[index].startswith("gate"):
                # Parse custom gates and convert gates in the definition to Clifford+T basis
                new_lines, new_index = self._parse_custom_gate(index)
                new_circuit.append(self.circuit_string[index])

            elif flag:
                if "}" in self.circuit_string[index]:
                    flag = False
                new_circuit.append(self.circuit_string[index])
            else:
                new_circuit.append(self.circuit_string[index])

            # elif any(ignored in line for ignored in ignored_instructions):
            #     new_circuit.append(line)

            # elif any(line.startswith(cliff) for cliff in is_cliffordT):
            #     new_circuit.append(line)

    def _parse_custom_gate(self, index):
        custom_gate_as_clifford = list()
        while "}" not in self.circuit_string[index]:  # Write string
            # TODO: get instruction and change it to a multi line gate definition
            new_lines = CliffordInstructionGenerator(
                self.circuit_string[index]
            )  # make statement that generate line for this
            custom_gate_as_clifford.extend(new_lines)
            index += 1


# string.startswith(gate_name) is not a good check because the control flow statements
# might make the gates start indented or deep in the string in case of single line for loops
# the last check in generate_cliffordTCircuit might be useless. Find out what is required.
# the flag check might also be irrelvant
# are we also breaking down custom gates to clifford operations
# would it make more sense loop with an index instead of an iterable.
