import numpy as np
from unittest import TestCase
import os
import VZcomp.utils as utils
import VZcomp


class Utils(TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_list_from_file(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        lines = utils.list_from_file(bell_file.replace(chr(47), chr(92)))
        self.assertAlmostEqual(lines[0], 'Y90 q0')
        self.assertAlmostEqual(lines[1], 'Y90 q1')
        self.assertAlmostEqual(lines[2], 'CZ q0,q1')
        self.assertAlmostEqual(lines[3], 'Y90 q0')

    def test_split_entangling(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        lines = utils.list_from_file(bell_file.replace(chr(47), chr(92)))
        list_1Q, list_2Q = utils.split_entangling(lines)
        # print(list_1Q,list_2Q)
        self.assertAlmostEqual(list_1Q[0], ['Y90 q0', 'Y90 q1'])
        self.assertAlmostEqual(list_1Q[1], ['Y90 q0'])
        self.assertAlmostEqual(list_2Q[0], 'CZ q0,q1')

    def test_op2matrix(self):
        X90 = utils.op2matrix('X 90')
        X90_r = np.round(X90, 3)
        self.assertAlmostEqual(X90_r[0, 0], 0.707)
        self.assertAlmostEqual(X90_r[0, 1], -0.707j)
        self.assertAlmostEqual(X90_r[1, 0], -0.707j)
        self.assertAlmostEqual(X90_r[1, 1], 0.707)

        X = utils.op2matrix('X')
        X_r = np.round(X, 3)
        self.assertAlmostEqual(X_r[0, 0], 0)
        self.assertAlmostEqual(X_r[0, 1], -1j)
        self.assertAlmostEqual(X_r[1, 0], -1j)
        self.assertAlmostEqual(X_r[1, 1], 0)

        Y = utils.op2matrix('Y')
        Y_r = np.round(Y, 3)
        self.assertAlmostEqual(X_r[0, 0], Y_r[0, 0])
        self.assertAlmostEqual(X_r[0, 1], Y_r[0, 1])
        self.assertAlmostEqual(X_r[1, 0], Y_r[1, 0])
        self.assertAlmostEqual(X_r[1, 1], Y_r[1, 1])

        Z = utils.op2matrix('Z')
        Z_r = np.round(Z, 3)
        self.assertAlmostEqual(X_r[0, 0], Z_r[0, 0])
        self.assertAlmostEqual(X_r[0, 1], Z_r[0, 1])
        self.assertAlmostEqual(X_r[1, 0], Z_r[1, 0])
        self.assertAlmostEqual(X_r[1, 1], Z_r[1, 1])

        H = utils.op2matrix('H')
        H_r = np.round(H, 3)
        self.assertAlmostEqual(H_r[0, 0], -0.707j)
        self.assertAlmostEqual(H_r[0, 1], -0.707j)
        self.assertAlmostEqual(H_r[1, 0], -0.707j)
        self.assertAlmostEqual(H_r[1, 1], 0.707j)

        T = utils.op2matrix('T')
        T_r = np.round(T, 3)
        self.assertAlmostEqual(T_r[0, 0], 0.924-0.383j)
        self.assertAlmostEqual(T_r[0, 1], 0)
        self.assertAlmostEqual(T_r[1, 0], 0)
        self.assertAlmostEqual(T_r[1, 1], 0.924+0.383j)

        I = utils.op2matrix('I')
        I_r = np.round(I, 3)
        self.assertAlmostEqual(I_r[0, 0], 1)
        self.assertAlmostEqual(I_r[0, 1], 0)
        self.assertAlmostEqual(I_r[1, 0], 0)
        self.assertAlmostEqual(I_r[1, 1], 1)