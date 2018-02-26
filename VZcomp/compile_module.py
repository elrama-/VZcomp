import numpy as np
from VZcomp import utils
from VZcomp import representations as rep


def file2qasm(file, n_qubits):
        # read file
    lines = utils.list_from_file(file)
    # get qasm representation
    code_qasm = rep.qasm(lines=lines, n_qubits=n_qubits)
    return code_qasm


def structured_to_rotlist(code_structured):
    op_qubits = np.zeros((code_structured.n_qubits, 2, 2), dtype=np.complex)
    n_1q = int((code_structured.depth + 1) / 2)
    rot_vector = np.zeros((n_1q, code_structured.n_qubits, 4))
    for i, step in enumerate(code_structured.lines_1Q):
            # initialize the operation accumulator
        for q in range(code_structured.n_qubits):
            op_qubits[q, :, :] = np.eye(2)
        # pack qubits
        # print(step)
        for j, gate in enumerate(step):
            # print(gate)
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
    return code_rotations
