import numpy as np
from qiskit_aer import *
from qiskit import *
from qiskit.visualization import *
from qiskit.quantum_info import *


class My_Quantum_circuit2():
    sub_task_info : int = 2
    I = np.identity(2)
    x_matrix = np.array([[0, 1], [1, 0]])
    h_matrix = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    cx_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    num_qubits : int
    state : np.array

    def __init__(self, num_qubits):
        if num_qubits < 1:
            raise ValueError('Number of qubits should be at least 1')
        state = np.zeros((2,) * num_qubits)
        state[(0, )* num_qubits] = 1
        self.state = state
        self.num_qubits = num_qubits
    

    def check_out_of_index(self, qubit):
        if qubit >= self.num_qubits:
            raise IndexError('qubit index out of range: ',  qubit)
        
    def get_msb_format(self, qubit_index):
        return self.num_qubits - qubit_index  - 1
        # return qubit_index
    
    def apply_gate_2(self, state, gate_matrix, qubit_index):
        """
        testing optimized way
        but not correct way
        """
        qubit_index = self.get_msb_format(qubit_index)
        self.state = np.tensordot(gate_matrix, self.state, axes=([1], [qubit_index]))


    def apply_gate(self, state, gate_matrix, qubit_index):
        qubit_index = self.get_msb_format(qubit_index)
        self.state = np.moveaxis(self.state, qubit_index, 0)
        self.state = np.tensordot(gate_matrix, self.state, axes=([1], [0]))
        self.state = np.moveaxis(self.state, 0, qubit_index)
            

    def x(self, qubit_index : int):
        self.check_out_of_index(qubit_index)
        self.apply_gate(self.state, self.x_matrix, qubit_index)

    def h(self, qubit_index : int):
        self.check_out_of_index(qubit_index)
        self.apply_gate(self.state, self.h_matrix, qubit_index)
    
    def cx(self, control_qubit, target_qubit):
        self.check_out_of_index(control_qubit)
        self.check_out_of_index(target_qubit)
        control_qubit = self.get_msb_format(control_qubit)
        target_qubit  = self.get_msb_format(target_qubit)
        gate = self.cx_matrix    

        # Bringing control_qubit_axes and target_qubit axes in 0, 1 (so we can reshape into (4, 1, 2,..))
        curr_state = np.moveaxis(self.state, [control_qubit, target_qubit], [0, 1])
        curr_state = curr_state.reshape((4, 1,) +  (2,)* (self.num_qubits - 2))

        curr_state = np.tensordot(gate, curr_state, axes=([1], [0]))

        curr_state = curr_state.reshape((2, ) * (self.num_qubits))
        curr_state = np.moveaxis(curr_state, [0, 1], [control_qubit, target_qubit])        
        self.state = curr_state
        
        
    