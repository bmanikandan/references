package com.example.batch.listener;

import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.BatchStatus;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobExecutionListener;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.LocalDateTime;

/**
 * Listener for job-level events.
 * Logs job start/completion and provides summary statistics.
 */
@Slf4j
@Component
public class JobCompletionNotificationListener implements JobExecutionListener {

    private final JdbcTemplate sourceJdbcTemplate;
    private final JdbcTemplate targetJdbcTemplate;

    public JobCompletionNotificationListener(
            @Qualifier("sourceJdbcTemplate") JdbcTemplate sourceJdbcTemplate,
            @Qualifier("targetJdbcTemplate") JdbcTemplate targetJdbcTemplate) {
        this.sourceJdbcTemplate = sourceJdbcTemplate;
        this.targetJdbcTemplate = targetJdbcTemplate;
    }

    @Override
    public void beforeJob(JobExecution jobExecution) {
        log.info("========================================");
        log.info("JOB STARTED: {}", jobExecution.getJobInstance().getJobName());
        log.info("Job ID: {}", jobExecution.getJobId());
        log.info("Start Time: {}", jobExecution.getStartTime());
        log.info("Job Parameters: {}", jobExecution.getJobParameters());
        log.info("========================================");

        // Log source database record count
        logSourceDatabaseInfo();
    }

    @Override
    public void afterJob(JobExecution jobExecution) {
        Duration duration = Duration.between(
                jobExecution.getStartTime(),
                jobExecution.getEndTime() != null ? jobExecution.getEndTime() : LocalDateTime.now()
        );

        log.info("========================================");
        log.info("JOB COMPLETED: {}", jobExecution.getJobInstance().getJobName());
        log.info("Job ID: {}", jobExecution.getJobId());
        log.info("Status: {}", jobExecution.getStatus());
        log.info("Exit Status: {}", jobExecution.getExitStatus());
        log.info("Duration: {} seconds", duration.toSeconds());

        // Log step summaries
        jobExecution.getStepExecutions().forEach(stepExecution -> {
            log.info("--- Step: {} ---", stepExecution.getStepName());
            log.info("    Read: {}", stepExecution.getReadCount());
            log.info("    Written: {}", stepExecution.getWriteCount());
            log.info("    Skipped: {}", stepExecution.getSkipCount());
            log.info("    Filtered: {}", stepExecution.getFilterCount());
        });

        if (jobExecution.getStatus() == BatchStatus.COMPLETED) {
            log.info("Job completed successfully!");
            logTargetDatabaseSummary();
        } else if (jobExecution.getStatus() == BatchStatus.FAILED) {
            log.error("Job FAILED!");
            jobExecution.getAllFailureExceptions().forEach(ex ->
                    log.error("Failure exception: {}", ex.getMessage(), ex)
            );
        }

        log.info("========================================");
    }

    private void logSourceDatabaseInfo() {
        try {
            Integer sourceCount = sourceJdbcTemplate.queryForObject(
                    "SELECT COUNT(*) FROM employees WHERE status = 'ACTIVE'", Integer.class);
            log.info("Source database - Active employees to process: {}", sourceCount);
        } catch (Exception e) {
            log.warn("Could not retrieve source database info: {}", e.getMessage());
        }
    }

    private void logTargetDatabaseSummary() {
        try {
            Integer totalCount = targetJdbcTemplate.queryForObject(
                    "SELECT COUNT(*) FROM employees", Integer.class);
            log.info("Target database - Total employees: {}", totalCount);

            Integer activeCount = targetJdbcTemplate.queryForObject(
                    "SELECT COUNT(*) FROM employees WHERE status = 'ACTIVE'", Integer.class);
            log.info("Target database - Active employees: {}", activeCount);
        } catch (Exception e) {
            log.warn("Could not retrieve target database summary: {}", e.getMessage());
        }
    }
}
