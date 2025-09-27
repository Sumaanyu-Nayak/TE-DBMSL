from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL connection
connection = None
current_database = None
current_table = None

def connect_to_mysql(host, port, username, password, database):
    """Connect to MySQL with the provided credentials"""
    global connection, current_database
    
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            current_database = database
            return True, f"Connected successfully to MySQL database: {database}"
    except Error as e:
        return False, f"MySQL connection error: {str(e)}"

def get_cursor():
    """Get a cursor for executing queries"""
    if connection and connection.is_connected():
        return connection.cursor(dictionary=True)
    return None

@app.route('/api/connect', methods=['POST'])
def connect_database():
    """Establish connection to MySQL"""
    data = request.json
    host = data.get('host', 'localhost')
    port = int(data.get('port', 3306))
    username = data.get('username', 'root')
    password = data.get('password', '')
    database = data.get('database', 'testdb')
    
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'}), 400
    
    success, message = connect_to_mysql(host, port, username, password, database)
    
    if success:
        return jsonify({
            'success': True, 
            'message': message,
            'host': host,
            'port': port,
            'database': database
        })
    else:
        return jsonify({'success': False, 'message': message}), 500

@app.route('/api/create-table', methods=['POST'])
def create_table():
    """Create a new table"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        table_name = data.get('table_name')
        columns = data.get('columns', [])
        
        if not table_name or not columns:
            return jsonify({'success': False, 'message': 'Table name and columns are required'}), 400
        
        cursor = get_cursor()
        
        # Build CREATE TABLE query
        column_definitions = []
        for col in columns:
            col_def = f"`{col['name']}` {col['type']}"
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if col.get('auto_increment'):
                col_def += " AUTO_INCREMENT"
            if col.get('not_null'):
                col_def += " NOT NULL"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            column_definitions.append(col_def)
        
        query = f"CREATE TABLE `{table_name}` ({', '.join(column_definitions)})"
        cursor.execute(query)
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': f'Table {table_name} created successfully',
            'query': query
        })
    
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/insert', methods=['POST'])
def insert_record():
    """Insert a new record"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        table_name = data.get('table')
        record_data = data.get('data', {})
        
        if not table_name or not record_data:
            return jsonify({'success': False, 'message': 'Table name and data are required'}), 400
        
        cursor = get_cursor()
        
        # Build INSERT query
        columns = list(record_data.keys())
        values = list(record_data.values())
        
        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join([f'`{col}`' for col in columns])
        
        query = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
        cursor.execute(query, values)
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Record inserted successfully',
            'inserted_id': cursor.lastrowid,
            'affected_rows': cursor.rowcount
        })
    
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/select', methods=['POST'])
def select_records():
    """Select records with optional WHERE clause"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        table_name = data.get('table')
        columns = data.get('columns', ['*'])
        where_clause = data.get('where', '')
        limit = data.get('limit', 100)
        
        if not table_name:
            return jsonify({'success': False, 'message': 'Table name is required'}), 400
        
        cursor = get_cursor()
        
        # Build SELECT query
        columns_str = ', '.join([f'`{col}`' if col != '*' else col for col in columns])
        query = f"SELECT {columns_str} FROM `{table_name}`"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        query += f" LIMIT {limit}"
        
        cursor.execute(query)
        records = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'records': records,
            'count': len(records),
            'query': query
        })
    
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/update', methods=['POST'])
def update_records():
    """Update records"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        table_name = data.get('table')
        set_clause = data.get('set', {})
        where_clause = data.get('where', '')
        
        if not table_name or not set_clause:
            return jsonify({'success': False, 'message': 'Table name and SET clause are required'}), 400
        
        cursor = get_cursor()
        
        # Build UPDATE query
        set_parts = []
        values = []
        for column, value in set_clause.items():
            set_parts.append(f"`{column}` = %s")
            values.append(value)
        
        query = f"UPDATE `{table_name}` SET {', '.join(set_parts)}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        cursor.execute(query, values)
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Records updated successfully',
            'affected_rows': cursor.rowcount,
            'query': query
        })
    
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/delete', methods=['POST'])
def delete_records():
    """Delete records"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        table_name = data.get('table')
        where_clause = data.get('where', '')
        
        if not table_name:
            return jsonify({'success': False, 'message': 'Table name is required'}), 400
        
        if not where_clause:
            return jsonify({'success': False, 'message': 'WHERE clause is required for safety'}), 400
        
        cursor = get_cursor()
        
        # Build DELETE query
        query = f"DELETE FROM `{table_name}` WHERE {where_clause}"
        cursor.execute(query)
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Records deleted successfully',
            'affected_rows': cursor.rowcount,
            'query': query
        })
    
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/execute-query', methods=['POST'])
def execute_query():
    """Execute raw SQL query"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'message': 'Query is required'}), 400
        
        cursor = get_cursor()
        cursor.execute(query)
        
        # Check if it's a SELECT query
        if query.upper().strip().startswith('SELECT'):
            records = cursor.fetchall()
            return jsonify({
                'success': True,
                'records': records,
                'count': len(records),
                'query': query
            })
        else:
            connection.commit()
            return jsonify({
                'success': True,
                'message': 'Query executed successfully',
                'affected_rows': cursor.rowcount,
                'query': query
            })
    
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get connection status"""
    if connection and connection.is_connected():
        cursor = get_cursor()
        
        try:
            # Get database info with separate queries to avoid syntax issues
            cursor.execute("SELECT DATABASE() as current_db")
            current_db_result = cursor.fetchone()
            current_db = current_db_result['current_db'] if current_db_result and current_db_result['current_db'] else 'None'
            
            # Use USER() instead of CURRENT_USER() for MariaDB compatibility
            cursor.execute("SELECT USER() as current_user")
            current_user_result = cursor.fetchone()
            current_user = current_user_result['current_user'] if current_user_result else 'Unknown'
            
            cursor.execute("SELECT VERSION() as version")
            version_result = cursor.fetchone()
            version = version_result['version'] if version_result else 'Unknown'
            
        except Exception as e:
            # If there's still an issue, use a simpler approach
            current_db = current_database if current_database else 'None'
            current_user = 'Connected User'
            version = 'MariaDB/MySQL'
            
        cursor.close()
        
        return jsonify({
            'connected': True,
            'database': current_database,
            'current_db': current_db,
            'current_user': current_user,
            'mysql_version': version
        })
    else:
        return jsonify({'connected': False})

@app.route('/api/tables', methods=['GET'])
def list_tables():
    """List all tables in the current database"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        cursor = get_cursor()
        cursor.execute("SHOW TABLES")
        tables = [list(table.values())[0] for table in cursor.fetchall()]
        
        return jsonify({
            'success': True,
            'tables': tables
        })
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/table-info', methods=['POST'])
def get_table_info():
    """Get table structure information"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        table_name = data.get('table')
        
        if not table_name:
            return jsonify({'success': False, 'message': 'Table name is required'}), 400
        
        cursor = get_cursor()
        cursor.execute(f"DESCRIBE `{table_name}`")
        columns = cursor.fetchall()
        
        cursor.execute(f"SELECT COUNT(*) as row_count FROM `{table_name}`")
        row_count = cursor.fetchone()['row_count']
        
        return jsonify({
            'success': True,
            'table': table_name,
            'columns': columns,
            'row_count': row_count
        })
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@app.route('/api/databases', methods=['GET'])
def list_databases():
    """List all databases"""
    if not connection or not connection.is_connected():
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        cursor = get_cursor()
        cursor.execute("SHOW DATABASES")
        databases = [list(db.values())[0] for db in cursor.fetchall()]
        
        return jsonify({
            'success': True,
            'databases': databases
        })
    except Error as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    print("Starting MySQL CRUD API Server...")
    print("Make sure to install required packages:")
    print("pip install flask flask-cors mysql-connector-python")
    print("\nServer will run on http://localhost:5001")
    print("Make sure MySQL server is running on localhost:3306")
    app.run(debug=True, host='0.0.0.0', port=5001)