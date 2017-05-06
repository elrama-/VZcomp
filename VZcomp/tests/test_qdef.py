import numpy as np
from unittest import TestCase

import VZcomp.qdef as qdef


class Quantum_definitions(TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_pauli_matrices(self):

        XX = np.real(np.dot(qdef.X, qdef.X))
        YY = np.real(np.dot(qdef.Y, qdef.Y))
        ZZ = np.real(np.dot(qdef.Z, qdef.Z))

        self.assertAlmostEqual(np.real_if_close(XX[0, 0]), 1)
        self.assertAlmostEqual(np.real_if_close(XX[0, 1]), 0)
        self.assertAlmostEqual(np.real_if_close(XX[1, 0]), 0)
        self.assertAlmostEqual(np.real_if_close(XX[1, 1]), 1)

        self.assertAlmostEqual(np.real_if_close(YY[0, 0]), 1)
        self.assertAlmostEqual(np.real_if_close(YY[0, 1]), 0)
        self.assertAlmostEqual(np.real_if_close(YY[1, 0]), 0)
        self.assertAlmostEqual(np.real_if_close(YY[1, 1]), 1)

        self.assertAlmostEqual(np.real_if_close(ZZ[0, 0]), 1)
        self.assertAlmostEqual(np.real_if_close(ZZ[0, 1]), 0)
        self.assertAlmostEqual(np.real_if_close(ZZ[1, 0]), 0)
        self.assertAlmostEqual(np.real_if_close(ZZ[1, 1]), 1)

    def test_rotation_matrix(self):

        I_0axis = qdef.qrot2mat([0, 0, 0], np.pi)

        I_0angle = qdef.qrot2mat([123, 213, 23], 0.)

        X180 = qdef.qrot2mat([1, 0, 0], np.pi)

        Y180 = qdef.qrot2mat([0, 1, 0], np.pi)

        Z180 = qdef.qrot2mat([0, 0, 1], np.pi)

        # include checks versus ideal.
