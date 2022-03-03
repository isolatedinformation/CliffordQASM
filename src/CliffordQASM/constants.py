from typing import Dict, List, Tuple, Union

ROTATION_GATES_T0_Z_BASIS: Dict[str, List[str]] = {
    "rx": ["h", "rz", "h"],
    "ry": ["s", "h", "rz", "h", "sdg"],
    "rz": ["rz"],
    "p": ["gphase", "rz"],
}

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

CH_TO_CLIFFORDT = (
    ("s", 1),
    ("h", 1),
    ("t", 1),
    ("cx", [0, 1]),
    ("tdg", 1),
    ("h", 1),
    ("sdg", 1),
)  # approx decomp Eq 54 of https://threeplusone.com/pubs/on_gates.pdf

SINGLE_QUBIT_CLIFFORDT_BASIS: Tuple = ("id", "x", "y", "z", "h", "s", "sdg", "t")
TWO_QUBIT_CLIFFORDT_BASIS: Tuple = ("cx", "cy", "cz", "swap")
GATES_THAT_CAN_BE_CONVERTED: Tuple = ("rx", "ry", "rz", "ccx", "p", "ch")
GATES_NOT_SUPPORTED: Tuple = ["U", "cswap", "cu", "crx", "cry", "crz", "cphase"]
