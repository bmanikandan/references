import org.springframework.context.annotation.Configuration;
import org.springframework.data.r2dbc.repository.config.EnableR2dbcRepositories;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * R2DBC Configuration for Oracle Database.
 * 
 * Connection settings are primarily configured via application.yml/properties.
 * This class enables R2DBC repositories and transaction management.
 */
@Configuration
@EnableR2dbcRepositories(basePackages = "com.example.pdfdownload.repository")
@EnableTransactionManagement
public class DatabaseConfig {
    // Spring Boot auto-configuration handles ConnectionFactory setup
    // based on spring.r2dbc.url property in application.yml
}
