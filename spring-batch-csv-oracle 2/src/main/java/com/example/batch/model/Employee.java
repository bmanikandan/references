package com.example.batch.model;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Employee entity representing both CSV input and Oracle table structure.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Employee {

    private Long id;

    @NotBlank(message = "Employee ID is required")
    private String employeeId;

    @NotBlank(message = "First name is required")
    private String firstName;

    @NotBlank(message = "Last name is required")
    private String lastName;

    @Email(message = "Invalid email format")
    private String email;

    private String department;

    @NotNull(message = "Salary is required")
    @Positive(message = "Salary must be positive")
    private BigDecimal salary;

    private LocalDate hireDate;

    private String status;

    // CSV line number for error tracking
    private int lineNumber;
}
