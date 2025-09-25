# MongoDB CRUD Operations

A complete MongoDB CRUD (Create, Read, Update, Delete) application with Python Flask backend and HTML frontend.

## Features

- **Create**: Insert new documents into MongoDB
- **Read**: Query documents with filters and limits
- **Update**: Modify existing documents (single or multiple)
- **Delete**: Remove documents (single or multiple)
- **Aggregate**: Run complex aggregation pipelines
- **Database Info**: List collections and view statistics

## Architecture

- **Backend**: Python Flask server with MongoDB integration
- **Frontend**: Pure HTML with JavaScript (no frameworks)
- **Database**: MongoDB Atlas with connection string

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install flask flask-cors pymongo
```

### 2. MongoDB Atlas Setup

Your MongoDB connection string:
```
mongodb+srv://nayaksumaanyu:<db_password>@cluster03.fy1gemz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster03
```

### 3. Start the Backend Server

```bash
python backend.py
```

The server will start on `http://localhost:5000`

### 4. Open the Frontend

Open `dbconn.html` in your web browser.

## Usage

1. **Start Backend**: Run `python backend.py`
2. **Check Server Status**: Click "Check Server Status" in the web interface
3. **Connect to Database**: Enter your MongoDB password and database/collection names
4. **Perform CRUD Operations**: Use the forms to create, read, update, delete, or aggregate documents

## API Endpoints

- `GET /api/status` - Check connection status
- `POST /api/connect` - Connect to MongoDB
- `POST /api/create` - Create document
- `POST /api/read` - Read documents
- `POST /api/update` - Update documents
- `POST /api/delete` - Delete documents
- `POST /api/aggregate` - Run aggregation
- `GET /api/collections` - List collections
- `GET /api/stats` - Get collection statistics

## Example Operations

### Create Document
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "city": "New York"
}
```

### Read with Filter
```json
{
  "age": {"$gte": 18}
}
```

### Update Document
Filter:
```json
{"name": "John Doe"}
```

Update:
```json
{"$set": {"age": 31, "city": "Boston"}}
```

### Aggregation Pipeline
```json
[
  {"$group": {"_id": "$city", "count": {"$sum": 1}, "avgAge": {"$avg": "$age"}}},
  {"$sort": {"count": -1}}
]
```

## Security Notes

- This is for educational/experimental purposes
- Database password is transmitted from frontend to backend
- For production, implement proper authentication and environment variables

## Troubleshooting

1. **Server Offline**: Make sure `python backend.py` is running
2. **Connection Failed**: Check MongoDB Atlas password and network access
3. **CORS Issues**: Flask-CORS is enabled for all origins
4. **Invalid JSON**: Validate JSON syntax in the web interface