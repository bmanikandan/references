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
import org.springframework.batch.item.database.builder.JdbcBatchItemWriterBuilder;
import org.springframework.batch.item.file.FlatFileItemReader;
import org.springframework.batch.item.file.FlatFileParseException;
import org.springframework.batch.item.file.builder.FlatFileItemReaderBuilder;
import org.springframework.batch.item.file.mapping.BeanWrapperFieldSetMapper;
import org.springframework.batch.item.file.transform.DelimitedLineTokenizer;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;
import org.springframework.transaction.PlatformTransactionManager;

import javax.sql.DataSource;
import java.beans.PropertyEditorSupport;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

/**
 * Spring Batch configuration for CSV to Oracle ETL job.
 */
@Configuration
public class BatchConfig {

    @Value("${batch.chunk-size:100}")
    private int chunkSize;

    @Value("${batch.skip-limit:10}")
    private int skipLimit;

    /**
     * CSV File ItemReader with field mapping to Employee.
     */
    @Bean
    @StepScope
    public FlatFileItemReader<Employee> csvReader(
            @Value("#{jobParameters['inputFile'] ?: '${batch.input.file}'}") Resource inputFile) {

        // Custom FieldSetMapper to handle LocalDate parsing
        BeanWrapperFieldSetMapper<Employee> fieldSetMapper = new BeanWrapperFieldSetMapper<>();
        fieldSetMapper.setTargetType(Employee.class);

        // Register custom editor for LocalDate
        Map<Class<?>, PropertyEditorSupport> customEditors = new HashMap<>();
        customEditors.put(LocalDate.class, new PropertyEditorSupport() {
            @Override
            public void setAsText(String text) {
                if (text == null || text.trim().isEmpty()) {
                    setValue(null);
                } else {
                    setValue(LocalDate.parse(text, DateTimeFormatter.ISO_LOCAL_DATE));
                }
            }
        });
        fieldSetMapper.setCustomEditors(customEditors);

        return new FlatFileItemReaderBuilder<Employee>()
                .name("employeeCsvReader")
                .resource(inputFile)
                .linesToSkip(1) // Skip header row
                .delimited()
                .delimiter(",")
                .names("employeeId", "firstName", "lastName", "email", 
                       "department", "salary", "hireDate", "status")
                .fieldSetMapper(fieldSetMapper)
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
     * JDBC Writer for Oracle database using MERGE (upsert) operation.
     */
    @Bean
    public JdbcBatchItemWriter<Employee> oracleWriter(
            @Qualifier("oracleDataSource") DataSource oracleDataSource) {

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
                .dataSource(oracleDataSource)
                .sql(sql)
                .beanMapped()
                .build();
    }

    /**
     * Step definition with chunk-oriented processing.
     */
    @Bean
    public Step importEmployeeStep(
            JobRepository jobRepository,
            PlatformTransactionManager transactionManager,
            FlatFileItemReader<Employee> csvReader,
            EmployeeProcessor employeeProcessor,
            JdbcBatchItemWriter<Employee> oracleWriter,
            StepExecutionNotificationListener stepListener) {

        return new StepBuilder("importEmployeeStep", jobRepository)
                .<Employee, Employee>chunk(chunkSize, transactionManager)
                .reader(csvReader)
                .processor(employeeProcessor)
                .writer(oracleWriter)
                .faultTolerant()
                .skipLimit(skipLimit)
                .skip(FlatFileParseException.class)
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
