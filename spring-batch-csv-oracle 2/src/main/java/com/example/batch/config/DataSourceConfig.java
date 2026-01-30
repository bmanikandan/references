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
 * - Oracle: Business data persistence
 */
@Configuration
public class DataSourceConfig {

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

    /**
     * Oracle DataSource properties for business data.
     */
    @Bean
    @ConfigurationProperties("spring.datasource.oracle")
    public DataSourceProperties oracleDataSourceProperties() {
        return new DataSourceProperties();
    }

    /**
     * Oracle DataSource for business data operations.
     */
    @Bean
    public DataSource oracleDataSource() {
        HikariDataSource dataSource = oracleDataSourceProperties()
                .initializeDataSourceBuilder()
                .type(HikariDataSource.class)
                .build();
        dataSource.setPoolName("OracleHikariPool");
        dataSource.setMaximumPoolSize(10);
        dataSource.setMinimumIdle(5);
        return dataSource;
    }

    /**
     * JdbcTemplate for Oracle database operations.
     */
    @Bean
    public JdbcTemplate oracleJdbcTemplate(@Qualifier("oracleDataSource") DataSource oracleDataSource) {
        return new JdbcTemplate(oracleDataSource);
    }
}
