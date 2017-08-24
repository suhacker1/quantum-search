'''An implementation of Grover's Algorithm'''
#Dependencies
import sys
sys.path.append("/Users/suhahussain/qiskit-sdk-py/")
from qiskit import QuantumProgram
import Qconfig

#Initializing the program as well as the registers and the circuit
qp = QuantumProgram()
n = 2 # n refers to the number of qubits in the system
qr = qp.create_quantum_register('qr', n)
cr = qp.create_classical_register('cr', n)
qc = qp.create_circuit('Circuit', [qr], [cr])

#Creating the uniform superposition by applying Hadamard gates to each register
for i in range(n):
    qc.h(qr[i])

#Setting the input to search for
#In this program, we are searching for "00" so the Phase gate is applied twice to each register.
#Delete the S gates for the first or second register for '10' or '01' respectively.
#Delete all of the S gates for '11'.
qc.s(qr[0])
qc.s(qr[1])
qc.s(qr[0])
qc.s(qr[1])

#Oracle
qc.h(qr[1]) #Hadamard to second register
qc.cx(qr[0],qr[1]) #Control function for both qubits
qc.h(qr[1]) #Hadamard to second register

for i in range(n): #Hadamard on both qubits
    qc.h(qr[i])

#Reflection of Oracle function
for i in range(n): #X gates/ bit flips on both qubits
    qc.x(qr[i])

qc.h(qr[1]) #Hadamard to second register
qc.cx(qr[0],qr[1]) #Control function for both qubits
qc.h(qr[1])  #Hadamard to second register

for i in range(n):  #X gates/ bit flips on both qubits
    qc.x(qr[i])
for i in range(n): #Hadamard on both qubits
    qc.h(qr[i])

#Measurements of qubits along Z-axis
qc.measure(qr[0], cr[0])
qc.measure(qr[1], cr[1])

#Executing on a local quantum computer simulator and printing counts
result = qp.execute(["Circuit"], backend='local_qasm_simulator',
                    coupling_map=None, shots=1024)
print(result.get_counts('Circuit'))
