This example demonstrates how to delegate the task to a coding(cloud agent).

https://github.com/kostinams/github-copilot-use-cases/agents?author=kostinams

**Prompt in Cloud Agent:**
Generate a FastAPI app with the following considerations:

Create it at the root folder and name it api-app.py
GET / : Show a health check message.
GET /items: Retrieve a list of all items.
GET /items/{item_id}: Retrieve an item by its ID.
POST /items: Create a new item.
PUT /items/{item_id}: Update an existing item by its ID.
DELETE /items/{item_id}: Delete an existing item by its ID.
The application should use a simple in-memory data store (a list) to manage the items with 10 creative sample items.
The item should have an ID, a name, and a description.
Use Pydantic for data validation and serialization.
Include appropriate status codes and error handling.
Use the FastAPI framework for building the API.
Run the application using uvicorn on port 8080.
