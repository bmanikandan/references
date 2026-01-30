-- Oracle DDL for Employees Table
-- Run this script to create the required table structure

-- Drop existing table (if needed for clean setup)
-- DROP TABLE employees CASCADE CONSTRAINTS;

-- Create employees table
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

-- Create indexes for common queries
CREATE INDEX idx_emp_department ON employees(department);
CREATE INDEX idx_emp_status ON employees(status);
CREATE INDEX idx_emp_hire_date ON employees(hire_date);

-- Create trigger to auto-update updated_at timestamp
CREATE OR REPLACE TRIGGER trg_employees_updated_at
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    :NEW.updated_at := SYSTIMESTAMP;
END;
/

-- Add comments for documentation
COMMENT ON TABLE employees IS 'Employee master data imported from CSV batch processing';
COMMENT ON COLUMN employees.employee_id IS 'Unique business identifier for employee';
COMMENT ON COLUMN employees.status IS 'Employee status: ACTIVE, INACTIVE, TERMINATED, ON_LEAVE';

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON employees TO batch_user;

-- Verify table creation
SELECT table_name, num_rows 
FROM user_tables 
WHERE table_name = 'EMPLOYEES';
