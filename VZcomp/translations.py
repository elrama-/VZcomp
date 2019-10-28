import numpy as np
from transforms3d import euler
from VZcomp import representations as rep

#Define Pauli operators
I = np.eye(2)
X = np.array([[0, 1], [1, 0]], dtype=np.complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex)

def list_from_file(filepath):
    '''
    Inputs filepath and returns contents in a list.
    '''
    lines = [line.rstrip('\n') for line in open(filepath)]
    return lines

def set_parameters(qasm_list,gamma_1,gamma_2,alpha_1,alpha_2):
    '''
    Sets parameters as string from QASM list to input angle as string. 
    '''
    new_qasm_list=[]
    for line in qasm_list:    
        if '90+gamma1' in line:
            new_gamma1=str(90+gamma_1)
            new_line=line.replace('90+gamma1',new_gamma1)
            new_qasm_list.append(new_line)
        elif 'gamma1' in line:
            new_line=line.replace('gamma1',str(gamma_1))
            new_qasm_list.append(new_line)
        elif '-gamma2' in line:
            new_line=line.replace('-gamma2',str(-gamma_2))
            new_qasm_list.append(new_line)
        elif 'alpha1' in line:
            new_line=line.replace('alpha1',str(alpha_1))
            new_qasm_list.append(new_line)
        elif '-alpha2' in line:
            new_line=line.replace('-alpha2',str(-alpha_2))
            new_qasm_list.append(new_line)
        else:
            new_qasm_list.append(line)
    return new_qasm_list 


def qasm_list_deg2rad(qasm_list):
    '''
    Sets a Qasm list from degree to radians. Necessary when one requires to get the correct density matrix in qsoverlay. 
    '''
    
    qasm_rad_list=[]
    for line in qasm_list:
        line = line.split(' ')
        if len(line)==3:
            line[2]=str(np.deg2rad(float(line[2])))
        if len(line)==4:
            line[2]=str(np.deg2rad(float(line[2])))
            line[3]=str(np.deg2rad(float(line[3])))
        line_new=' '.join(line)
        qasm_rad_list.append(line_new)
    return qasm_rad_list


def split_entangling(script):
    '''
    Splits a QASM script into stages of 1Q gates and 2Q CPhase gates. 
    Sequential 2Q gates are seperated by ';' which is used to seperate them later on. 
    '''
    list_1Q = []
    list_2Q = []
    accum_1Q = []
    for i in range(len(script)):
        line = script[i]
        if line[:6] == 'CPhase':
            if accum_1Q == [] and list_2Q == []:
                list_2Q.append(line)
            elif accum_1Q == [] and list_2Q != []:
                list_2Q[-1] += ';' + line
            else:
                list_2Q.append(line)
                list_1Q.append(accum_1Q)
                accum_1Q = []
        else:
            accum_1Q.append(line)
    list_1Q.append(accum_1Q)
    return list_1Q, list_2Q

def list2qasm(list_for_qasm):
    '''
    Inputs a list of gates and seperates CPhases.
    '''
    step_list=[]
    for i,step in enumerate(list_for_qasm):
        if ';' in step:
            step_new=step.split(';')
            del list_for_qasm[i]
            list_for_qasm.insert(i,step_new[0])
            list_for_qasm.insert(i+1,step_new[1])
    return list_for_qasm



def qrot2mat(vector, angle):
    '''
    Inputs Pauli vector and rotation angle and returns a 2x2 rotation matrix
    '''
    vector_norm = np.dot(vector,np.conjugate(vector))
    if not np.isclose(vector_norm, 1):
        vector = vector / vector_norm
    pauli_vec = vector[0]*X+vector[1]*Y+vector[2]*Z
    rot_matrix = np.cos(angle/2)*I-1j*np.sin(angle/2)*pauli_vec
    return rot_matrix


def op2matrix(op_string):
    '''
    Produces a 3D rotation matrix from a gate string
    Inputs:
            op_string (str): gate within {X,Y,Z,H,T}.
                             For X,Y,Z angles are admited in deg like X q0 180.
    '''
    op_string = op_string.split(' ')
    axis_str = op_string[0]
    if (len(op_string) == 3):
        angle = float(op_string[2])
    elif (len(op_string) == 4):
        phi,theta = float(op_string[2]),float(op_string[3])
    elif (len(op_string) == 5):
        phi,theta,lamda = float(op_string[2]),float(op_string[3]),float(op_string[4])
    else:
        angle = 180
    if axis_str == 'X' or axis_str=='Rx':
        axis_vec = [1, 0, 0]
        angle = angle * np.pi/180.
    elif axis_str == 'Y' or axis_str=='Ry':
        axis_vec = [0, 1, 0]
        angle = angle * np.pi/180.
    elif axis_str == 'Z' or axis_str=='Rz':
        axis_vec = [0, 0, 1]
        angle = angle * np.pi/180.
    elif axis_str == 'H':
        axis_vec = [1./np.sqrt(2.), 0, 1./np.sqrt(2.)]
        angle = np.pi
    elif axis_str == 'T':
        axis_vec = [0, 0, 1]
        angle = np.pi/4.
    elif axis_str == 'I':
        axis_vec = [0, 0, 0]
        angle = 0.
    elif axis_str == 'RotateXY':
        axis_vec = [np.cos(np.deg2rad(phi)), np.sin(np.deg2rad(phi)), 0]
        angle = np.deg2rad(theta)
    elif axis_str == 'RotateEuler':
        axis_vec, angle = euler.euler2axangle(np.deg2rad(lamda),np.deg2rad(theta),np.deg2rad(phi),'szxz') 
    matrix=qrot2mat(axis_vec, angle)
    return matrix


