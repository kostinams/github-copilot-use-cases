"""
FastAPI Application for managing items with CRUD operations.

This application provides a REST API for managing items with in-memory storage.
Run with: uvicorn api-app:app --host 0.0.0.0 --port 8080
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# Pydantic models for data validation and serialization
class Item(BaseModel):
    """
    Item model with validation.
    
    Attributes:
        id: Unique identifier for the item
        name: Name of the item
        description: Description of the item
    """
    id: int = Field(..., description="Unique identifier for the item", ge=1)
    name: str = Field(..., description="Name of the item", min_length=1)
    description: str = Field(..., description="Description of the item", min_length=1)


class ItemCreate(BaseModel):
    """
    Model for creating a new item (without ID).
    
    Attributes:
        name: Name of the item
        description: Description of the item
    """
    name: str = Field(..., description="Name of the item", min_length=1)
    description: str = Field(..., description="Description of the item", min_length=1)


class ItemUpdate(BaseModel):
    """
    Model for updating an existing item.
    
    Attributes:
        name: Optional new name for the item
        description: Optional new description for the item
    """
    name: Optional[str] = Field(None, description="Name of the item", min_length=1)
    description: Optional[str] = Field(None, description="Description of the item", min_length=1)


# Initialize FastAPI application
app = FastAPI(
    title="Items API",
    description="A simple API for managing items with CRUD operations",
    version="1.0.0"
)

# In-memory data store with 10 creative sample items
items_db: List[Item] = [
    Item(id=1, name="Cosmic Coffee Mug", description="A mug that keeps your coffee at the perfect temperature using quantum physics"),
    Item(id=2, name="Telepathic Keyboard", description="Type with your thoughts! No more RSI from excessive typing"),
    Item(id=3, name="Self-Folding Laundry Basket", description="Your laundry folds itself while you binge-watch your favorite shows"),
    Item(id=4, name="Time-Traveling Alarm Clock", description="Wake up 5 minutes before you actually need to, every single time"),
    Item(id=5, name="Invisible Umbrella", description="Protects you from rain using an advanced force field technology"),
    Item(id=6, name="Singing Toaster", description="Serenades you with your favorite songs while toasting your bread to perfection"),
    Item(id=7, name="Levitating Plant Pot", description="Your plants float in mid-air, making watering an adventure"),
    Item(id=8, name="Memory Foam Pillow 2.0", description="Remembers your dreams and plays them back on demand"),
    Item(id=9, name="Programmable Pizza Cutter", description="Cuts your pizza according to precise geometric patterns using AI"),
    Item(id=10, name="Holographic Pet Rock", description="All the companionship of a pet rock, now with 3D holographic projections")
]

# Helper function to get next available ID
def get_next_id() -> int:
    """
    Get the next available ID for a new item.
    
    Returns:
        The next available ID
    """
    if not items_db:
        return 1
    return max(item.id for item in items_db) + 1


# Helper function to find item by ID
def find_item_by_id(item_id: int) -> Optional[Item]:
    """
    Find an item in the database by its ID.
    
    Parameters:
        item_id: The ID of the item to find
        
    Returns:
        The item if found, None otherwise
    """
    for item in items_db:
        if item.id == item_id:
            return item
    return None


@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        A message indicating the API is running
    """
    return {
        "status": "healthy",
        "message": "Items API is up and running!",
        "version": "1.0.0"
    }


@app.get("/items", response_model=List[Item], tags=["Items"])
def get_items():
    """
    Retrieve all items from the database.
    
    Returns:
        A list of all items
    """
    return items_db


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: int):
    """
    Retrieve a specific item by its ID.
    
    Parameters:
        item_id: The ID of the item to retrieve
        
    Returns:
        The requested item
        
    Raises:
        HTTPException: 404 if the item is not found
    """
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item: ItemCreate):
    """
    Create a new item.
    
    Parameters:
        item: The item data to create
        
    Returns:
        The created item with its assigned ID
    """
    new_id = get_next_id()
    new_item = Item(
        id=new_id,
        name=item.name,
        description=item.description
    )
    items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: int, item_update: ItemUpdate):
    """
    Update an existing item by its ID.
    
    Parameters:
        item_id: The ID of the item to update
        item_update: The fields to update
        
    Returns:
        The updated item
        
    Raises:
        HTTPException: 404 if the item is not found
        HTTPException: 400 if no fields are provided for update
    """
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    # Check if at least one field is provided for update
    if item_update.name is None and item_update.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (name or description) must be provided for update"
        )
    
    # Update only the fields that are provided
    if item_update.name is not None:
        item.name = item_update.name
    if item_update.description is not None:
        item.description = item_update.description
    
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def delete_item(item_id: int):
    """
    Delete an item by its ID.
    
    Parameters:
        item_id: The ID of the item to delete
        
    Raises:
        HTTPException: 404 if the item is not found
    """
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    
    items_db.remove(item)
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
