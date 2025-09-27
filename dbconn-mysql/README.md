# MySQL CRUD Operations

A complete MySQL CRUD (Create, Read, Update, Delete) application with Python Flask backend and HTML frontend.

## Features

- **Create Table**: Design tables with columns, data types, primary keys, and auto-increment
- **Insert**: Add new records to tables
- **Select**: Query records with filters, WHERE clauses, and limits
- **Update**: Modify existing records with SET and WHERE clauses
- **Delete**: Remove records safely with mandatory WHERE clauses
- **Raw SQL**: Execute any SQL query directly
- **Database Info**: List databases, tables, and view table structures

## Architecture

- **Backend**: Python Flask server with MySQL integration
- **Frontend**: Pure HTML with JavaScript (no frameworks)
- **Database**: MySQL Server (localhost)

## Setup Instructions

### 1. Install MySQL Server

Make sure MySQL is installed and running on your system:

**Windows:**
```bash
# Install MySQL and start service
net start mysql
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Linux:**
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

### 2. Install Python Dependencies

```bash
cd dbconn-mysql
pip install -r requirements.txt
```

Or install individually:
```bash
pip install flask flask-cors mysql-connector-python
```

### 3. Setup MySQL Database

Connect to MySQL and create a test database:

```sql
mysql -u root -p

CREATE DATABASE testdb;
USE testdb;

-- Optional: Create a test table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Start the Backend Server

```bash
python backend.py
```

The server will start on `http://localhost:5001`

### 5. Open the Frontend

Open `dbconn.html` in your web browser.

## Usage

1. **Start MySQL Server**: Ensure MySQL is running
2. **Start Backend**: Run `python backend.py`
3. **Check Server Status**: Click "Check Server Status" in the web interface
4. **Connect to Database**: Enter your MySQL credentials (default: root/localhost/3306)
5. **Perform Operations**: Use the various forms to create tables, insert, select, update, delete records

## API Endpoints

- `GET /api/status` - Check connection status
- `POST /api/connect` - Connect to MySQL database
- `POST /api/create-table` - Create new table
- `POST /api/insert` - Insert record
- `POST /api/select` - Select records
- `POST /api/update` - Update records
- `POST /api/delete` - Delete records
- `POST /api/execute-query` - Execute raw SQL query
- `GET /api/databases` - List all databases
- `GET /api/tables` - List tables in current database
- `POST /api/table-info` - Get table structure information

## Example Operations

### Create Table
```json
{
  "table_name": "users",
  "columns": [
    {
      "name": "id",
      "type": "INT",
      "primary_key": true,
      "auto_increment": true,
      "not_null": true
    },
    {
      "name": "name",
      "type": "VARCHAR(255)",
      "not_null": true
    },
    {
      "name": "email",
      "type": "VARCHAR(255)"
    }
  ]
}
```

### Insert Record
```json
{
  "table": "users",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
```

### Select with WHERE
```json
{
  "table": "users",
  "columns": ["*"],
  "where": "age > 18 AND name LIKE 'J%'",
  "limit": 50
}
```

### Update Records
```json
{
  "table": "users",
  "set": {
    "age": 31,
    "email": "john.doe@example.com"
  },
  "where": "id = 1"
}
```

### Raw SQL Query
```sql
SELECT u.name, u.email, COUNT(o.id) as order_count 
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id 
WHERE u.created_at > '2023-01-01' 
GROUP BY u.id 
ORDER BY order_count DESC;
```

## Security Features

- **Safe DELETE**: Mandatory WHERE clause for delete operations
- **SQL Injection Protection**: Parameterized queries
- **Connection Management**: Proper cursor and connection handling
- **Error Handling**: Comprehensive error reporting

## Default Connection Settings

- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: (empty - enter your MySQL root password)
- **Database**: testdb

## Troubleshooting

1. **Server Offline**: Make sure `python backend.py` is running
2. **MySQL Connection Failed**: 
   - Check if MySQL server is running
   - Verify credentials (username/password)
   - Ensure database exists
3. **Access Denied**: Check MySQL user permissions
4. **Table Not Found**: Make sure you're connected to the correct database

## Advanced Features

- **Table Designer**: Visual table creation with column specifications
- **Query History**: All executed queries are shown in results
- **Multi-column Operations**: Support for complex WHERE clauses
- **Database Schema**: View table structures and row counts
- **Raw SQL Support**: Execute any MySQL query directly

This MySQL CRUD application provides a complete interface for database operations while maintaining security and ease of use!