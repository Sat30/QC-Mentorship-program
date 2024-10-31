import numpy as np
from qiskit_aer import *
from qiskit import *
from qiskit.visualization import *
from qiskit.quantum_info import *


class My_Quantum_circuit1():
    sub_task_info : int = 1
    num_qubits : int
    state : np.array
    I = np.identity(2)
    x_matrix = np.array([[0, 1], [1, 0]])
    h_matrix = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    cx_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    def __init__(self, num_qubits):
        if num_qubits < 1:
            raise ValueError('Number of qubits should be at least 1')
        state = np.zeros(2**num_qubits)
        state[0] = 1
        self.state = state
        self.num_qubits = num_qubits
    

    def check_out_of_index(self, qubit):
        if qubit >= self.num_qubits:
            raise IndexError('qubit index out of range: ',  qubit)
        
    def get_msb_format(self, qubit_index):
        return self.num_qubits - qubit_index  - 1
        # return qubit_index
    
                
    def apply_gate(self, gate_matrix, qubit_index):
        gate = np.eye(1)
        for i in range(self.num_qubits):
            if i == qubit_index:
                gate = np.kron(gate, gate_matrix)
            else:
                gate = np.kron(gate, self.I)
        self.state = np.dot(gate, self.state)


    def x(self, qubit_index : int):
        self.check_out_of_index(qubit_index)  
        qubit_index = self.get_msb_format(qubit_index)
        self.apply_gate(self.x_matrix, qubit_index)

    def h(self, qubit_index : int):
        self.check_out_of_index(qubit_index)
        qubit_index = self.get_msb_format(qubit_index)
        self.apply_gate(self.h_matrix, qubit_index)
    
    def cx(self, control_qubit, target_qubit):
        if control_qubit == target_qubit:
            raise ValueError('Control and target qubits should be different')
        
        self.check_out_of_index(control_qubit)
        self.check_out_of_index(target_qubit)
        control_qubit = self.get_msb_format(control_qubit)
        target_qubit  = self.get_msb_format(target_qubit)
        gate = self.cx_matrix
        for i in range(self.num_qubits - 2):
            gate = np.kron(gate, self.I)

        curr_state = self.state.reshape((2,) * self.num_qubits)
        curr_state = np.moveaxis(curr_state, [control_qubit, target_qubit], [0, 1])
        curr_state = curr_state.flatten()

        curr_state = np.dot(gate, curr_state)

        curr_state = curr_state.reshape((2,) * self.num_qubits)
        curr_state = np.moveaxis(curr_state, [0, 1], [control_qubit, target_qubit])
        self.state = curr_state.flatten()

        

