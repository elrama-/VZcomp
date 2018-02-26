import numpy as np
from unittest import TestCase
import VZcomp
from VZcomp import compile_module as cp
from VZcomp import utils as utils


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
        code_rotations = cp.structured2rotlist(code_struct)
        self.assertAlmostEqual(code_rotations.n_qubits, 2)
        self.assertAlmostEqual(code_rotations.depth, 3)
        self.assertAlmostEqual(code_rotations.lines_2Q[0], 'CZ q0,q1')
        self.assertAlmostEqual(len(code_rotations.rotations_1Q[0, 0, :]), 4)
        self.assertAlmostEqual(len(code_rotations.rotations_1Q[0, :, 0]), 2)
        self.assertAlmostEqual(len(code_rotations.rotations_1Q[:, 0, 0]), 2)

        rounded_rots = np.round(code_rotations.rotations_1Q, 3)
        self.assertAlmostEqual(rounded_rots[0, 0, 0], 0)
        self.assertAlmostEqual(rounded_rots[0, 0, 1], 1)
        self.assertAlmostEqual(rounded_rots[0, 0, 2], 0)
        self.assertAlmostEqual(rounded_rots[0, 0, 3], 1.571)
        self.assertAlmostEqual(rounded_rots[0, 1, 0], 0)
        self.assertAlmostEqual(rounded_rots[0, 1, 1], 1)
        self.assertAlmostEqual(rounded_rots[0, 1, 2], 0)
        self.assertAlmostEqual(rounded_rots[0, 1, 3], 1.571)
        self.assertAlmostEqual(rounded_rots[1, 0, 0], 0)
        self.assertAlmostEqual(rounded_rots[1, 0, 1], 1)
        self.assertAlmostEqual(rounded_rots[1, 0, 2], 0)
        self.assertAlmostEqual(rounded_rots[1, 0, 3], 1.571)
        self.assertAlmostEqual(rounded_rots[1, 1, 0], 0)
        self.assertAlmostEqual(rounded_rots[1, 1, 1], 0)
        self.assertAlmostEqual(rounded_rots[1, 1, 2], 0)
        self.assertAlmostEqual(rounded_rots[1, 1, 3], 0)

    def test_rotlist2euler(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        code_qasm = cp.file2qasm(bell_file, 2)
        code_struct = cp.qasm2struct(code_qasm)
        code_rotations = cp.structured2rotlist(code_struct)
        code_euler = cp.rotlist2euler(code_rotations)

        self.assertAlmostEqual(code_euler.n_qubits, 2)
        self.assertAlmostEqual(code_euler.depth, 3)
        self.assertAlmostEqual(code_euler.lines_2Q[0], 'CZ q0,q1')
        self.assertAlmostEqual(len(code_euler.euler_1Q[0, 0, :]), 3)
        self.assertAlmostEqual(len(code_euler.euler_1Q[0, :, 0]), 2)
        self.assertAlmostEqual(len(code_euler.euler_1Q[:, 0, 0]), 2)

        rounded_euler = np.round(code_euler.euler_1Q, 3)
        self.assertAlmostEqual(rounded_euler[0, 0, 0], -1.571)
        self.assertAlmostEqual(rounded_euler[0, 0, 1], 1.571)
        self.assertAlmostEqual(rounded_euler[0, 0, 2], 1.571)
        self.assertAlmostEqual(rounded_euler[0, 1, 0], -1.571)
        self.assertAlmostEqual(rounded_euler[0, 1, 1], 1.571)
        self.assertAlmostEqual(rounded_euler[0, 1, 2], 1.571)
        self.assertAlmostEqual(rounded_euler[1, 0, 0], -1.571)
        self.assertAlmostEqual(rounded_euler[1, 0, 1], 1.571)
        self.assertAlmostEqual(rounded_euler[1, 0, 2], 1.571)
        self.assertAlmostEqual(rounded_euler[1, 1, 0], 0)
        self.assertAlmostEqual(rounded_euler[1, 1, 1], 0)
        self.assertAlmostEqual(rounded_euler[1, 1, 2], 0)

    def test_euler2xy(self):
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        code_qasm = cp.file2qasm(bell_file, 2)
        code_struct = cp.qasm2struct(code_qasm)
        code_rotations = cp.structured2rotlist(code_struct)
        code_euler = cp.rotlist2euler(code_rotations)
        code_xy = cp.euler2xy(code_euler)

        self.assertAlmostEqual(code_xy.n_qubits, 2)
        self.assertAlmostEqual(code_xy.depth, 3)
        self.assertAlmostEqual(code_xy.lines_2Q[0], 'CZ q0,q1')
        self.assertAlmostEqual(len(code_xy.XY_rotations[0, 0, :]), 2)
        self.assertAlmostEqual(len(code_xy.XY_rotations[0, :, 0]), 2)
        self.assertAlmostEqual(len(code_xy.XY_rotations[:, 0, 0]), 2)

        rounded_xy = np.round(code_xy.XY_rotations, 3)
        self.assertAlmostEqual(rounded_xy[0, 0, 0], -1.571)
        self.assertAlmostEqual(rounded_xy[0, 0, 1], 1.571)
        self.assertAlmostEqual(rounded_xy[0, 1, 0], -1.571)
        self.assertAlmostEqual(rounded_xy[0, 1, 1], 1.571)
        self.assertAlmostEqual(rounded_xy[1, 0, 0], 1.571)
        self.assertAlmostEqual(rounded_xy[1, 0, 1], 1.571)
        self.assertAlmostEqual(rounded_xy[1, 1, 0], 3.142)
        self.assertAlmostEqual(rounded_xy[1, 1, 1], 0)

    def test_print2file_funcs(self):
        def files_different(basename):
            lines_A = utils.list_from_file(basename)
            lines_B = utils.list_from_file(basename+'_test')
            dif_lines = 0
            for i in range(len(lines_A)):
                if not (lines_A[i] == lines_B[i]):
                    dif_lines += 1
            return bool(dif_lines)
        bell_file = VZcomp.__path__[0]+'/tests/files/bell_state.qasm'
        basename = VZcomp.__path__[0]+'/tests/files/bell_state'
        code_qasm = cp.file2qasm(bell_file, 2)
        code_struct = cp.qasm2struct(code_qasm)
        code_rotations = cp.structured2rotlist(code_struct)
        code_euler = cp.rotlist2euler(code_rotations)
        code_xy = cp.euler2xy(code_euler)

        su2_file = (basename+'.su2').replace(chr(92), chr(47))
        szxz_file = (basename+'.szxz').replace(chr(92), chr(47))
        mw_file = (basename+'.mw').replace(chr(92), chr(47))
        code_rotations.print_to_file(su2_file+'_test')
        code_euler.print_to_file(szxz_file+'_test')
        code_xy.print_to_file(mw_file+'_test')

        self.assertAlmostEqual(files_different(su2_file), False)
        self.assertAlmostEqual(files_different(szxz_file), False)
        self.assertAlmostEqual(files_different(mw_file), False)

        try:
            os.remove(su2_file+'_test')
            os.remove(szxz_file+'_test')
            os.remove(mw_file+'_test')
        except:
            print('Test-files removal could not be done. Do you have that user-level?')
