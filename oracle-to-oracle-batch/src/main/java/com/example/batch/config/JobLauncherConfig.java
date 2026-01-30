package com.example.batch.config;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersBuilder;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

import java.time.LocalDateTime;

/**
 * Job launcher configuration for programmatic job execution.
 * Active when 'cli' profile is enabled.
 */
@Slf4j
@Configuration
@RequiredArgsConstructor
public class JobLauncherConfig {

    private final JobLauncher jobLauncher;
    private final Job importEmployeeJob;

    /**
     * Command line runner to execute the job on application startup.
     * Only active when 'cli' profile is enabled.
     */
    @Bean
    @Profile("cli")
    public CommandLineRunner runJob() {
        return args -> {
            JobParametersBuilder builder = new JobParametersBuilder()
                    .addLocalDateTime("startTime", LocalDateTime.now());

            // Check for custom query argument
            if (args.length > 0) {
                String customQuery = args[0];
                log.info("Using custom query from argument: {}", customQuery);
                builder.addString("customQuery", customQuery);
            }

            JobParameters jobParameters = builder.toJobParameters();

            log.info("Launching Oracle-to-Oracle ETL job with parameters: {}", jobParameters);

            try {
                var jobExecution = jobLauncher.run(importEmployeeJob, jobParameters);
                log.info("Job execution completed with status: {}", jobExecution.getStatus());
            } catch (Exception e) {
                log.error("Job execution failed", e);
                throw e;
            }
        };
    }
}
