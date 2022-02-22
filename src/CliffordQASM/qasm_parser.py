# import openqasm3


class QASMParser:
    def __init__(self, filepath: str) -> None:
        with open("qasm_circuits/adder.qasm") as f:
            self.circuit_string = f.read()

    @staticmethod
    def parse(s: str, strict: bool = True):
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

        data = "\n".join(r)
        return data


# def parse_custom_gate():
# # print(parse(circuit_string))
