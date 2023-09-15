# Building a Simple CRUD API with FastAPI and SQLite

This API performs all four CRUD functions and uses a SQLite database to store and access data. The Person model has fields for name, email, id, and creation time. Here’s a diagram of the database model:

![Database CRUD Interactions](diagram.png "Database CRUD Interactions")

# Usage
1. Install the requiremnts
```
pip install -r requirements.txt
```

2. Run the server
```
uvicorn main:app --reload
```

  