def mat2qrot(matrix):
    '''
    Inputs 2x2 matrix and returns Pauli vector and rotation angle
    '''
    if np.isclose(matrix, np.eye(2)).all():
        nx, ny, nz = 0, 0, 0
        theta = 0
    else:
        c_I = np.trace(matrix)
        c_X = np.trace(np.dot(X, matrix))
        c_Y = np.trace(np.dot(Y, matrix))
        c_Z = np.trace(np.dot(Z, matrix))
        norm_vec = np.sqrt(np.abs(c_X**2 + c_Y**2 + c_Z**2))
        if np.real(matrix[1,0]) > 0:
            theta = 2*np.arccos(c_I/2)
        else:
            theta= -2*np.arccos(c_I/2)
        if (float(np.real_if_close(theta)) % np.pi) != 0.:
            nx = 1j*c_X/np.sin(theta/2)/2
            ny = 1j*c_Y/np.sin(theta/2)/2
            nz = 1j*c_Z/np.sin(theta/2)/2
        else:
            nx, ny, nz = c_X, c_Y, c_Z
        norm = np.sqrt(nx*nx+ny*ny+nz*nz)
        nx /= norm
        ny /= norm
        nz /= norm
    return np.real([nx, ny, nz]), np.rad2deg(np.real(theta))


def rot2szxz(rot_vector, rot_angle):
    '''
    Compiles the input rotation as ZXZ rotations.
    Inputs:
            rot_vector (float): direction for the rotation
            rot_angle (float): angle for the rotation
    Output:
            Angle Z,Angle X,Angle Z
    '''
    return euler.axangle2euler(rot_vector, rot_angle, axes='szxz')


def merge_1Q(qasmfile,gamma_1,gamma_2,alpha_1,alpha_2):
    '''
    Inputs qasm file and input parameters and returns code_euler representation.
    This function uses various representation classes.
    '''
    # read file
    lines = list_from_file(qasmfile)
    lines = set_parameters(lines,gamma_1,gamma_2,alpha_1,alpha_2)
    # get qasm representation
    code_qasm = rep.qasm(lines=lines, n_qubits=4)
    # transform to structured
    list1Q, list2Q = split_entangling(code_qasm.lines)
    # get structured representation
    code_structured = rep.structured_script(lines_1Q=list1Q,
                                            lines_2Q=list2Q,
                                            n_qubits=code_qasm.n_qubits)
    
    
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
            gate_op = op2matrix(gate)
            # multiply
            for q in range(code_structured.n_qubits):
                #digits = int(np.floor(np.log10(q)+1) if q > 0 else 1)
                digits = gate.find('q')+1
                if float(gate[digits])==q:
                    op_qubits[q, :, :] = np.dot(gate_op, op_qubits[q, :, :])
        # now get the rotation parameter for every operation
        for q in range(code_structured.n_qubits):
            axis, angle = mat2qrot(op_qubits[q, :, :])
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
            axis, angle = code_rotations.rotations_1Q[i, q, :3], np.deg2rad(code_rotations.rotations_1Q[i, q, 3])
            if np.isclose(axis, [0, 0, 0]).all() and np.isclose(angle, 0):
                szxz_vector[i, q, :] = 0, 0, 0
            else:
                szxz_vector[i, q, :] = np.rad2deg(rot2szxz(axis, angle)[::-1])
    # create euler object
    code_euler = rep.euler_list(euler_1Q=szxz_vector,
                                lines_2Q=code_rotations.lines_2Q,
                                n_qubits=code_rotations.n_qubits)
    return code_euler

def code_euler_to_list(code_euler):
    '''
    Inputs code_euler and returns list of merged Euler angles.
    '''
    new_list = []
    n_d = len(code_euler.euler_1Q[:, 0, 0])
    for i in range(n_d):
            for j in range(code_euler.n_qubits):
                line = 'RotateEuler q%d %.3f %.3f %.3f\n' % (j,
                                                         code_euler.euler_1Q[i, j, 0],
                                                         code_euler.euler_1Q[i, j, 1],
                                                         code_euler.euler_1Q[i, j, 2])
                new_list.append(line)
            if i+1 < n_d:
                new_list.append(code_euler.lines_2Q[i]+'\n')
    return new_list 
        
