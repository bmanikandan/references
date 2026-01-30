-- ============================================================
-- Oracle DDL for Source and Target Employees Tables
-- Run appropriate scripts on respective Oracle databases
-- ============================================================

-- ============================================================
-- SOURCE DATABASE DDL
-- Run this on the SOURCE Oracle database
-- ============================================================

-- Create source employees table
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

-- Create indexes for source queries
CREATE INDEX idx_src_emp_status ON employees(status);
CREATE INDEX idx_src_emp_department ON employees(department);

-- Sample data for source database (optional)
INSERT INTO employees (employee_id, first_name, last_name, email, department, salary, hire_date, status)
VALUES ('EMP001', 'John', 'Doe', 'john.doe@example.com', 'Engineering', 75000.00, DATE '2020-01-15', 'ACTIVE');

INSERT INTO employees (employee_id, first_name, last_name, email, department, salary, hire_date, status)
VALUES ('EMP002', 'Jane', 'Smith', 'jane.smith@example.com', 'Marketing', 68000.00, DATE '2019-06-20', 'ACTIVE');

INSERT INTO employees (employee_id, first_name, last_name, email, department, salary, hire_date, status)
VALUES ('EMP003', 'Bob', 'Wilson', 'bob.wilson@example.com', 'Sales', 72000.00, DATE '2021-03-10', 'ACTIVE');

COMMIT;


-- ============================================================
-- TARGET DATABASE DDL
-- Run this on the TARGET Oracle database
-- ============================================================

-- Create target employees table
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

-- Create indexes for target queries
CREATE INDEX idx_tgt_emp_department ON employees(department);
CREATE INDEX idx_tgt_emp_status ON employees(status);
CREATE INDEX idx_tgt_emp_hire_date ON employees(hire_date);

-- Create trigger to auto-update updated_at timestamp
CREATE OR REPLACE TRIGGER trg_employees_updated_at
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    :NEW.updated_at := SYSTIMESTAMP;
END;
/

-- Add comments for documentation
COMMENT ON TABLE employees IS 'Employee data synchronized from source database via batch processing';
COMMENT ON COLUMN employees.employee_id IS 'Unique business identifier for employee (from source)';
COMMENT ON COLUMN employees.status IS 'Employee status: ACTIVE, INACTIVE, TERMINATED, ON_LEAVE';

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON employees TO batch_user;

-- Verify table creation
SELECT table_name, num_rows 
FROM user_tables 
WHERE table_name = 'EMPLOYEES';
