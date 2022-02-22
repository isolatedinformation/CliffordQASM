import subprocess
import numpy as np


def generate_clifford_T_approximation_from_rz_gate(angle: float):
    n = angle / np.pi
    phase_gate_angle = f"pi/{n}"
    command_output = subprocess.check_output(f"gridsynth {phase_gate_angle}", shell=True).decode(
        "utf-8"
    )
    clifford_sequence = command_output.replace("W", "")  # drop the global phase
    clifford_sequence = clifford_sequence[::-1]  # reverse to go from operator to circuit form

    return clifford_sequence
