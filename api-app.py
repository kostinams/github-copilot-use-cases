"""
FastAPI Application for Item Management

This application provides a REST API for managing items with CRUD operations.
It uses an in-memory data store and includes proper error handling.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional


# Pydantic model for Item with validation
class Item(BaseModel):
    """
    Item model for data validation and serialization.
    
    Attributes:
        id (int): Unique identifier for the item.
        name (str): Name of the item.
        description (str): Description of the item.
    """
    id: int = Field(..., description="Unique identifier for the item")
    name: str = Field(..., min_length=1, description="Name of the item")
    description: str = Field(
        ..., 
        min_length=1, 
        description="Description of the item"
    )


class ItemCreate(BaseModel):
    """
    Model for creating a new item (without ID).
    
    Attributes:
        name (str): Name of the item.
        description (str): Description of the item.
    """
    name: str = Field(..., min_length=1, description="Name of the item")
    description: str = Field(
        ..., 
        min_length=1, 
        description="Description of the item"
    )


class ItemUpdate(BaseModel):
    """
    Model for updating an existing item.
    
    Attributes:
        name (Optional[str]): Updated name of the item.
        description (Optional[str]): Updated description of the item.
    """
    name: Optional[str] = Field(
        None, 
        min_length=1, 
        description="Updated name of the item"
    )
    description: Optional[str] = Field(
        None, 
        min_length=1, 
        description="Updated description of the item"
    )


# Initialize FastAPI application
app = FastAPI(
    title="Item Management API",
    description="A simple API for managing items with CRUD operations",
    version="1.0.0"
)


# In-memory data store with 10 creative sample items
items_db: List[Item] = [
    Item(
        id=1, 
        name="Quantum Keyboard", 
        description="A keyboard that types in multiple dimensions"
    ),
    Item(
        id=2, 
        name="Holographic Mouse", 
        description="Navigate through virtual space with holographic precision"
    ),
    Item(
        id=3, 
        name="Self-Brewing Coffee Mug", 
        description="Never wait for coffee again with this auto-brewing mug"
    ),
    Item(
        id=4, 
        name="Telepathic Headphones", 
        description="Listen to music by thinking about your favorite songs"
    ),
    Item(
        id=5, 
        name="Infinite Battery Charger", 
        description="Charges any device instantly with unlimited power"
    ),
    Item(
        id=6, 
        name="Time-Bending Watch", 
        description="A watch that lets you pause, rewind, or fast-forward time"
    ),
    Item(
        id=7, 
        name="Gravity-Defying Sneakers", 
        description="Walk on walls and ceilings with anti-gravity technology"
    ),
    Item(
        id=8, 
        name="Invisible Umbrella", 
        description="Stay dry without carrying anything visible"
    ),
    Item(
        id=9, 
        name="Dream Recording Pillow", 
        description="Record and replay your dreams in high definition"
    ),
    Item(
        id=10, 
        name="Universal Translator Earpiece", 
        description="Understand and speak any language instantly"
    )
]


# Helper function to get the next available ID
def get_next_id() -> int:
    """
    Generate the next available ID for a new item.
    
    Returns:
        int: The next available ID.
    """
    if not items_db:
        return 1
    return max(item.id for item in items_db) + 1


# Helper function to find an item by ID
def find_item_by_id(item_id: int) -> Optional[Item]:
    """
    Find an item in the database by its ID.
    
    Parameters:
        item_id (int): The ID of the item to find.
    
    Returns:
        Optional[Item]: The found item or None if not found.
    """
    for item in items_db:
        if item.id == item_id:
            return item
    return None


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check() -> dict:
    """
    Health check endpoint to verify API is running.
    
    Returns:
        dict: Status message indicating the API is healthy.
    """
    return {
        "status": "healthy",
        "message": "Item Management API is running successfully"
    }


@app.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
async def get_items() -> List[Item]:
    """
    Retrieve all items from the database.
    
    Returns:
        List[Item]: List of all items in the database.
    """
    return items_db


@app.get(
    "/items/{item_id}", 
    response_model=Item, 
    status_code=status.HTTP_200_OK
)
async def get_item(item_id: int) -> Item:
    """
    Retrieve a specific item by its ID.
    
    Parameters:
        item_id (int): The ID of the item to retrieve.
    
    Returns:
        Item: The requested item.
    
    Raises:
        HTTPException: 404 if the item is not found.
    """
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_data: ItemCreate) -> Item:
    """
    Create a new item in the database.
    
    Parameters:
        item_data (ItemCreate): The data for the new item.
    
    Returns:
        Item: The newly created item with its assigned ID.
    """
    new_item = Item(
        id=get_next_id(),
        name=item_data.name,
        description=item_data.description
    )
    items_db.append(new_item)
    return new_item


@app.put(
    "/items/{item_id}", 
    response_model=Item, 
    status_code=status.HTTP_200_OK
)
async def update_item(item_id: int, item_data: ItemUpdate) -> Item:
    """
    Update an existing item by its ID.
    
    Parameters:
        item_id (int): The ID of the item to update.
        item_data (ItemUpdate): The updated data for the item.
    
    Returns:
        Item: The updated item.
    
    Raises:
        HTTPException: 404 if the item is not found.
        HTTPException: 400 if no update data is provided.
    """
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Check if at least one field is provided for update
    if item_data.name is None and item_data.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (name or description) must be provided"
        )
    
    # Update only the provided fields
    if item_data.name is not None:
        item.name = item_data.name
    if item_data.description is not None:
        item.description = item_data.description
    
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int) -> None:
    """
    Delete an item by its ID.
    
    Parameters:
        item_id (int): The ID of the item to delete.
    
    Raises:
        HTTPException: 404 if the item is not found.
    """
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    items_db.remove(item)


# Run the application with: uvicorn api-app:app --host 0.0.0.0 --port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
