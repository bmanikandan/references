package com.example.batch.config;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.*;
import org.springframework.batch.core.explore.JobExplorer;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.batch.core.launch.JobOperator;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.context.annotation.Profile;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * REST API for batch job management.
 * Active when 'web' profile is enabled.
 */
@Slf4j
@RestController
@RequestMapping("/api/batch")
@RequiredArgsConstructor
@Profile("web")
public class BatchJobController {

    private final JobLauncher jobLauncher;
    private final Job importEmployeeJob;
    private final JobExplorer jobExplorer;
    private final JobRepository jobRepository;

    /**
     * Start a new job execution.
     */
    @PostMapping("/jobs/import-employees/start")
    public ResponseEntity<Map<String, Object>> startJob(
            @RequestParam(required = false, defaultValue = "classpath:data/input.csv") String inputFile) {

        Map<String, Object> response = new HashMap<>();

        try {
            JobParameters jobParameters = new JobParametersBuilder()
                    .addString("inputFile", inputFile)
                    .addLocalDateTime("startTime", LocalDateTime.now())
                    .toJobParameters();

            JobExecution execution = jobLauncher.run(importEmployeeJob, jobParameters);

            response.put("status", "STARTED");
            response.put("jobId", execution.getJobId());
            response.put("executionId", execution.getId());
            response.put("startTime", execution.getStartTime());

            log.info("Job started: executionId={}", execution.getId());
            return ResponseEntity.accepted().body(response);

        } catch (Exception e) {
            log.error("Failed to start job", e);
            response.put("status", "FAILED");
            response.put("error", e.getMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }

    /**
     * Get job execution status by ID.
     */
    @GetMapping("/jobs/executions/{executionId}")
    public ResponseEntity<Map<String, Object>> getJobStatus(@PathVariable Long executionId) {
        JobExecution execution = jobExplorer.getJobExecution(executionId);

        if (execution == null) {
            return ResponseEntity.notFound().build();
        }

        Map<String, Object> response = new HashMap<>();
        response.put("jobId", execution.getJobId());
        response.put("executionId", execution.getId());
        response.put("jobName", execution.getJobInstance().getJobName());
        response.put("status", execution.getStatus());
        response.put("exitStatus", execution.getExitStatus().getExitCode());
        response.put("startTime", execution.getStartTime());
        response.put("endTime", execution.getEndTime());

        // Add step execution details
        execution.getStepExecutions().forEach(step -> {
            Map<String, Object> stepInfo = new HashMap<>();
            stepInfo.put("stepName", step.getStepName());
            stepInfo.put("status", step.getStatus());
            stepInfo.put("readCount", step.getReadCount());
            stepInfo.put("writeCount", step.getWriteCount());
            stepInfo.put("skipCount", step.getSkipCount());
            response.put("step_" + step.getStepName(), stepInfo);
        });

        return ResponseEntity.ok(response);
    }

    /**
     * Get all running job executions.
     */
    @GetMapping("/jobs/running")
    public ResponseEntity<Map<String, Object>> getRunningJobs() {
        Set<JobExecution> runningExecutions = jobExplorer.findRunningJobExecutions("importEmployeeJob");

        Map<String, Object> response = new HashMap<>();
        response.put("count", runningExecutions.size());
        response.put("executions", runningExecutions.stream()
                .map(exec -> Map.of(
                        "executionId", exec.getId(),
                        "startTime", exec.getStartTime(),
                        "status", exec.getStatus()
                ))
                .toList());

        return ResponseEntity.ok(response);
    }

    /**
     * Stop a running job execution.
     */
    @PostMapping("/jobs/executions/{executionId}/stop")
    public ResponseEntity<Map<String, Object>> stopJob(@PathVariable Long executionId) {
        JobExecution execution = jobExplorer.getJobExecution(executionId);

        if (execution == null) {
            return ResponseEntity.notFound().build();
        }

        Map<String, Object> response = new HashMap<>();

        if (!execution.isRunning()) {
            response.put("status", "NOT_RUNNING");
            response.put("message", "Job is not currently running");
            return ResponseEntity.badRequest().body(response);
        }

        execution.setStatus(BatchStatus.STOPPING);
        jobRepository.update(execution);

        response.put("status", "STOPPING");
        response.put("executionId", executionId);
        return ResponseEntity.ok(response);
    }
}
