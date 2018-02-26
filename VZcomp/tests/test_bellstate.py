import numpy as np
import os
from unittest import TestCase
import VZcomp.utils as utils
import VZcomp
from subprocess import call


class Quantum_definitions(TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_compilation_call(self):
        compiler_file = VZcomp.__path__[0]+'/compiler.py'
        compiler_file.replace(chr(92), chr(47))
        par_dir = os.path.abspath(os.path.join(VZcomp.__path__[0], os.pardir))
        bell_file = par_dir+'/examples/bell_state/bell_state.qasm'
        bell_file.replace(chr(92), chr(47))
        call('python %s %s --intermediate' % (compiler_file, bell_file))
