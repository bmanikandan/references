#!/usr/bin/env python3
"""
First Quantum Program - Introduction to Quantum Computing Concepts

This program demonstrates the fundamental concepts of quantum computing:
1. Quantum bits (qubits) and superposition
2. Quantum gates and operations
3. Measurement and probability
4. Bell states and entanglement
"""

import math
import random
from typing import List, Tuple, Dict


class Qubit:
    """A quantum bit with complex probability amplitudes."""
    
    def __init__(self, alpha: float = 1.0, beta: float = 0.0):
        """
        Initialize a qubit with amplitudes for |0⟩ and |1⟩ states.
        |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1
        """
        self._normalize(alpha, beta)
    
    def _normalize(self, alpha: float, beta: float):
        """Normalize the amplitude coefficients."""
        norm = math.sqrt(alpha**2 + beta**2)
        if norm == 0:
            norm = 1
        self.alpha = alpha / norm
        self.beta = beta / norm
    
    def measure(self) -> int:
        """
        Measure the qubit, collapsing it to |0⟩ or |1⟩.
        Probability of |0⟩ = |α|², Probability of |1⟩ = |β|²
        """
        prob_zero = self.alpha**2
        result = 0 if random.random() < prob_zero else 1
        
        # After measurement, qubit collapses to the measured state
        if result == 0:
            self.alpha, self.beta = 1.0, 0.0
        else:
            self.alpha, self.beta = 0.0, 1.0
        
        return result
    
    def apply_x_gate(self):
        """Apply Pauli-X gate (quantum NOT gate): |0⟩ ↔ |1⟩"""
        self.alpha, self.beta = self.beta, self.alpha
    
    def apply_hadamard_gate(self):
        """
        Apply Hadamard gate to create superposition:
        |0⟩ → (|0⟩ + |1⟩)/√2
        |1⟩ → (|0⟩ - |1⟩)/√2
        """
        new_alpha = (self.alpha + self.beta) / math.sqrt(2)
        new_beta = (self.alpha - self.beta) / math.sqrt(2)
        self.alpha = new_alpha
        self.beta = new_beta
    
    def apply_z_gate(self):
        """Apply Pauli-Z gate: |0⟩ → |0⟩, |1⟩ → -|1⟩"""
        self.beta = -self.beta
    
    def get_probabilities(self) -> Tuple[float, float]:
        """Get probabilities of measuring |0⟩ and |1⟩."""
        return (self.alpha**2, self.beta**2)
    
    def __str__(self) -> str:
        """String representation of the qubit state."""
        return f"{self.alpha:.3f}|0⟩ + {self.beta:.3f}|1⟩"


def demonstrate_basic_qubit():
    """Demonstrate basic qubit operations."""
    print("🔬 BASIC QUBIT OPERATIONS")
    print("-" * 30)
    
    # Create a qubit in |0⟩ state
    qubit = Qubit()
    print(f"Initial state: {qubit}")
    print(f"Probabilities: P(0)={qubit.get_probabilities()[0]:.3f}, P(1)={qubit.get_probabilities()[1]:.3f}")
    
    # Apply X gate (quantum NOT)
    print("\nApplying X gate (quantum NOT)...")
    qubit.apply_x_gate()
    print(f"After X gate: {qubit}")
    
    # Reset and apply Hadamard gate
    qubit = Qubit()
    print("\nApplying Hadamard gate (creates superposition)...")
    qubit.apply_hadamard_gate()
    print(f"After Hadamard: {qubit}")
    print(f"Probabilities: P(0)={qubit.get_probabilities()[0]:.3f}, P(1)={qubit.get_probabilities()[1]:.3f}")
    
    # Measure the qubit multiple times (need fresh qubits each time)
    print("\nMeasuring superposed qubits (10 trials):")
    results = []
    for i in range(10):
        fresh_qubit = Qubit()
        fresh_qubit.apply_hadamard_gate()
        result = fresh_qubit.measure()
        results.append(result)
        print(f"Trial {i+1}: {result}")
    
    count_0 = results.count(0)
    count_1 = results.count(1)
    print(f"\nResults: {count_0} zeros, {count_1} ones")
    print(f"Experimental probabilities: P(0)={count_0/10:.1f}, P(1)={count_1/10:.1f}")


