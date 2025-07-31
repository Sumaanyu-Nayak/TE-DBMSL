-- =============================================
-- Use (or create) the target database
-- =============================================
-- CREATE DATABASE IF NOT EXISTS DBMS_ASSIGN1;
-- USE DBMS_ASSIGN1;

-- =============================================
-- 1. DROP TABLES IF THEY EXIST
--    (reverse order for FK dependencies)
-- =============================================
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Company;

-- =============================================
-- 2. CREATE TABLES
-- =============================================

-- Company table
CREATE TABLE Company (
    C_ID     INT           PRIMARY KEY,
    C_Name   VARCHAR(100)  NOT NULL,
    City     VARCHAR(100)  NOT NULL
);

-- Employee table (E_ID auto-increments; other fields nullable)
CREATE TABLE Employee (
    E_ID        INT             PRIMARY KEY AUTO_INCREMENT,
    E_Name      VARCHAR(100)    NULL,
    Street      VARCHAR(100)    NULL,
    City        VARCHAR(100)    NULL,
    Salary      DECIMAL(10,2)   NULL,
    Manager_ID  INT             NULL,
    C_ID        INT             NULL,
    FOREIGN KEY (Manager_ID) REFERENCES Employee(E_ID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (C_ID)        REFERENCES Company(C_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Department table
CREATE TABLE Department (
    D_ID        INT           PRIMARY KEY,
    D_Name      VARCHAR(100)  NOT NULL,
    Manager_ID  INT           NULL,
    C_ID        INT           NULL,
    FOREIGN KEY (Manager_ID) REFERENCES Employee(E_ID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (C_ID)        REFERENCES Company(C_ID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- =============================================
-- 3. 20 QUERIES
-- =============================================

-- 3.1 Insert values into above created tables
INSERT INTO Company VALUES 
  (1, 'Amazon',   'Pune'),
  (2, 'Google',   'Hyderabad'),
  (3, 'Flipkart', 'Bangalore'),
  (4, 'ABC Corp', 'Mumbai');

INSERT INTO Employee (E_ID, E_Name, Street, City, Salary, Manager_ID, C_ID) VALUES 
  (101, 'Alice',   'MG Road',      'Pune',      60000, NULL, 1),
  (102, 'Bob',     'Park St',      'Hyderabad', 75000, 101, 2),
  (103, 'Charlie', 'BTM Layout',   'Bangalore', 40000, 101, 3),
  (104, 'David',   'Andheri West', 'Mumbai',    35000, 102, 4),
  (105, 'Eva',     'Baner',        'Pune',      50000, 102, 1);

INSERT INTO Department VALUES 
  (1, 'Sales',      101, 1),
  (2, 'R&D',        102, 2),
  (3, 'HR',         103, 3);

-- 3.2 Insert values into only selected columns (Street, City)
INSERT INTO Employee (Street, City) VALUES ('JM Road', 'Pune');

-- 3.3 Select all values from Employee and Company tables
SELECT * FROM Employee;
SELECT * FROM Company;

-- 3.4 Select employee ID and name from Employee
SELECT E_ID, E_Name FROM Employee;

-- 3.5 Select names of all employees who are managers
SELECT DISTINCT E.E_Name
FROM Employee E
JOIN Department D ON E.E_ID = D.Manager_ID;

-- 3.6 Select list of all distinct cities from Company
SELECT DISTINCT City FROM Company;

-- 3.7 Update address (Street, City) of employee whose E_ID = 12345
UPDATE Employee
SET Street = 'New Street',
    City   = 'New City'
WHERE E_ID = 12345;

-- 3.8 Increase salary of employees working in “Amazon” by 10000
UPDATE Employee
SET Salary = Salary + 10000
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Amazon');

-- 3.9 Delete records of all employees having salary between 20000 and 50000
DELETE FROM Employee
WHERE Salary BETWEEN 20000 AND 50000;

-- 3.10 Select all company names where city starts with ‘P’
SELECT C_Name
FROM Company
WHERE City LIKE 'P%';

-- 3.11 List all employees from (“Amazon”, “Flipkart”, “Google”)
SELECT *
FROM Employee
WHERE C_ID IN (
    SELECT C_ID FROM Company
    WHERE C_Name IN ('Amazon','Flipkart','Google')
);

-- 3.12 What is the average salary of employees working in “ABC Corp”
SELECT AVG(Salary) AS Avg_Salary
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'ABC Corp');

-- 3.13 Find total number of employees working in “Amazon”
SELECT COUNT(*) AS Total_Employees
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Amazon');

-- 3.14 Find MAX and MIN salary of employees in “Google”
SELECT MAX(Salary) AS Max_Salary,
       MIN(Salary) AS Min_Salary
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Google');

-- 3.15 Find total amount spent on salaries of employees of “ABC Corp”
SELECT SUM(Salary) AS Total_Salary
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'ABC Corp');

-- 3.16 List all details of Company, sorted ascending by C_Name and descending by City
SELECT * FROM Company
ORDER BY C_Name ASC, City DESC;

-- 3.17 List all employee names from “Amazon” and “Google” using UNION
SELECT E_Name
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Amazon')
UNION
SELECT E_Name
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Google');

-- 3.18 List all employee names (allow duplicates) using UNION ALL
SELECT E_Name
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Amazon')
UNION ALL
SELECT E_Name
FROM Employee
WHERE C_ID = (SELECT C_ID FROM Company WHERE C_Name = 'Google');

-- 3.19 List all employee details who are managers (emulate INTERSECT)
SELECT * FROM Employee
WHERE E_ID IN (SELECT Manager_ID FROM Department);

-- 3.20 List all employee details who are not managers (emulate MINUS)
SELECT * FROM Employee
WHERE E_ID NOT IN (SELECT Manager_ID FROM Department);
