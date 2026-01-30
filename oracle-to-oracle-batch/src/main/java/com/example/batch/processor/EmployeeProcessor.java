package com.example.batch.processor;

import com.example.batch.model.Employee;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.item.ItemProcessor;

import java.util.Set;
import java.util.stream.Collectors;

/**
 * Processor for Employee records.
 * Performs validation, transformation, and data cleansing.
 */
@Slf4j
public class EmployeeProcessor implements ItemProcessor<Employee, Employee> {

    private final Validator validator;

    public EmployeeProcessor() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        this.validator = factory.getValidator();
    }

    @Override
    public Employee process(Employee employee) throws Exception {
        log.debug("Processing employee: {}", employee.getEmployeeId());

        // Validate the employee
        Set<ConstraintViolation<Employee>> violations = validator.validate(employee);
        if (!violations.isEmpty()) {
            String errorMessage = violations.stream()
                    .map(v -> v.getPropertyPath() + ": " + v.getMessage())
                    .collect(Collectors.joining(", "));
            log.warn("Validation failed for employee {}: {}", employee.getEmployeeId(), errorMessage);
            throw new IllegalArgumentException("Validation failed: " + errorMessage);
        }

        // Transform/clean the data
        Employee transformed = Employee.builder()
                .employeeId(employee.getEmployeeId().trim().toUpperCase())
                .firstName(capitalizeFirstLetter(employee.getFirstName()))
                .lastName(capitalizeFirstLetter(employee.getLastName()))
                .email(employee.getEmail() != null ? employee.getEmail().toLowerCase().trim() : null)
                .department(employee.getDepartment() != null ? employee.getDepartment().trim() : null)
                .salary(employee.getSalary())
                .hireDate(employee.getHireDate())
                .status(normalizeStatus(employee.getStatus()))
                .build();

        log.debug("Transformed employee: {} -> {}", employee.getEmployeeId(), transformed.getEmployeeId());
        return transformed;
    }

    private String capitalizeFirstLetter(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        String trimmed = input.trim();
        return trimmed.substring(0, 1).toUpperCase() + trimmed.substring(1).toLowerCase();
    }

    private String normalizeStatus(String status) {
        if (status == null || status.isEmpty()) {
            return "ACTIVE";
        }
        return switch (status.trim().toUpperCase()) {
            case "A", "ACTIVE", "1" -> "ACTIVE";
            case "I", "INACTIVE", "0" -> "INACTIVE";
            case "T", "TERMINATED" -> "TERMINATED";
            case "L", "LEAVE" -> "ON_LEAVE";
            default -> "ACTIVE";
        };
    }
}
