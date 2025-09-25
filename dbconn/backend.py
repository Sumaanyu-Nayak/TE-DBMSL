from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
DB_PASSWORD = ""  # Will be set via frontend
MONGO_URI = ""
client = None
db = None
collection = None

def connect_to_mongodb(password, database_name, collection_name):
    """Connect to MongoDB with the provided credentials"""
    global client, db, collection, MONGO_URI
    
    try:
        MONGO_URI = f"mongodb+srv://nayaksumaanyu:{password}@cluster03.fy1gemz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster03"
        client = MongoClient(MONGO_URI)
        
        # Test the connection
        client.admin.command('ping')
        
        db = client[database_name]
        collection = db[collection_name]
        
        return True, "Connected successfully"
    except Exception as e:
        return False, str(e)

@app.route('/api/connect', methods=['POST'])
def connect_database():
    """Establish connection to MongoDB"""
    data = request.json
    password = data.get('password')
    database_name = data.get('database', 'dbmsl')
    collection_name = data.get('collection', 'users')
    
    if not password:
        return jsonify({'success': False, 'message': 'Password is required'}), 400
    
    success, message = connect_to_mongodb(password, database_name, collection_name)
    
    if success:
        return jsonify({
            'success': True, 
            'message': message,
            'database': database_name,
            'collection': collection_name
        })
    else:
        return jsonify({'success': False, 'message': message}), 500

@app.route('/api/create', methods=['POST'])
def create_document():
    """Create a new document"""
    if collection is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        document = data.get('document')
        
        if not document:
            return jsonify({'success': False, 'message': 'Document data is required'}), 400
        
        result = collection.insert_one(document)
        
        return jsonify({
            'success': True,
            'message': 'Document created successfully',
            'inserted_id': str(result.inserted_id),
            'acknowledged': result.acknowledged
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/read', methods=['POST'])
def read_documents():
    """Read documents with optional filter"""
    if collection is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        filter_query = data.get('filter', {})
        limit = data.get('limit', 10)
        
        # Convert ObjectId strings in filter
        if '_id' in filter_query and isinstance(filter_query['_id'], str):
            try:
                filter_query['_id'] = ObjectId(filter_query['_id'])
            except:
                pass
        
        cursor = collection.find(filter_query).limit(limit)
        documents = []
        
        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            documents.append(doc)
        
        return jsonify({
            'success': True,
            'documents': documents,
            'count': len(documents),
            'filter': filter_query,
            'limit': limit
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/update', methods=['POST'])
def update_documents():
    """Update documents"""
    if collection is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        filter_query = data.get('filter', {})
        update_data = data.get('update', {})
        update_multiple = data.get('multiple', False)
        
        if not filter_query or not update_data:
            return jsonify({'success': False, 'message': 'Filter and update data are required'}), 400
        
        # Convert ObjectId strings in filter
        if '_id' in filter_query and isinstance(filter_query['_id'], str):
            try:
                filter_query['_id'] = ObjectId(filter_query['_id'])
            except:
                pass
        
        if update_multiple:
            result = collection.update_many(filter_query, update_data)
        else:
            result = collection.update_one(filter_query, update_data)
        
        return jsonify({
            'success': True,
            'message': 'Update completed',
            'matched_count': result.matched_count,
            'modified_count': result.modified_count,
            'acknowledged': result.acknowledged
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/delete', methods=['POST'])
def delete_documents():
    """Delete documents"""
    if collection is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        filter_query = data.get('filter', {})
        delete_multiple = data.get('multiple', False)
        
        if not filter_query:
            return jsonify({'success': False, 'message': 'Filter is required'}), 400
        
        # Convert ObjectId strings in filter
        if '_id' in filter_query and isinstance(filter_query['_id'], str):
            try:
                filter_query['_id'] = ObjectId(filter_query['_id'])
            except:
                pass
        
        if delete_multiple:
            result = collection.delete_many(filter_query)
        else:
            result = collection.delete_one(filter_query)
        
        return jsonify({
            'success': True,
            'message': 'Delete completed',
            'deleted_count': result.deleted_count,
            'acknowledged': result.acknowledged
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/aggregate', methods=['POST'])
def aggregate_documents():
    """Perform aggregation"""
    if collection is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        data = request.json
        pipeline = data.get('pipeline', [])
        
        if not pipeline:
            return jsonify({'success': False, 'message': 'Pipeline is required'}), 400
        
        cursor = collection.aggregate(pipeline)
        results = []
        
        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            if '_id' in doc and isinstance(doc['_id'], ObjectId):
                doc['_id'] = str(doc['_id'])
            results.append(doc)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'pipeline': pipeline
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get connection status"""
    if collection is not None:
        return jsonify({
            'connected': True,
            'database': db.name if db is not None else None,
            'collection': collection.name if collection is not None else None
        })
    else:
        return jsonify({'connected': False})

@app.route('/api/collections', methods=['GET'])
def list_collections():
    """List all collections in the current database"""
    if db is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        collections = db.list_collection_names()
        return jsonify({
            'success': True,
            'collections': collections
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get collection statistics"""
    if collection is None:
        return jsonify({'success': False, 'message': 'Not connected to database'}), 400
    
    try:
        stats = db.command('collStats', collection.name)
        
        return jsonify({
            'success': True,
            'stats': {
                'count': stats.get('count', 0),
                'size': stats.get('size', 0),
                'avgObjSize': stats.get('avgObjSize', 0),
                'storageSize': stats.get('storageSize', 0),
                'indexes': stats.get('nindexes', 0)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("Starting MongoDB CRUD API Server...")
    print("Make sure to install required packages:")
    print("pip install flask flask-cors pymongo")
    print("\nServer will run on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)