def euler2ZXZ(code_euler):
    '''
    Inputs code_euler and returns a list of ZXZ gates.
    '''
    ZXZ_list=[]
    n_d = len(code_euler.euler_1Q[:, 0, 0])
    for i in range(n_d):
        for j in range(code_euler.n_qubits):
            z2, x, z1 = code_euler.euler_1Q[i, j, :3]
            line_z1 = 'RotateZ q%d %.3f' % (j, z1)
            line_x = 'RotateX q%d %.3f' % (j,x)
            line_z2 = 'RotateZ q%d %.3f' % (j,z2)
            ZXZ_list.append(line_z1)
            ZXZ_list.append(line_x)
            ZXZ_list.append(line_z2)
        if i+1 < n_d:
            ZXZ_list.append(code_euler.lines_2Q[i])
    return ZXZ_list

def euler2ZXZZ(code_euler):
    '''
    Inputs code_euler and returns a list of ZXZZ gates,
    so the angle of the first Z gate is negative to the angle of the second Z gate and the third Z gate is residual.
    '''
    ZXZZ_list=[]
    n_d = len(code_euler.euler_1Q[:, 0, 0])
    for i in range(n_d):
        for j in range(code_euler.n_qubits):
            z2, x, z1 = code_euler.euler_1Q[i, j, :3]
            alpha = z2+z1
            z2 = -z1
            line_z1 = 'RotateZ q%d %.3f' % (j, z1)
            line_x = 'RotateX q%d %.3f' % (j, x)
            line_z2 = 'RotateZ q%d %.3f' % (j, z2)
            line_alpha = 'RotateZ q%d %.3f' % (j, alpha)
            ZXZZ_list.append(line_z1)
            ZXZZ_list.append(line_x)
            ZXZZ_list.append(line_z2)
            ZXZZ_list.append(line_alpha)
        if i+1 < n_d:
            ZXZZ_list.append(code_euler.lines_2Q[i])
    return ZXZZ_list


def compile_euler(code_euler):
    '''
    Inputs code_euler, propagates residual Z gates to the end of the circuit and
    returns a list of ZXZ gates with residual Z gates at the end.  
    '''
    compiled_list=[]
    alpha=np.zeros(code_euler.n_qubits)
    n_d = len(code_euler.euler_1Q[:, 0, 0])
    for i in range(n_d):
        for j in range(code_euler.n_qubits):
            z2, x, z1 = code_euler.euler_1Q[i, j, :3]
            z1 = z1 + alpha[j]
            alpha[j] = z2+z1
            z2 = -z1
            line_z1 = 'RotateZ q%d %.3f' % (j, z1)
            line_x = 'RotateX q%d %.3f' % (j, x)
            line_z2 = 'RotateZ q%d %.3f' % (j, z2)
            compiled_list.append(line_z1)
            compiled_list.append(line_x)
            compiled_list.append(line_z2)
        if i+1 < n_d:
            compiled_list.append(code_euler.lines_2Q[i])
    for j in range(code_euler.n_qubits):
        line_alpha = 'RotateZ q%d %.3f' % (j, alpha[j])
        compiled_list.append(line_alpha)
    return compiled_list



def compile_euler_to_MW(code_euler):
    '''
    Inputs code_euler, propagates residual Z gates to the end of the circuit and
    returns a list of MW gates with residual Z gates at the end.  
    '''
    compiled_list=[]
    alpha=np.zeros(code_euler.n_qubits)
    n_1q = int((code_euler.depth + 1) / 2)
    xy_vector = np.zeros((n_1q, code_euler.n_qubits, 2))
    for i in range(n_1q):    
        for q in range(code_euler.n_qubits):
            z2, x, z1 = code_euler.euler_1Q[i, q, :3]
            z1 = z1 + alpha[q] % 360
            alpha[q] = z2+z1 % 360
            z2 = -z1 % 360
            line_MW= 'RotateXY q%d %.3f %.3f' % (q,z2,x)
            compiled_list.append(line_MW)
        if i+1 < n_1q:
            compiled_list.append(code_euler.lines_2Q[i])
    for j in range(code_euler.n_qubits):
        line_alpha = 'RotateZ q%d %.3f' % (j, alpha[j])
        compiled_list.append(line_alpha)
    return compiled_list



def compile_MW_to_X_Y(MW_qasm):
    '''
    Inputs list of qasm in RotateXY gates and compiles possible gates to Rx of Ry gates.
    '''
    new_list=[]
    for line in MW_qasm:
        if 'RotateXY' in line:
            line_split=line.split(' ')
            phi = np.round(float(line_split[2]),5)
            theta = line_split[3]
            if np.round(float(theta)) == 0.0:
                pass
            elif phi % 360 == 0.0:
                new_line='Rx '+line_split[1]+' '+theta
                new_list.append(new_line)
            elif phi % 360 == 90.0:
                new_line='Ry '+line_split[1]+' '+theta
                new_list.append(new_line)
            elif phi % 360 == 180.0:
                new_line='Rx '+line_split[1]+' -'+theta
                new_list.append(new_line)
            elif phi % 360 == 270.0:
                new_line='Ry '+line_split[1]+' -'+theta
                new_list.append(new_line)
            else:
                new_line=' '.join(line_split)
                new_list.append(new_line)
        else: 
            new_list.append(line)
    return new_list