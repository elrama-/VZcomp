import numpy as np
import os
from unittest import TestCase
import VZcomp.utils as utils
import VZcomp
from VZcomp import compile_module as cp

class Quantum_definitions(TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_file2qasm(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        code_qasm = cp.file2qasm(bell_file, 2)
        self.assertAlmostEqual(code_qasm.lines[0], 'Y90 q0')
        self.assertAlmostEqual(code_qasm.lines[1], 'Y90 q1')
        self.assertAlmostEqual(code_qasm.lines[2], 'CZ q0,q1')
        self.assertAlmostEqual(code_qasm.lines[3], 'Y90 q0')
        self.assertAlmostEqual(code_qasm.n_qubits, 2)
        self.assertAlmostEqual(code_qasm.depth, 4)


    def test_file2struct(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        code_qasm = cp.file2qasm(bell_file, 2)
        code_struct = cp.qasm2struct(code_qasm)
        self.assertAlmostEqual(code_struct.lines_1Q[0][0], 'Y90 q0')
        self.assertAlmostEqual(code_struct.lines_1Q[0][1], 'Y90 q1')
        self.assertAlmostEqual(code_struct.lines_2Q[0], 'CZ q0,q1')
        self.assertAlmostEqual(code_struct.lines_1Q[1][0], 'Y90 q0')
        self.assertAlmostEqual(code_struct.n_qubits, 2)
        self.assertAlmostEqual(code_struct.depth, 3)


    def test_struct2rotlist(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        code_qasm = cp.file2qasm(bell_file, 2)
        code_struct = cp.qasm2struct(code_qasm)
        code_rotations = cp.structured_to_rotlist(code_struct)
