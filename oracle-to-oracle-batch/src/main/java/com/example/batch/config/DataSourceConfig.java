package com.example.batch.config;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.jdbc.DataSourceProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.sql.DataSource;

/**
 * Configuration for multiple DataSources:
 * - Primary (H2): In-memory database for Spring Batch JobRepository metadata
 * - Source Oracle: Read-only connection to source database
 * - Target Oracle: Write connection to target database
 */
@Configuration
public class DataSourceConfig {

    // ==================== H2 In-Memory (JobRepository) ====================

    /**
     * H2 DataSource properties for in-memory JobRepository.
     */
    @Bean
    @Primary
    @ConfigurationProperties("spring.datasource")
    public DataSourceProperties batchDataSourceProperties() {
        return new DataSourceProperties();
    }

    /**
     * Primary H2 DataSource for Spring Batch metadata (JobRepository).
     * Using @Primary makes this the default for Spring Batch infrastructure.
     */
    @Bean
    @Primary
    public DataSource batchDataSource() {
        return batchDataSourceProperties()
                .initializeDataSourceBuilder()
                .type(HikariDataSource.class)
                .build();
    }

    // ==================== Source Oracle Database ====================

    /**
     * Source Oracle DataSource properties.
     */
    @Bean
    @ConfigurationProperties("source.datasource")
    public DataSourceProperties sourceDataSourceProperties() {
        return new DataSourceProperties();
    }

    /**
     * Source Oracle DataSource for reading data.
     * Configured as read-only for safety.
     */
    @Bean
    public DataSource sourceDataSource() {
        HikariDataSource dataSource = sourceDataSourceProperties()
                .initializeDataSourceBuilder()
                .type(HikariDataSource.class)
                .build();
        dataSource.setPoolName("SourceOracleHikariPool");
        dataSource.setMaximumPoolSize(10);
        dataSource.setMinimumIdle(5);
        dataSource.setReadOnly(true); // Read-only for source
        return dataSource;
    }

    /**
     * JdbcTemplate for source Oracle database operations.
     */
    @Bean
    public JdbcTemplate sourceJdbcTemplate(@Qualifier("sourceDataSource") DataSource sourceDataSource) {
        return new JdbcTemplate(sourceDataSource);
    }

    // ==================== Target Oracle Database ====================

    /**
     * Target Oracle DataSource properties.
     */
    @Bean
    @ConfigurationProperties("target.datasource")
    public DataSourceProperties targetDataSourceProperties() {
        return new DataSourceProperties();
    }

    /**
     * Target Oracle DataSource for writing data.
     */
    @Bean
    public DataSource targetDataSource() {
        HikariDataSource dataSource = targetDataSourceProperties()
                .initializeDataSourceBuilder()
                .type(HikariDataSource.class)
                .build();
        dataSource.setPoolName("TargetOracleHikariPool");
        dataSource.setMaximumPoolSize(10);
        dataSource.setMinimumIdle(5);
        return dataSource;
    }

    /**
     * JdbcTemplate for target Oracle database operations.
     */
    @Bean
    public JdbcTemplate targetJdbcTemplate(@Qualifier("targetDataSource") DataSource targetDataSource) {
        return new JdbcTemplate(targetDataSource);
    }
}
