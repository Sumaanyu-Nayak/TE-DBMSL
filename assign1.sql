
-- -- =============================================
-- -- 1. DROP TABLES IF THEY EXIST (Reverse Order)
-- -- =============================================

-- DROP TABLE IF EXISTS Manages;
-- DROP TABLE IF EXISTS Works;
-- DROP TABLE IF EXISTS Company;
-- DROP TABLE IF EXISTS Employee;

-- -- =============================================
-- -- 2. CREATE TABLES
-- -- =============================================

-- -- Employee Table
-- CREATE TABLE Employee (
--     e_id INT PRIMARY KEY AUTO_INCREMENT,
--     name VARCHAR(50),
--     street VARCHAR(100),
--     city VARCHAR(50),
--     phone VARCHAR(15)
-- );

-- -- Company Table
-- CREATE TABLE Company (
--     company_name VARCHAR(50) PRIMARY KEY,
--     city VARCHAR(50)
-- );

-- -- Works Table
-- CREATE TABLE Works (
--     e_id INT,
--     company_name VARCHAR(50),
--     salary INT,
--     PRIMARY KEY (e_id, company_name),
--     FOREIGN KEY (e_id) REFERENCES Employee(e_id),
--     FOREIGN KEY (company_name) REFERENCES Company(company_name)
-- );

-- -- Manages Table
-- CREATE TABLE Manages (
--     e_id INT PRIMARY KEY,
--     dept_name VARCHAR(50),
--     FOREIGN KEY (e_id) REFERENCES Employee(e_id)
-- );

-- -- =============================================
-- -- 3. INSERT DATA (20 Queries Total)
-- -- =============================================

-- -- Insert 10 Employees (explicit IDs for clarity)
-- INSERT INTO Employee (e_id, name, street, city, phone) VALUES
-- (1, 'Aman Sharma', 'MG Road', 'Delhi', '9999000001'),
-- (2, 'Riya Sen', 'Park Street', 'Kolkata', '9999000002'),
-- (3, 'Kabir Mehta', 'Brigade Road', 'Bangalore', '9999000003'),
-- (4, 'Sneha Kapoor', 'Sector 21', 'Chandigarh', '9999000004'),
-- (5, 'Vikas Yadav', 'Banjara Hills', 'Hyderabad', '9999000005'),
-- (6, 'Priya Nair', 'Churchgate', 'Mumbai', '9999000006'),
-- (7, 'Dev Patel', 'Kalyani Nagar', 'Pune', '9999000007'),
-- (8, 'Meera Iyer', 'Anna Nagar', 'Chennai', '9999000008'),
-- (9, 'Raj Verma', 'Sector 62', 'Noida', '9999000009'),
-- (10, 'Neha Gupta', 'Salt Lake', 'Kolkata', '9999000010');

-- -- Insert 5 Companies
-- INSERT INTO Company VALUES
-- ('ABC', 'Delhi'),
-- ('XYZ', 'Mumbai'),
-- ('PQR', 'Bangalore'),
-- ('LMN', 'Hyderabad'),
-- ('OPQ', 'Chennai');

-- -- Insert 10 Works entries
-- INSERT INTO Works VALUES
-- (1, 'ABC', 45000),
-- (2, 'ABC', 52000),
-- (3, 'XYZ', 60000),
-- (4, 'PQR', 48000),
-- (5, 'LMN', 70000),
-- (6, 'OPQ', 55000),
-- (7, 'ABC', 75000),
-- (8, 'XYZ', 50000),
-- (9, 'LMN', 65000),
-- (10, 'ABC', 80000);

-- -- Insert 5 Manages entries
-- INSERT INTO Manages VALUES
-- (1, 'HR'),
-- (2, 'Sales'),
-- (3, 'Marketing'),
-- (4, 'Finance'),
-- (5, 'IT');

-- -- =============================================
-- -- 4. UPDATE PHONE FOR AN EMPLOYEE
-- -- =============================================
-- UPDATE Employee
-- SET phone = '9876543210'
-- WHERE e_id = 1;

-- -- =============================================
-- -- 5. VIEWS (ABC employees, salary > 50000, rename workaround)
-- -- =============================================

-- -- Drop old views (if exist)
-- DROP VIEW IF EXISTS ABC_Employees;
-- DROP VIEW IF EXISTS ABC_Employees_HighSalary;

-- -- Create view for ABC company employees
-- CREATE VIEW ABC_Employees AS
-- SELECT E.e_id, E.name, E.street, E.city
-- FROM Employee E
-- JOIN Works W ON E.e_id = W.e_id
-- WHERE W.company_name = 'ABC';

-- -- Replace with new view for salary > 50000
-- DROP VIEW IF EXISTS ABC_Employees;
-- CREATE VIEW ABC_Employees AS
-- SELECT E.e_id, E.name, E.street, E.city
-- FROM Employee E
-- JOIN Works W ON E.e_id = W.e_id
-- WHERE W.company_name = 'ABC' AND W.salary > 50000;

-- -- Rename view: workaround (MySQL doesn’t support ALTER VIEW RENAME)
-- -- Simulate rename by copying
-- CREATE VIEW ABC_Employees_HighSalary AS
-- SELECT * FROM ABC_Employees;
-- DROP VIEW ABC_Employees;