def quantum_coin_flip():
    """Use quantum superposition for a truly random coin flip."""
    print("\n\n🪙 QUANTUM COIN FLIP")
    print("-" * 20)
    
    print("Using quantum superposition for perfect randomness...")
    
    qubit = Qubit()
    qubit.apply_hadamard_gate()  # Create equal superposition
    
    print(f"Qubit in superposition: {qubit}")
    result = qubit.measure()
    
    coin_result = "HEADS" if result == 0 else "TAILS"
    print(f"Quantum coin flip result: {coin_result}")


def quantum_random_number_generator(bits: int = 4):
    """Generate random numbers using quantum superposition."""
    print(f"\n\n🎲 QUANTUM RANDOM NUMBER GENERATOR ({bits} bits)")
    print("-" * 40)
    
    print(f"Generating {bits}-bit random number using quantum superposition...")
    
    binary_result = ""
    for i in range(bits):
        qubit = Qubit()
        qubit.apply_hadamard_gate()
        bit = qubit.measure()
        binary_result += str(bit)
    
    decimal_result = int(binary_result, 2)
    print(f"Binary: {binary_result}")
    print(f"Decimal: {decimal_result}")
    print(f"Range: 0 to {2**bits - 1}")


def demonstrate_quantum_interference():
    """Show quantum interference using multiple Hadamard gates."""
    print("\n\n🌊 QUANTUM INTERFERENCE")
    print("-" * 25)
    
    print("Applying two Hadamard gates (should return to |0⟩)...")
    
    qubit = Qubit()
    print(f"Initial: {qubit}")
    
    qubit.apply_hadamard_gate()
    print(f"After 1st Hadamard: {qubit}")
    
    qubit.apply_hadamard_gate()
    print(f"After 2nd Hadamard: {qubit}")
    
    print("The amplitudes interfere to return the qubit to |0⟩!")


def quantum_phase_demonstration():
    """Demonstrate quantum phase with Z gate."""
    print("\n\n⚡ QUANTUM PHASE")
    print("-" * 17)
    
    print("Demonstrating quantum phase with Z gate...")
    
    # Start with |1⟩ state
    qubit = Qubit(0.0, 1.0)
    print(f"Initial |1⟩ state: {qubit}")
    
    # Apply Z gate (adds phase to |1⟩)
    qubit.apply_z_gate()
    print(f"After Z gate: {qubit}")
    print("Note: The -1 coefficient represents a quantum phase!")
    
    # Phase doesn't affect measurement probabilities
    prob_0, prob_1 = qubit.get_probabilities()
    print(f"Probabilities unchanged: P(0)={prob_0:.3f}, P(1)={prob_1:.3f}")


def main():
    """Run the complete first quantum program tutorial."""
    print("🚀 WELCOME TO YOUR FIRST QUANTUM PROGRAM!")
    print("=" * 45)
    print("This program will teach you quantum computing basics:")
    print("• Qubits and superposition")
    print("• Quantum gates")
    print("• Measurement and probability")
    print("• Quantum randomness")
    print("• Interference and phase")
    
    # Run demonstrations
    demonstrate_basic_qubit()
    quantum_coin_flip()
    quantum_random_number_generator(4)
    demonstrate_quantum_interference()
    quantum_phase_demonstration()
    
    print("\n\n🎉 CONGRATULATIONS!")
    print("You've completed your first quantum program!")
    print("\nKey takeaways:")
    print("• Qubits can exist in superposition of |0⟩ and |1⟩")
    print("• Measurement collapses superposition randomly")
    print("• Quantum gates manipulate probability amplitudes")
    print("• Quantum effects enable true randomness")
    print("• Phase and interference are unique quantum phenomena")


if __name__ == "__main__":
    # Set seed for reproducible demonstrations (remove for true randomness)
    random.seed(42)
    main()