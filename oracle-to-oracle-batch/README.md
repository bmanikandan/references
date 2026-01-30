# Spring Boot Batch - Oracle to Oracle

A production-ready Spring Boot Batch application that reads employee data from a **source Oracle database** and performs upsert operations into a **target Oracle database**, using an **in-memory H2 JobRepository** for batch metadata.

## Features

- **Oracle-to-Oracle ETL**: Reads from source Oracle, writes to target Oracle
- **In-Memory JobRepository**: H2 database for Spring Batch metadata (no persistent batch tables needed in Oracle)
- **JDBC Cursor Reader**: Efficient cursor-based reading for large datasets
- **MERGE (Upsert) Operations**: Insert if new, update if exists
- **Data Validation**: Jakarta Validation for input validation
- **Data Transformation**: Automatic formatting (capitalization, email normalization, status mapping)
- **Fault Tolerance**: Configurable skip limits for handling bad records
- **Comprehensive Logging**: Job and step listeners for detailed execution tracking
- **Multiple Execution Modes**: CLI or REST API execution
- **Configurable Source Query**: Custom SQL queries via job parameters

## Architecture

```
┌─────────────────────┐     ┌─────────────────┐     ┌─────────────────────┐
│   Source Oracle     │     │    Processor    │     │   Target Oracle     │
│  (JdbcCursor        │────▶│  (Validation +  │────▶│  (JdbcBatch         │
│   Reader)           │     │   Transform)    │     │   Writer - MERGE)   │
└─────────────────────┘     └─────────────────┘     └─────────────────────┘
                                    │
                         ┌──────────┴──────────┐
                         │  H2 In-Memory DB    │
                         │  (JobRepository)    │
                         └─────────────────────┘
```

## Prerequisites

- Java 21+
- Gradle 8.x (or use included wrapper)
- Two Oracle Database instances (Source and Target)

## Configuration

### Application Properties

Edit `src/main/resources/application.yml`:

```yaml
# Source Oracle Database
source:
  datasource:
    url: jdbc:oracle:thin:@//source-host:1521/SOURCEDB
    username: source_user
    password: source_password

# Target Oracle Database  
target:
  datasource:
    url: jdbc:oracle:thin:@//target-host:1521/TARGETDB
    username: target_user
    password: target_password

# Batch Settings
batch:
  chunk-size: 100    # Records per transaction
  skip-limit: 10     # Max records to skip on errors
  source:
    query: >
      SELECT employee_id, first_name, last_name, email, 
             department, salary, hire_date, status 
      FROM employees 
      WHERE status = 'ACTIVE'
```

### Environment Variables

```bash
# Source Database
export SOURCE_ORACLE_USERNAME=source_user
export SOURCE_ORACLE_PASSWORD=source_password

# Target Database
export TARGET_ORACLE_USERNAME=target_user
export TARGET_ORACLE_PASSWORD=target_password

# Batch Settings
export CHUNK_SIZE=500
export SKIP_LIMIT=50
```

## Database Setup

Run the DDL scripts on respective Oracle databases:

### Source Database

```sql
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

### Target Database

Same table structure as source. See `src/main/resources/schema-oracle.sql` for complete DDL including indexes and triggers.

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
# Using default source query from application.yml
java -jar build/libs/oracle-to-oracle-batch.jar --spring.profiles.active=cli

# With custom source query
java -jar build/libs/oracle-to-oracle-batch.jar --spring.profiles.active=cli \
  "SELECT * FROM employees WHERE department = 'Engineering'"

# Or using Gradle bootRun
./gradlew bootRun --args='--spring.profiles.active=cli'
```

### Run with REST API

```bash
java -jar build/libs/oracle-to-oracle-batch.jar --spring.profiles.active=web

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

**Start Job with Default Query:**

```bash
curl -X POST "http://localhost:8080/api/batch/jobs/import-employees/start"
```

**Start Job with Custom Query:**

```bash
curl -X POST "http://localhost:8080/api/batch/jobs/import-employees/start" \
  --data-urlencode "customQuery=SELECT * FROM employees WHERE hire_date > DATE '2023-01-01'"
```

**Check Status:**

```bash
curl "http://localhost:8080/api/batch/jobs/executions/1"
```

## In-Memory JobRepository

This application uses an **in-memory H2 database** for Spring Batch metadata instead of persisting to either Oracle database. Benefits:

- **No Oracle Schema Pollution**: Batch tables (BATCH_JOB_*, BATCH_STEP_*) stay in H2
- **Faster Metadata Operations**: In-memory is faster than disk-based Oracle
- **Simpler Deployment**: No need for batch DDL in production Oracle databases
- **Clean Separation**: Business data in Oracle, batch metadata in H2

### Trade-offs

- Job history is lost on application restart
- Cannot resume failed jobs after restart
- Not suitable for clustered batch execution

For persistent job metadata, modify `DataSourceConfig` to use one of the Oracle databases for batch metadata.

## Data Flow

1. **Read**: `JdbcCursorItemReader` fetches records from source Oracle using configured SQL query
2. **Process**: `EmployeeProcessor` validates and transforms each record
3. **Write**: `JdbcBatchItemWriter` performs MERGE (upsert) into target Oracle

### Source Query Customization

The default query is configured in `application.yml`. You can override it:

- Via job parameter `customQuery` (REST API or CLI argument)
- Column names in SELECT must match `Employee` field names (using snake_case to camelCase mapping)

**Required columns:**
- `employee_id` → `employeeId`
- `first_name` → `firstName`
- `last_name` → `lastName`
- `email` → `email`
- `department` → `department`
- `salary` → `salary`
- `hire_date` → `hireDate`
- `status` → `status`

## Error Handling

### Skip Policy

Bad records are skipped (up to `skip-limit`) for:
- `IllegalArgumentException`: Validation failures (missing required fields, invalid data)

### Monitoring Skipped Records

Skipped records are logged with details:

```
WARN  Skip #1 during PROCESS - Item: Employee(employeeId=EMP099...) - Error: Validation failed: salary must be positive
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
│   ├── DataSourceConfig.java      # Triple datasource configuration (H2, Source, Target)
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

### Chunk Size & Fetch Size

The reader's `fetchSize` matches `chunk-size` for optimal performance:

- **Small datasets (<1000 rows)**: chunk-size=50-100
- **Medium datasets (1000-100000)**: chunk-size=500-1000
- **Large datasets (>100000)**: chunk-size=1000-5000

### Connection Pool

```yaml
source:
  datasource:
    hikari:
      maximum-pool-size: 10     # Read operations
      read-only: true           # Enforced read-only

target:
  datasource:
    hikari:
      maximum-pool-size: 20     # Increase for write parallelism
```

## Troubleshooting

### Common Issues

**1. Oracle Connection Refused**
```
Verify: url, username, password, firewall rules, listener status for BOTH databases
```

**2. Column Mapping Errors**
```
Ensure SELECT column names match Employee fields (snake_case → camelCase)
```

**3. MERGE Statement Failures**
```
Check target table structure matches expected schema
Verify employee_id uniqueness constraint exists
```

**4. Memory Issues with Large Datasets**
```
Increase heap: java -Xmx2g -jar build/libs/oracle-to-oracle-batch.jar
Reduce chunk-size to lower memory footprint
```

**5. Slow Performance**
```
Increase chunk-size for fewer commits
Add indexes on source table for WHERE clause columns
Check network latency between app server and Oracle databases
```

## License

MIT License
