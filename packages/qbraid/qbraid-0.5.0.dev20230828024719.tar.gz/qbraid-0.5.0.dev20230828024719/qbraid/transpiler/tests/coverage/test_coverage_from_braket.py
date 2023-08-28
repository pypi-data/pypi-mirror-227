# Copyright (C) 2023 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Benchmarking tests for braket conversions

"""
import braket
import pytest

import qbraid
from qbraid.interface.qbraid_braket.gates import get_braket_gates

TARGETS = [("cirq", 1.0), ("pyquil", 1.0), ("pytket", 1.0), ("qiskit", 1.0)]
braket_gates = get_braket_gates(seed=0)


def convert_from_braket_to_x(target, gate_name):
    gate = braket_gates[gate_name]

    if gate.qubit_count == 1:
        source_circuit = braket.circuits.Circuit([braket.circuits.Instruction(gate, 0)])
    else:
        source_circuit = braket.circuits.Circuit(
            [braket.circuits.Instruction(gate, range(gate.qubit_count))]
        )

    target_circuit = qbraid.circuit_wrapper(source_circuit).transpile(target)
    assert qbraid.interface.circuits_allclose(source_circuit, target_circuit, strict_gphase=False)


@pytest.mark.parametrize(("target", "baseline"), TARGETS)
def test_braket_coverage(target, baseline):
    ACCURACY_BASELINE = baseline
    ALLOWANCE = 0.01
    failures = {}
    for gate_name in braket_gates:
        try:
            convert_from_braket_to_x(target, gate_name)
        except Exception as e:
            failures[f"{target}-{gate_name}"] = e

    total_tests = len(braket_gates)
    nb_fails = len(failures)
    nb_passes = total_tests - nb_fails
    accuracy = float(nb_passes) / float(total_tests)

    assert (
        nb_passes >= ACCURACY_BASELINE - ALLOWANCE
    ), f"The coverage threshold was not met. {nb_fails}/{total_tests} tests failed ({nb_fails / (total_tests):.2%}) and {nb_passes}/{total_tests} passed (expected >= {ACCURACY_BASELINE}).\nFailures: {failures.keys()}\n\n"
