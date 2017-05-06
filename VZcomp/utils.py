import numpy as np
from transforms3d import euler
import VZcomp.qdef as qdef

def list_from_file(filepath):
	lines = [line.rstrip('\n') for line in open(filepath)]
	return lines


def split_entangling(script):
    '''
    Splits a QASM script into stages of 1Q gates and 2Q gates
    '''
    list_1Q = []
    list_2Q = []
    accum_1Q = []
    for ii, line in enumerate(script):
        if line[:2] == 'CZ':
            if accum_1Q == []:
                list_2Q[-1] += ';'+ line
            else:
                list_2Q.append(line)
                list_1Q.append(accum_1Q)
                accum_1Q = []
        else:
            accum_1Q.append(line)
    list_1Q.append(accum_1Q)
    return list_1Q, list_2Q


def op2matrix(op_string):
    '''
    Produces a 3D rotation matrix from a gate string
    Inputs:
            op_string (str): gate within {X,Y,Z,H,T}.
                             For X,Y,Z angles are admited in deg like Y36.
    '''
    op_string = op_string.split(' ')[0]
    axis_str = op_string[0]
    if len(op_string) > 1:
        angle = float(op_string[1:])
    else:
        angle = np.pi
    if axis_str == 'X':
        axis = [1, 0, 0]
        angle = angle * np.pi/180.
    elif axis_str == 'Y':
        axis = [1, 0, 0]
        angle = angle * np.pi/180.
    elif axis_str == 'Z':
        axis = [1, 0, 0]
        angle = angle * np.pi/180.
    elif op_string == 'H':
        axis = [1./np.sqrt(2.), 0, 1./np.sqrt(2.)]
        angle = np.pi
    elif op_string == 'T':
        axis = [0, 0, 1]
        angle = np.pi/4.
    elif op_string == 'I':
        axis = [0, 0, 0]
        angle = 0.

    return qdef.qrot2mat(axis, angle)


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


def mat2szxz(matrix):
    '''
    Compiles the input rotation as ZXZ rotations.
    Inputs:
            matrix (array): rotation matrix
    Output:
            Angle Z,Angle X,Angle Z
    '''
    axis, angle = qdef.mat2qrot(matrix)
    return rot2szxz(axis, angle)

def update_frame(prev_z_angle, init_angle=0.):
	'''
	Updates the frame of a MW pulse under the following condition:
	Z(alpha)XZ(-alpha)

	More concrete:
	Z,-alpha q0
	X,beta q0
	Z,alpha q0

	turns into
	-alpha,beta q0

	the above being a rotation around the axis that locates at angle -alpha in the X-Y plane.
	'''
	return init_angle+prev_z_angle
