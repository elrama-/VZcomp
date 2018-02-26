import numpy as np
import os
from unittest import TestCase
import VZcomp.utils as utils
import VZcomp
from subprocess import call
from VZcomp import representations as rep
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

"""
    def test_file2qasm(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        lines = utils.list_from_file(bell_file.replace(chr(92), chr(47)))
        code_qasm = rep.qasm(lines=lines, n_qubits=2)
        list1Q, list2Q = utils.split_entangling(code_qasm.lines)


    def test_struct2rotlist(self):
"""