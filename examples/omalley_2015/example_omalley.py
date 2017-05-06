'''
Done up to structured_code stage
'''

from imp import reload
import numpy as np
from xy_compiler import utils
from xy_compiler import representations as rep
# read file
lines = utils.list_from_file('omalley.qasm')
# get qumis representation
code_qumis = rep.qumis(lines=lines, n_qubits=2)
# transform to structured
utils.split_entangling(code_qumis.lines)
list1Q, list2Q = utils.split_entangling(code_qumis.lines)
# get structured representation
code_structured = rep.structured_script(lines_1Q=list1Q,
                                        lines_2Q=list2Q,
                                        n_qubits=code_qumis.n_qubits)

# transform into rotations representation
op_qubits = np.zeros((code_structured.n_qubits, 2, 2), dtype=np.complex)
packed_lines_1Q = []
n_1q = int((code_structured.depth + 1) / 2)
rot_vector = np.zeros((n_1q, code_structured.n_qubits, 4))
for i, step in enumerate(code_structured.lines_1Q):
        # initialize the operation accumulator
    for q in range(code_structured.n_qubits):
        op_qubits[q, :, :] = np.eye(2)
    # pack qubits
    for j, gate in enumerate(step):
        gate_op = utils.op2matrix(gate)
        # multiply
        for q in range(code_structured.n_qubits):
            digits = int(np.floor(np.log10(q)+1) if q > 0 else 1)
            q_label = 'q%d' % q
            if q_label == gate[-(digits+1):]:
                op_qubits[q, :, :] = np.dot(gate_op, op_qubits[q, :, :])
    # now get the rotation parameter for every operation
    for q in range(code_structured.n_qubits):
        axis, angle = utils.qdef.mat2qrot(op_qubits[q, :, :])
        rot_vector[i, q, :3] = axis
        rot_vector[i, q, 3] = angle

# get rotations representation
code_rotations = rep.rotation_list(rotations_1Q=rot_vector,
                                   lines_2Q=code_structured.lines_2Q,
                                   n_qubits=code_structured.n_qubits)

# decompose in euler angles
n_1q = int((code_rotations.depth + 1) / 2)
szxz_vector = np.zeros((n_1q, code_structured.n_qubits, 3))
for i in range(n_1q):
    for q in range(code_rotations.n_qubits):
        axis, angle = code_rotations.rotations_1Q[
            i, q, :3], code_rotations.rotations_1Q[i, q, 3]
        if np.isclose(axis, [0, 0, 0]).all() and np.isclose(angle, 0):
            szxz_vector[i, q, :] = 0, 0, 0
        else:
            szxz_vector[i, q, :] = utils.rot2szxz(axis, angle)

# create euler object
code_euler = rep.euler_list(euler_1Q=szxz_vector,
                            lines_2Q=code_rotations.lines_2Q,
                            n_qubits=code_rotations.n_qubits)

# compile
n_1q = int((code_euler.depth + 1) / 2)
xy_vector = np.zeros((n_1q, code_euler.n_qubits, 2))
for q in range(code_euler.n_qubits):
    alpha_remaining = 0.
    for i in range(n_1q):
	    z1, x, z2 = code_euler.euler_1Q[i, q, :3]
	    prev_z_angle = z1+alpha_remaining
	    xy_vector[i, q, :] = utils.update_frame(prev_z_angle), x
	    alpha_remaining = z2 - prev_z_angle

# create XY object
code_XY = rep.XYcompiled_list(XY_rotations=xy_vector,
                              lines_2Q=code_euler.lines_2Q,
                              n_qubits=code_euler.n_qubits)
