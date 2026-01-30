package com.example.batch.config;

import com.example.batch.listener.JobCompletionNotificationListener;
import com.example.batch.listener.StepExecutionNotificationListener;
import com.example.batch.model.Employee;
import com.example.batch.processor.EmployeeProcessor;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.StepScope;
import org.springframework.batch.core.job.builder.JobBuilder;
import org.springframework.batch.core.launch.support.RunIdIncrementer;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.batch.core.step.builder.StepBuilder;
import org.springframework.batch.item.database.JdbcBatchItemWriter;
import org.springframework.batch.item.database.JdbcCursorItemReader;
import org.springframework.batch.item.database.builder.JdbcBatchItemWriterBuilder;
import org.springframework.batch.item.database.builder.JdbcCursorItemReaderBuilder;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;

/**
 * Spring Batch configuration for Oracle-to-Oracle ETL job.
 * Reads from source Oracle database and writes to target Oracle database.
 * Uses in-memory H2 for JobRepository metadata.
 */
@Configuration
public class BatchConfig {

    @Value("${batch.chunk-size:100}")
    private int chunkSize;

    @Value("${batch.skip-limit:10}")
    private int skipLimit;

    @Value("${batch.source.query}")
    private String sourceQuery;

    /**
     * JDBC Cursor ItemReader for reading from source Oracle database.
     * Uses cursor-based reading for efficient memory usage with large datasets.
     */
    @Bean
    @StepScope
    public JdbcCursorItemReader<Employee> sourceOracleReader(
            @Qualifier("sourceDataSource") DataSource sourceDataSource,
            @Value("#{jobParameters['customQuery']}") String customQuery) {

        String query = (customQuery != null && !customQuery.isBlank()) ? customQuery : sourceQuery;

        return new JdbcCursorItemReaderBuilder<Employee>()
                .name("sourceOracleReader")
                .dataSource(sourceDataSource)
                .sql(query)
                .rowMapper(new BeanPropertyRowMapper<>(Employee.class))
                .fetchSize(chunkSize) // Match fetch size with chunk size for optimal performance
                .saveState(true)
                .build();
    }

    /**
     * Employee processor for validation and transformation.
     */
    @Bean
    public EmployeeProcessor employeeProcessor() {
        return new EmployeeProcessor();
    }

    /**
     * JDBC Batch Writer for target Oracle database using MERGE (upsert) operation.
     * Performs insert if record doesn't exist, update if it does.
     */
    @Bean
    public JdbcBatchItemWriter<Employee> targetOracleWriter(
            @Qualifier("targetDataSource") DataSource targetDataSource) {

        // MERGE statement for upsert operation (insert or update)
        String sql = """
            MERGE INTO employees e
            USING (SELECT :employeeId AS employee_id FROM dual) src
            ON (e.employee_id = src.employee_id)
            WHEN MATCHED THEN
                UPDATE SET
                    first_name = :firstName,
                    last_name = :lastName,
                    email = :email,
                    department = :department,
                    salary = :salary,
                    hire_date = :hireDate,
                    status = :status,
                    updated_at = SYSTIMESTAMP
            WHEN NOT MATCHED THEN
                INSERT (employee_id, first_name, last_name, email, 
                        department, salary, hire_date, status, created_at, updated_at)
                VALUES (:employeeId, :firstName, :lastName, :email,
                        :department, :salary, :hireDate, :status, SYSTIMESTAMP, SYSTIMESTAMP)
            """;

        return new JdbcBatchItemWriterBuilder<Employee>()
                .dataSource(targetDataSource)
                .sql(sql)
                .beanMapped()
                .build();
    }

    /**
     * Step definition with chunk-oriented processing.
     * Reads from source Oracle, processes, and writes to target Oracle.
     */
    @Bean
    public Step importEmployeeStep(
            JobRepository jobRepository,
            PlatformTransactionManager transactionManager,
            JdbcCursorItemReader<Employee> sourceOracleReader,
            EmployeeProcessor employeeProcessor,
            JdbcBatchItemWriter<Employee> targetOracleWriter,
            StepExecutionNotificationListener stepListener) {

        return new StepBuilder("importEmployeeStep", jobRepository)
                .<Employee, Employee>chunk(chunkSize, transactionManager)
                .reader(sourceOracleReader)
                .processor(employeeProcessor)
                .writer(targetOracleWriter)
                .faultTolerant()
                .skipLimit(skipLimit)
                .skip(IllegalArgumentException.class)
                .listener(stepListener)
                .build();
    }

    /**
     * Job definition with completion listener.
     */
    @Bean
    public Job importEmployeeJob(
            JobRepository jobRepository,
            Step importEmployeeStep,
            JobCompletionNotificationListener jobListener) {

        return new JobBuilder("importEmployeeJob", jobRepository)
                .incrementer(new RunIdIncrementer())
                .listener(jobListener)
                .start(importEmployeeStep)
                .build();
    }
}
