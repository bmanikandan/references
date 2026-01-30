# Spring Boot Batch - CSV to Oracle

A production-ready Spring Boot Batch application that reads employee data from CSV files and performs upsert operations into an Oracle database, using an **in-memory H2 JobRepository** for batch metadata.

## Features

- **CSV File Processing**: Reads employee data from CSV files with configurable field mapping
- **Oracle Database Integration**: Uses MERGE (upsert) operations for insert/update logic
- **In-Memory JobRepository**: H2 database for Spring Batch metadata (no persistent batch tables needed)
- **Data Validation**: Jakarta Validation for input validation
- **Data Transformation**: Automatic formatting (capitalization, email normalization, status mapping)
- **Fault Tolerance**: Configurable skip limits for handling bad records
- **Comprehensive Logging**: Job and step listeners for detailed execution tracking
- **Multiple Execution Modes**: CLI or REST API execution

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   CSV Reader    │────▶│   Processor     │────▶│  Oracle Writer  │
│  (FlatFile)     │     │  (Validation +  │     │  (JDBC MERGE)   │
│                 │     │  Transform)     │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                        │
         └──────────────────────┴────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │  H2 In-Memory DB    │
                    │  (JobRepository)    │
                    └─────────────────────┘
```

## Prerequisites

- Java 21+
- Gradle 8.x (or use included wrapper)
- Oracle Database (11g or higher)

## Configuration

### Application Properties

Edit `src/main/resources/application.yml`:

```yaml
spring:
  datasource:
    oracle:
      url: jdbc:oracle:thin:@//your-host:1521/your-service
      username: your_username
      password: your_password

batch:
  input:
    file: classpath:data/input.csv  # or file:/path/to/file.csv
  chunk-size: 100    # Records per transaction
  skip-limit: 10     # Max records to skip on errors
```

### Environment Variables

```bash
export ORACLE_USERNAME=batch_user
export ORACLE_PASSWORD=secure_password
export INPUT_FILE=file:/data/employees.csv
export CHUNK_SIZE=500
export SKIP_LIMIT=50
```

## Database Setup

Run the Oracle DDL script to create the required table:

```sql
-- See src/main/resources/schema-oracle.sql
CREATE TABLE employees (
    id              NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id     VARCHAR2(50) NOT NULL UNIQUE,
    first_name      VARCHAR2(100) NOT NULL,
    last_name       VARCHAR2(100) NOT NULL,
    email           VARCHAR2(255),
    department      VARCHAR2(100),
    salary          NUMBER(12, 2),
    hire_date       DATE,
    status          VARCHAR2(20) DEFAULT 'ACTIVE',
    created_at      TIMESTAMP DEFAULT SYSTIMESTAMP,
    updated_at      TIMESTAMP DEFAULT SYSTIMESTAMP
);
```

## CSV Format

```csv
employeeId,firstName,lastName,email,department,salary,hireDate,status
EMP001,john,doe,john.doe@example.com,Engineering,75000.00,2020-01-15,ACTIVE
EMP002,jane,smith,jane.smith@example.com,Marketing,68000.00,2019-06-20,A
```

### Status Mappings

| Input Values | Normalized Status |
|--------------|-------------------|
| A, ACTIVE, 1 | ACTIVE |
| I, INACTIVE, 0 | INACTIVE |
| T, TERMINATED | TERMINATED |
| L, LEAVE | ON_LEAVE |
| (empty/null) | ACTIVE |

## Build & Run

### Initial Setup (if gradle-wrapper.jar is missing)

```bash
# Option 1: Use system Gradle to generate wrapper
gradle wrapper --gradle-version 8.12

# Option 2: Or just use system Gradle directly
gradle clean build -x test
```

### Build

```bash
./gradlew clean build -x test
```

### Run via Command Line

```bash
# Using default input file
java -jar build/libs/spring-batch-csv-oracle.jar --spring.profiles.active=cli

# With custom input file
java -jar build/libs/spring-batch-csv-oracle.jar --spring.profiles.active=cli /path/to/employees.csv

# Or using Gradle bootRun
./gradlew bootRun --args='--spring.profiles.active=cli'
```

### Run with REST API

```bash
java -jar build/libs/spring-batch-csv-oracle.jar --spring.profiles.active=web

# Or using Gradle
./gradlew bootRun --args='--spring.profiles.active=web'
```

#### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/batch/jobs/import-employees/start` | Start job execution |
| GET | `/api/batch/jobs/executions/{id}` | Get execution status |
| GET | `/api/batch/jobs/running` | List running jobs |
| POST | `/api/batch/jobs/executions/{id}/stop` | Stop a running job |

**Start Job Example:**

```bash
curl -X POST "http://localhost:8080/api/batch/jobs/import-employees/start?inputFile=classpath:data/input.csv"
```

**Check Status:**

```bash
curl "http://localhost:8080/api/batch/jobs/executions/1"
```

## In-Memory JobRepository

This application uses an **in-memory H2 database** for Spring Batch metadata instead of persisting to Oracle. Benefits:

- **No Oracle Schema Pollution**: Batch tables (BATCH_JOB_*, BATCH_STEP_*) stay in H2
- **Faster Metadata Operations**: In-memory is faster than disk-based Oracle
- **Simpler Deployment**: No need for batch DDL in production Oracle

### Trade-offs

- Job history is lost on application restart
- Cannot resume failed jobs after restart
- Not suitable for clustered batch execution

For persistent job metadata, modify `DataSourceConfig` to use Oracle for both datasources.

## Error Handling

### Skip Policy

Bad records are skipped (up to `skip-limit`) for:
- `FlatFileParseException`: Malformed CSV lines
- `IllegalArgumentException`: Validation failures

### Monitoring Skipped Records

Skipped records are logged with details:

```
WARN  Skip #1 during READ - Line 15: Parsing error - Input: 'BAD,DATA,HERE'
WARN  Skip #2 during PROCESS - Item: Employee(employeeId=EMP099...) - Error: Validation failed
```

## Testing

```bash
# Run all tests
./gradlew test

# Run with test report
./gradlew test jacocoTestReport
```

## Project Structure

```
src/main/java/com/example/batch/
├── BatchApplication.java           # Main application
├── config/
│   ├── BatchConfig.java           # Job, Step, Reader, Writer beans
│   ├── DataSourceConfig.java      # Dual datasource configuration
│   ├── JobLauncherConfig.java     # CLI job launcher
│   └── BatchJobController.java    # REST API controller
├── model/
│   └── Employee.java              # Data model with validation
├── processor/
│   └── EmployeeProcessor.java     # Validation & transformation
└── listener/
    ├── JobCompletionNotificationListener.java
    └── StepExecutionNotificationListener.java
```

## Performance Tuning

### Chunk Size

Adjust based on your data:
- **Small datasets (<1000 rows)**: chunk-size=50-100
- **Medium datasets (1000-100000)**: chunk-size=500-1000
- **Large datasets (>100000)**: chunk-size=1000-5000

### Connection Pool

```yaml
spring:
  datasource:
    oracle:
      hikari:
        maximum-pool-size: 20      # Increase for parallel processing
        minimum-idle: 5
```

## Troubleshooting

### Common Issues

**1. Oracle Connection Refused**
```
Verify: url, username, password, firewall rules, listener status
```

**2. CSV Parse Errors**
```
Check: encoding (UTF-8), delimiter, date format (yyyy-MM-dd)
```

**3. Memory Issues with Large Files**
```
Increase heap: java -Xmx2g -jar build/libs/spring-batch-csv-oracle.jar
Reduce chunk-size if needed
```

## License

MIT License
