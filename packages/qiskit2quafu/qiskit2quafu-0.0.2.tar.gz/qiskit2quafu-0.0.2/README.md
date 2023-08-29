
This package converts the circuit of qiskit into a circuit supported by quafu
The converted circuit can be input to the cloud platform for processing

Input:
qc: QuantumCircuit object of Qiskit

regName (optional): Modified register name
basis_gates (optional): The set of gates supported by the quafu chip
optimization_level (optional): optimization level

Output:
The function returns two objects, quafu_qc and qc_merge
quafu_qc: The circuit instance of quafu;
qc_merge: The converted qasm circuit in string form.
