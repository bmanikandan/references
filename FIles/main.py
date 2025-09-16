
#!/usr/bin/env python3
"""
PyQuantum - A sample Python application for quantum computing concepts.
"""

import math
from typing import List, Tuple


class QuantumBit:
    """Represents a quantum bit with probability amplitudes."""
    
    def __init__(self, alpha: float = 1.0, beta: float = 0.0):
        """Initialize a qubit with amplitude coefficients."""
        # Normalize the amplitudes
        norm = math.sqrt(alpha**2 + beta**2)
        self.alpha = alpha / norm  # Amplitude for |0⟩ state
        self.beta = beta / norm    # Amplitude for |1⟩ state
    
    def measure(self) -> int:
        """Measure the qubit, collapsing to 0 or 1."""
        probability_zero = self.alpha**2
        import random
        return 0 if random.random() < probability_zero else 1
    
    def hadamard(self):
        """Apply Hadamard gate to create superposition."""
        new_alpha = (self.alpha + self.beta) / math.sqrt(2)
        new_beta = (self.alpha - self.beta) / math.sqrt(2)
        self.alpha = new_alpha
        self.beta = new_beta
    
    def __str__(self) -> str:
        return f"{self.alpha:.3f}|0⟩ + {self.beta:.3f}|1⟩"


class QuantumCircuit:
    """Simple quantum circuit simulator."""
    
    def __init__(self, num_qubits: int):
        self.qubits = [QuantumBit() for _ in range(num_qubits)]
    
    def apply_hadamard(self, qubit_index: int):
        """Apply Hadamard gate to specified qubit."""
        if 0 <= qubit_index < len(self.qubits):
            self.qubits[qubit_index].hadamard()
    
    def measure_all(self) -> List[int]:
        """Measure all qubits in the circuit."""
        return [qubit.measure() for qubit in self.qubits]
    
    def get_state(self) -> List[str]:
        """Get string representation of all qubit states."""
        return [str(qubit) for qubit in self.qubits]


def main():
    """Demonstrate basic quantum operations."""
    print("PyQuantum - Quantum Computing Simulation")
    print("=" * 40)
    
    # Create a quantum circuit with 3 qubits
    circuit = QuantumCircuit(3)
    
    print("Initial state:")
    for i, state in enumerate(circuit.get_state()):
        print(f"  Qubit {i}: {state}")
    
    # Apply Hadamard gates to create superposition
    print("\nApplying Hadamard gates...")
    for i in range(3):
        circuit.apply_hadamard(i)
    
    print("After Hadamard gates:")
    for i, state in enumerate(circuit.get_state()):
        print(f"  Qubit {i}: {state}")
    
    # Perform measurements
    print("\nMeasurement results:")
    for trial in range(5):
        measurements = circuit.measure_all()
        binary_str = ''.join(map(str, measurements))
        print(f"  Trial {trial + 1}: {binary_str}")


if __name__ == "__main__":
    main()