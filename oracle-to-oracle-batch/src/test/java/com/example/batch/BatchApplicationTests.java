package com.example.batch;

import com.example.batch.model.Employee;
import com.example.batch.processor.EmployeeProcessor;
import org.junit.jupiter.api.Test;
import org.springframework.batch.core.*;
import org.springframework.batch.test.JobLauncherTestUtils;
import org.springframework.batch.test.JobRepositoryTestUtils;
import org.springframework.batch.test.context.SpringBatchTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDate;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@SpringBatchTest
@ActiveProfiles("test")
class BatchApplicationTests {

    @Autowired
    private JobLauncherTestUtils jobLauncherTestUtils;

    @Autowired
    private JobRepositoryTestUtils jobRepositoryTestUtils;

    @Test
    void contextLoads() {
        // Verify application context loads successfully
    }

    @Test
    void testEmployeeProcessor_ValidEmployee() throws Exception {
        EmployeeProcessor processor = new EmployeeProcessor();

        Employee input = Employee.builder()
                .employeeId("emp001")
                .firstName("john")
                .lastName("doe")
                .email("JOHN.DOE@EXAMPLE.COM")
                .department("engineering")
                .salary(new BigDecimal("75000.00"))
                .hireDate(LocalDate.of(2020, 1, 15))
                .status("A")
                .build();

        Employee result = processor.process(input);

        assertThat(result).isNotNull();
        assertThat(result.getEmployeeId()).isEqualTo("EMP001");
        assertThat(result.getFirstName()).isEqualTo("John");
        assertThat(result.getLastName()).isEqualTo("Doe");
        assertThat(result.getEmail()).isEqualTo("john.doe@example.com");
        assertThat(result.getStatus()).isEqualTo("ACTIVE");
    }

    @Test
    void testEmployeeProcessor_InvalidEmployee() {
        EmployeeProcessor processor = new EmployeeProcessor();

        Employee invalidEmployee = Employee.builder()
                .employeeId(null) // Required field missing
                .firstName("John")
                .lastName("Doe")
                .salary(new BigDecimal("-1000")) // Invalid negative salary
                .build();

        assertThatThrownBy(() -> processor.process(invalidEmployee))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Validation failed");
    }

    @Test
    void testEmployeeProcessor_StatusNormalization() throws Exception {
        EmployeeProcessor processor = new EmployeeProcessor();

        // Test various status inputs
        assertThat(processWithStatus(processor, "A")).isEqualTo("ACTIVE");
        assertThat(processWithStatus(processor, "ACTIVE")).isEqualTo("ACTIVE");
        assertThat(processWithStatus(processor, "1")).isEqualTo("ACTIVE");
        assertThat(processWithStatus(processor, "I")).isEqualTo("INACTIVE");
        assertThat(processWithStatus(processor, "T")).isEqualTo("TERMINATED");
        assertThat(processWithStatus(processor, "L")).isEqualTo("ON_LEAVE");
        assertThat(processWithStatus(processor, null)).isEqualTo("ACTIVE");
        assertThat(processWithStatus(processor, "")).isEqualTo("ACTIVE");
    }

    private String processWithStatus(EmployeeProcessor processor, String status) throws Exception {
        Employee input = Employee.builder()
                .employeeId("EMP001")
                .firstName("John")
                .lastName("Doe")
                .salary(new BigDecimal("50000"))
                .status(status)
                .build();
        return processor.process(input).getStatus();
    }
}
