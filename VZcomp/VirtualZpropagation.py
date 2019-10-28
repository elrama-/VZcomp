import numpy as np
from VZcomp import representations as rep
import translations as trans
from qsoverlay import DiCarlo_setup
from qsoverlay import Builder
from quantumsim.sparsedm import SparseDM
from qsoverlay import Controller
from qsoverlay import Setup
from qsoverlay.DiCarlo_setup import quick_setup
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

def plot_compiled(file_string,gamma_1,gamma_2,alpha_1,alpha_2,width,height):
    ##Translations
    #Import qasm file
    qasm_list = trans.list_from_file(file_string)
    #Set parameterized gate parameters
    set_qasm_list=trans.set_parameters(qasm_list,gamma_1,gamma_2,alpha_1,alpha_2)
    #Merge all single qubit gates in layer and present as Euler gates for certain parameters
    euler_merged=trans.merge_1Q(file_string,gamma_1,gamma_2,alpha_1,alpha_2)
    #Compile Z gates and set all gates to MW gates
    MW_list=trans.compile_euler_to_MW(euler_merged)
    #Make list readable by qsoverlay
    MW_qasm=trans.list2qasm(MW_list)
    #compile standard MW gates to X and Y gates
    compile_X_Y=trans.compile_MW_to_X_Y(MW_qasm)
    
    
    ##qsoverlay plotting
    #Name Qubits
    qubit_list = ['q0','q1','q2','q3']
    #Initiate setups
    setup_ideal = quick_setup(qubit_list=qubit_list, noise_flag=False) #Ideal set up
    state=SparseDM(qubit_list)
    #Ensure ordering in density matrix
    for i in qubit_list:
        state.ensure_dense(i)
    #Create circuit
    circuitbuild_X_Y_compiled=Builder(setup_ideal)
    circuitbuild_X_Y_compiled.add_qasm(compile_X_Y)
    circuitbuild_X_Y_compiled.finalize()
    plt.figure(figsize=(width,height))
    circuitbuild_X_Y_compiled.circuit.plot()
    
def plot_compilation_with_steps(file_string,gamma_1,gamma_2,alpha_1,alpha_2,width,height):
    ##Translations
    #Import qasm file
    qasm_list = trans.list_from_file(file_string)
    #Set parameterized gate parameters
    set_qasm_list=trans.set_parameters(qasm_list,gamma_1,gamma_2,alpha_1,alpha_2)
    #Merge all single qubit gates in layer and present as Euler gates for certain parameters
    euler_merged=trans.merge_1Q(file_string,gamma_1,gamma_2,alpha_1,alpha_2)
    #get qasm file in list
    merged_list = trans.code_euler_to_list(euler_merged)
    merged_qasm=trans.list2qasm(merged_list)
    #Present euler gates as ZXZ gates
    ZXZ_list=trans.euler2ZXZ(euler_merged)
    ZXZ_qasm=trans.list2qasm(ZXZ_list)
    #Present euler gates as ZXZZ gates
    ZXZZ_list=trans.euler2ZXZZ(euler_merged)
    ZXZZ_qasm=trans.list2qasm(ZXZZ_list)
    #Compile Z gates and write as ZXZ gates
    compiled_list=trans.compile_euler(euler_merged)
    compiled_qasm=trans.list2qasm(compiled_list)
    #Compile Z gates and set all gates to MW gates
    MW_list=trans.compile_euler_to_MW(euler_merged)
    #Make list readable by qsoverlay
    MW_qasm=trans.list2qasm(MW_list)
    #compile standard MW gates to X and Y gates
    compile_X_Y=trans.compile_MW_to_X_Y(MW_qasm)
    
    
    ##qsoverlay plotting
    #Name Qubits
    qubit_list = ['q0','q1','q2','q3']
    #Initiate setups
    setup_ideal = quick_setup(qubit_list=qubit_list, noise_flag=False) #Ideal set up
    state=SparseDM(qubit_list)
    #Ensure ordering in density matrix
    for i in qubit_list:
        state.ensure_dense(i)
   
    #Create circuit for input circuit
    circuitbuild_initial_qasm_deg=Builder(setup_ideal)
    circuitbuild_initial_qasm_deg.add_qasm(set_qasm_list)
    circuitbuild_initial_qasm_deg.finalize()    
    plt.figure(figsize=(width,height))
    circuitbuild_initial_qasm_deg.circuit.plot() 
    
    #Create circuit for merged Euler gates
    circuitbuild_merged_euler=Builder(setup_ideal)
    circuitbuild_merged_euler.add_qasm(merged_qasm)
    circuitbuild_merged_euler.finalize()
    plt.figure(figsize=(width,height))
    circuitbuild_merged_euler.circuit.plot()
    
    #Create circuit for ZXZ gates
    circuitbuild_ZXZ=Builder(setup_ideal)
    circuitbuild_ZXZ.add_qasm(ZXZ_qasm)
    circuitbuild_ZXZ.finalize()
    plt.figure(figsize=(width,height))
    circuitbuild_ZXZ.circuit.plot()
    
    #Create circuit for ZXZZ gates
    circuitbuild_ZXZZ=Builder(setup_ideal)
    circuitbuild_ZXZZ.add_qasm(ZXZZ_qasm)
    circuitbuild_ZXZZ.finalize()
    plt.figure(figsize=(width,height))
    circuitbuild_ZXZZ.circuit.plot()
    
    #Create circuit for compiled Z and ZXZ gates
    circuitbuild_ZXZ_compiled=Builder(setup_ideal)
    circuitbuild_ZXZ_compiled.add_qasm(compiled_qasm)
    circuitbuild_ZXZ_compiled.finalize()
    plt.figure(figsize=(width,height))
    circuitbuild_ZXZ_compiled.circuit.plot()
    
    #Create circuit for compiled Z and MW gates
    circuitbuild_MW_compiled_deg=Builder(setup_ideal)
    circuitbuild_MW_compiled_deg.add_qasm(MW_qasm)
    circuitbuild_MW_compiled_deg.finalize()        
    plt.figure(figsize=(width,height))
    circuitbuild_MW_compiled_deg.circuit.plot()
   
    #Create circuit for compiled Z and X and Y gates
    circuitbuild_X_Y_compiled=Builder(setup_ideal)
    circuitbuild_X_Y_compiled.add_qasm(compile_X_Y)
    circuitbuild_X_Y_compiled.finalize()
    plt.figure(figsize=(width,height))
    circuitbuild_X_Y_compiled.circuit.plot()