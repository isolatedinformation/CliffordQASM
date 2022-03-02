from email import generator
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
GATES_TO_CONVERT = ["rx(", "ry(", "rz(", "ccx "]
GATES_NOT_SUPPORTED = [
    "p(",
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
        self.fp = "cliffordT_qasm_circuits/" + "cliffordT_" + filepath[filepath.find("/") + 1 :]
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
                t = s  # .strip()  # .strip() removing the strip operator so as to maintain identantion levels
            if t:
                r.append(t)

        print(r[0])
        if r[0].startswith("OPENQASM"):
            pass
            # r.pop(0)
        elif strict:
            raise TypeError("File does not start with OPENQASM descriptor")

        if r[1].startswith('include "stdgates.inc";'):
            pass
            # r.pop(0)
        elif strict:
            raise TypeError("File is not importing standard library")  # TODO: remove these pops

        return r

    def generate_cliffordTCircuit(self):
        new_circuit = list()
        index = 0

        while index < len(self.circuit_string):
            current_instruction = self.circuit_string[index]

            non_clifford = list(
                filter(lambda nc_gate: nc_gate in current_instruction, GATES_TO_CONVERT)
            )

            if non_clifford:
                gate_start_index = current_instruction.find(*non_clifford)
                gate_end_index = current_instruction.find(";")
                generator = CliffordInstructionGenerator(
                    current_instruction[gate_start_index:gate_end_index]
                )
                cliffordised_instructions = generator._get_qasm_instructions()
                if len(current_instruction) == gate_end_index + 1:
                    for ins in cliffordised_instructions:
                        new_circuit.append(current_instruction[:gate_start_index] + ins)
                elif (
                    len(current_instruction) > gate_end_index + 1
                    and current_instruction[gate_end_index + 1 :].isspace()
                ):
                    for ins in cliffordised_instructions:
                        new_circuit.append(current_instruction[:gate_start_index] + ins)
                else:
                    new_circuit.append(current_instruction[:gate_start_index])
                    for ins in cliffordised_instructions:
                        new_circuit.append(f"\t{ins}")
                    new_circuit.append("}")

                index += 1
            else:
                new_circuit.append(current_instruction)
                index += 1

        return new_circuit

    def cliffordT_qasm_output_string(self):
        space = "\n"
        qasm_output = space.join(self.generate_cliffordTCircuit())
        return qasm_output

    def generate_cliffordT_qasm_file(self):
        with open(self.fp, "w") as file:
            file.write(self.cliffordT_qasm_output_string())