-- -- =============================================
-- -- 6. DML ON VIEWS (Handled through base tables)
-- -- =============================================

-- -- Insert new employee (not through view; through base tables)
-- INSERT INTO Employee (e_id, name, street, city, phone)
-- VALUES (11, 'Prashant Mishra', 'Golf Course Road', 'Gurgaon', '9988776655');

-- INSERT INTO Works (e_id, company_name, salary)
-- VALUES (11, 'ABC', 60000);

-- -- Update salary
-- UPDATE Works
-- SET salary = 65000
-- WHERE e_id = 2 AND company_name = 'ABC';

-- -- Delete entry
-- DELETE FROM Works
-- WHERE e_id = 11 AND company_name = 'ABC';

-- -- =============================================
-- -- 7. INDEX CREATION AND DELETION
-- -- =============================================

-- -- Create index on Employee.city and Company.city
-- CREATE INDEX idx_employee_city ON Employee(city);
-- CREATE INDEX idx_company_city ON Company(city);

-- -- Drop indexes (MySQL/MariaDB doesn't support ALTER INDEX)
-- DROP INDEX idx_employee_city ON Employee;
-- DROP INDEX idx_company_city ON Company;

-- -- =============================================
-- -- 8. SIMULATING SEQUENCES IN MYSQL/MARIADB
-- -- =============================================

-- -- AUTO_INCREMENT is already used in Employee
-- -- Simulate a salary sequence using a helper table
-- CREATE TABLE SalarySeq (
--     next_val INT NOT NULL
-- );

-- INSERT INTO SalarySeq VALUES (50000);

-- -- Function to get next salary (simulated)
-- UPDATE SalarySeq SET next_val = next_val + 5000;
-- SELECT next_val FROM SalarySeq;

-- -- You can now use this in application logic or stored procedures.


-- Step 1: Create Tables
CREATE TABLE Employee (
    e_id INT PRIMARY KEY,
    name VARCHAR(100),
    dob DATE
);

CREATE TABLE Company (
    company_name VARCHAR(100) PRIMARY KEY,
    city VARCHAR(100)
);

CREATE TABLE Works (
    e_id INT,
    company_name VARCHAR(100),
    salary INT,
    PRIMARY KEY (e_id, company_name),
    FOREIGN KEY (e_id) REFERENCES Employee(e_id) ON DELETE CASCADE,
    FOREIGN KEY (company_name) REFERENCES Company(company_name) ON DELETE CASCADE
);

CREATE TABLE Manages (
    e_id INT PRIMARY KEY,
    dept_name VARCHAR(100),
    FOREIGN KEY (e_id) REFERENCES Employee(e_id) ON DELETE CASCADE
);

-- Step 2: Insert Sample Data
INSERT INTO Employee VALUES
(1, 'Alice', '1990-01-01'),
(2, 'Bob', '1988-02-02'),
(3, 'Charlie', '1992-03-03');

INSERT INTO Company VALUES
('ABC', 'Pune'),
('XYZ', 'Mumbai');

INSERT INTO Works VALUES
(1, 'ABC', 60000),
(2, 'ABC', 40000),
(3, 'XYZ', 55000);

INSERT INTO Manages VALUES
(1, 'HR'),
(2, 'Tech');

-- Step 3: Create a View
CREATE VIEW ABC_Employees_HighSalary AS
SELECT E.name, W.salary
FROM Employee E
JOIN Works W ON E.e_id = W.e_id
WHERE W.company_name = 'ABC' AND W.salary > 50000;

-- Step 4: Create Index
CREATE INDEX idx_city ON Company(city);

-- Step 5: Add a Sequence Table
CREATE TABLE SalarySeq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100),
    salary INT
);

-- Step 6: Log Current Data

-- Log: Employee Table
SELECT * FROM Employee;

-- Log: Company Table
SELECT * FROM Company;

-- Log: Works Table
SELECT * FROM Works;

-- Log: Manages Table
SELECT * FROM Manages;

-- Log: View Output
SELECT * FROM ABC_Employees_HighSalary;

-- Log: Index Info
SHOW INDEX FROM Company;

-- Step 7: Update a Salary
UPDATE Works SET salary = 65000 WHERE e_id = 1 AND company_name = 'ABC';

-- Log: View After Update
SELECT * FROM ABC_Employees_HighSalary;

-- Step 8: Delete a Manager
DELETE FROM Manages WHERE e_id = 2;

-- Log: Manages Table After Deletion
SELECT * FROM Manages;

-- Step 9: Insert into Sequence Table
INSERT INTO SalarySeq (employee_name, salary)
SELECT E.name, W.salary
FROM Employee E
JOIN Works W ON E.e_id = W.e_id;

-- Log: Sequence Table
SELECT * FROM SalarySeq;

-- Step 10: Drop Index
DROP INDEX idx_city ON Company;

-- Log: Index Drop Check
SHOW INDEX FROM Company;

-- Step 11: Drop View
DROP VIEW ABC_Employees_HighSalary;

-- Final Log of All Tables
SELECT * FROM Employee;
SELECT * FROM Company;
SELECT * FROM Works;
SELECT * FROM Manages;
SELECT * FROM SalarySeq;
