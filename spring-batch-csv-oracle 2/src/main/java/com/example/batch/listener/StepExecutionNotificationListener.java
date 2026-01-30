package com.example.batch.listener;

import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.ExitStatus;
import org.springframework.batch.core.StepExecution;
import org.springframework.batch.core.StepExecutionListener;
import org.springframework.batch.core.annotation.OnSkipInProcess;
import org.springframework.batch.core.annotation.OnSkipInRead;
import org.springframework.batch.core.annotation.OnSkipInWrite;
import org.springframework.batch.item.file.FlatFileParseException;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * Listener for step-level events and skip handling.
 */
@Slf4j
@Component
public class StepExecutionNotificationListener implements StepExecutionListener {

    private final AtomicInteger skipCount = new AtomicInteger(0);

    @Override
    public void beforeStep(StepExecution stepExecution) {
        skipCount.set(0);
        log.info("Starting step: {}", stepExecution.getStepName());
    }

    @Override
    public ExitStatus afterStep(StepExecution stepExecution) {
        log.info("Step '{}' finished with status: {}",
                stepExecution.getStepName(),
                stepExecution.getStatus());

        log.info("Step Statistics - Read: {}, Written: {}, Skipped: {}, Filtered: {}",
                stepExecution.getReadCount(),
                stepExecution.getWriteCount(),
                stepExecution.getSkipCount(),
                stepExecution.getFilterCount());

        if (stepExecution.getSkipCount() > 0) {
            log.warn("Total records skipped during step: {}", stepExecution.getSkipCount());
        }

        return stepExecution.getExitStatus();
    }

    @OnSkipInRead
    public void onSkipInRead(Throwable t) {
        int count = skipCount.incrementAndGet();
        if (t instanceof FlatFileParseException parseException) {
            log.warn("Skip #{} during READ - Line {}: {} - Input: '{}'",
                    count,
                    parseException.getLineNumber(),
                    parseException.getMessage(),
                    parseException.getInput());
        } else {
            log.warn("Skip #{} during READ: {}", count, t.getMessage());
        }
    }

    @OnSkipInProcess
    public void onSkipInProcess(Object item, Throwable t) {
        int count = skipCount.incrementAndGet();
        log.warn("Skip #{} during PROCESS - Item: {} - Error: {}",
                count, item, t.getMessage());
    }

    @OnSkipInWrite
    public void onSkipInWrite(Object item, Throwable t) {
        int count = skipCount.incrementAndGet();
        log.warn("Skip #{} during WRITE - Item: {} - Error: {}",
                count, item, t.getMessage());
    }
}
