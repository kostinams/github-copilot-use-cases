from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Schema used to create or update an item."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)


class Item(ItemCreate):
    """Schema returned by the API."""

    id: int = Field(..., ge=1)


app = FastAPI(title="Items API")

items: List[Item] = [
    Item(id=1, name="Nebula Compass", description="A brass compass that points toward your next big idea."),
    Item(id=2, name="Echo Quill", description="A fountain pen that records spoken notes as you write."),
    Item(id=3, name="Solar Bloom Lamp", description="A desk lamp that opens like a flower at sunrise."),
    Item(id=4, name="Pixel Bonsai", description="A tiny LED tree that changes color with the weather."),
    Item(id=5, name="Aurora Mug", description="A heat-reactive mug that reveals constellations."),
    Item(id=6, name="Drift Notebook", description="A reusable notebook with pages that erase using steam."),
    Item(id=7, name="Whisper Keyboard", description="A silent mechanical keyboard with tactile feedback."),
    Item(id=8, name="Orbit Timer", description="A magnetic timer ring designed for focus sessions."),
    Item(id=9, name="Skyline Coaster Set", description="Coasters that stack into a miniature city skyline."),
    Item(id=10, name="Tide Speaker", description="A portable speaker with ambient ocean sound presets."),
]


@app.get("/", status_code=status.HTTP_200_OK)
def health_check() -> dict:
    """Return a health check response."""

    return {"message": "FastAPI app is healthy."}


@app.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def get_items() -> List[Item]:
    """Retrieve all items from memory."""

    return items


@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_item(item_id: int) -> Item:
    """Retrieve a single item by its identifier."""

    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate) -> Item:
    """Create a new item and assign a new identifier."""

    next_id = max((existing_item.id for existing_item in items), default=0) + 1
    new_item = Item(id=next_id, name=item.name, description=item.description)
    items.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: ItemCreate) -> Item:
    """Update an existing item by its identifier."""

    for index, existing_item in enumerate(items):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, name=item.name, description=item.description)
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    """Delete an existing item by its identifier."""

    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return None
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
