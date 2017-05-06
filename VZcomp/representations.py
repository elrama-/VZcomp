'''
representations
qumis/qasm input: script
ordered list: arrays containing the 1Q and the 2Q steps
rotation list: arrays, but instead of strings, su2 operations on the same mw step are packed into one
euler list: arrays, but instead of su2 rotations, we already have their szxz representation
compiled list: z gates are packed, and x gates are rotated by their preceding zs
qumis/qasm final: script
-----------------------------
'''


class qumis:

	def __init__(self, lines, n_qubits):
		self.lines = lines
		self.n_qubits = n_qubits
		self.depth = len(lines)


class structured_script:

	def __init__(self, lines_1Q, lines_2Q, n_qubits):
		# 1Q,[2Q,1Q]xd,RO
		self.n_qubits = n_qubits
		# 1Qubit- and 2Qubit-operations layers do not match in size
		if not((len(lines_2Q)+1) == len(lines_1Q)):
			raise ValueError('1Qubit- and 2Qubit-operations layers do not match in size')
		self.depth = 1+2*len(lines_2Q)
		self.lines_1Q = lines_1Q
		self.lines_2Q = lines_2Q


class rotation_list:

	def __init__(self, rotations_1Q, lines_2Q, n_qubits):
		self.rotations_1Q = rotations_1Q
		self.lines_2Q = lines_2Q
		self.n_qubits = n_qubits
		dim_depth, dim_qubits, dim_rot = self.rotations_1Q.shape
		self.depth = 1+2*len(lines_2Q)
		# 1Q rotations vector does not match the depth
		if not((2*dim_depth-1) == self.depth):
			raise ValueError('1Q rotations vector does not match the depth')
		# 1Q rotations vector does not match the qubit number
		if not(dim_qubits == n_qubits):
			raise ValueError('1Q rotations vector does not match the qubit number')
		# 1Q rotations vector does not match the parameter number
		if not(dim_rot == 4):
			raise ValueError('1Q rotations vector does not match the parameter number')


class euler_list:

	def __init__(self, euler_1Q, lines_2Q, n_qubits):
		self.euler_1Q = euler_1Q
		self.lines_2Q = lines_2Q
		self.n_qubits = n_qubits
		dim_depth, dim_qubits, dim_euler = self.euler_1Q.shape
		self.depth = 1+2*len(lines_2Q)
		# euler angles vector does not match the depth
		if not((2*dim_depth-1) == self.depth):
			raise ValueError('euler angles vector does not match the depth')
		# euler angles vector does not match the qubit number
		if not(dim_qubits == n_qubits):
			raise ValueError('euler angles vector does not match the qubit number')
		# euler angles vector does not match the parameter number
		if not(dim_euler == 3):
			raise ValueError('euler angles vector does not match the parameter number')


class XYcompiled_list:

	def __init__(self, XY_rotations, lines_2Q, n_qubits):
		self.XY_rotations = XY_rotations
		self.lines_2Q = lines_2Q
		self.n_qubits = n_qubits
		dim_depth, dim_qubits, dim_XY = self.XY_rotations.shape
		self.depth = 1+2*len(lines_2Q)
		# XY rotations vector does not match the depth
		if not((2*dim_depth-1) == self.depth):
			raise ValueError('XY rotations vector does not match the depth')
		# XY rotations vector does not match the qubit number
		if not(dim_qubits == n_qubits):
			raise ValueError('XY rotations vector does not match the qubit number')
		# XY rotations vector does not match the parameter number
		if not(dim_XY == 2):
			raise ValueError('XY rotations vector does not match the parameter number')

	def print(self, fname):
		raw_script = []
		f = open(fname, mode='w+')
		n_d = len(self.XY_rotations[:,0,0])
		for i in range(n_d):
			for j in range(self.n_qubits):
				if self.XY_rotations[i,j,0]==0 and self.XY_rotations[i,j,1]==0:
					line = 'I q%d\n'%j
				else:
					line = 'R %.3f, %.3f q%d\n' % (self.XY_rotations[i,j,0],
						                           self.XY_rotations[i,j,1], j)
				raw_script.append(line)
			if i+1 < n_d:
				print(i)
				raw_script.append(self.lines_2Q[i]+'\n')
		f.writelines(raw_script)
		f.close()
