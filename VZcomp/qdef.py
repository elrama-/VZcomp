import numpy as np
I = np.eye(2)
X = np.array([[0, 1], [1, 0]], dtype=np.complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex)


def qrot2mat(vector, angle):
    vector_norm = np.sum(np.abs(vector)**2)
    if not np.isclose(vector_norm, 1):
        vector = vector / vector_norm
    if angle == 0 or np.isclose(vector, [0, 0, 0]).all():
        rot_matrix = I
    else:
        pauli_vec = vector[0]*X+vector[1]*Y+vector[2]*Z
        rot_matrix = np.cos(0.5*angle)*I-1j*np.sin(0.5*angle)*pauli_vec
    return rot_matrix


def mat2qrot(matrix):
    if np.isclose(matrix, np.eye(2)).all():
        nx, ny, nz = 0, 0, 0
        theta = 0
    else:
        c_I = np.trace(np.dot(I, matrix))
        c_X = np.trace(np.dot(X, matrix))
        c_Y = np.trace(np.dot(Y, matrix))
        c_Z = np.trace(np.dot(Z, matrix))
        # print(c_I, c_X, c_Y, c_Z)
        norm_vec = np.sqrt(c_X**2 + c_Y**2 + c_Z**2)
        # print(norm_vec,c_I)
        theta = np.arccos(-1j*c_I/norm_vec)*0.5
        theta = np.real_if_close(theta)
        # print(theta)
        # print(c_I,c_X,c_Y,c_Z)
        if (theta % np.pi) != 0.:
            nx = 1j*c_X/np.sin(theta)
            ny = 1j*c_Y/np.sin(theta)
            nz = 1j*c_Z/np.sin(theta)
        else:
            nx, ny, nz = c_X, c_Y, c_Z
        norm = np.sqrt(nx*nx+ny*ny+nz*nz)
        # print('theta,norm,v')
        # print(theta,norm,nx,ny,nz)
        nx /= norm
        ny /= norm
        nz /= norm
        # print(np.real([nx, ny, nz]))
    return np.real([nx, ny, nz]), theta
