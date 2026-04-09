"""
FastAPI application with in-memory CRUD operations for items.

Provides endpoints for health check and item management.
Run with: python api-app.py
"""

import threading
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Items API", description="A simple CRUD API for managing items.")

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ItemBase(BaseModel):
    """Shared fields for item creation and update."""

    name: str = Field(..., min_length=1, description="Name of the item")
    description: Optional[str] = Field(None, description="Optional description of the item")


class ItemCreate(ItemBase):
    """Schema used when creating a new item."""


class ItemUpdate(ItemBase):
    """Schema used when updating an existing item."""


class Item(ItemBase):
    """Full item representation returned from the API."""

    id: int = Field(..., description="Unique identifier of the item")

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

_items: List[Item] = [
    Item(id=1, name="Enchanted Compass", description="A compass that always points toward adventure."),
    Item(id=2, name="Thunderbolt Umbrella", description="An umbrella that doubles as a lightning rod."),
    Item(id=3, name="Whispering Tome", description="A book that reads itself aloud in a soothing voice."),
    Item(id=4, name="Gravity-Defying Boots", description="Boots that let you walk on ceilings."),
    Item(id=5, name="Chronos Watch", description="A watch that can pause time for exactly 5 seconds."),
    Item(id=6, name="Moonlight Lantern", description="A lantern powered by moonlight instead of sunlight."),
    Item(id=7, name="Infinite Canteen", description="A canteen that never runs out of sparkling water."),
    Item(id=8, name="Echo Mirror", description="A mirror that shows your reflection from yesterday."),
    Item(id=9, name="Pocket Greenhouse", description="A tiny greenhouse that fits in your pocket."),
    Item(id=10, name="Luck Crystal", description="A crystal said to attract small fortunes and lost socks."),
]

_next_id: int = len(_items) + 1
_lock = threading.Lock()


def _find_item(item_id: int) -> Item:
    """Return the item with *item_id*, or raise HTTP 404.

    Must be called while holding *_lock*.
    """
    for item in _items:
        if item.id == item_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found.",
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/", summary="Health check")
def health_check() -> dict:
    """Return a simple health-check message."""
    return {"status": "ok", "message": "Items API is running."}


@app.get("/items", response_model=List[Item], summary="List all items")
def get_items() -> List[Item]:
    """Retrieve a list of all items."""
    with _lock:
        return list(_items)


@app.get("/items/{item_id}", response_model=Item, summary="Get an item by ID")
def get_item(item_id: int) -> Item:
    """Retrieve a single item by its ID."""
    with _lock:
        return _find_item(item_id)


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
def create_item(payload: ItemCreate) -> Item:
    """Create a new item and add it to the store."""
    global _next_id
    with _lock:
        new_item = Item(id=_next_id, **payload.model_dump())
        _items.append(new_item)
        _next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item, summary="Update an existing item")
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    """Replace the fields of an existing item identified by *item_id*."""
    with _lock:
        existing = _find_item(item_id)
        idx = _items.index(existing)
        updated = Item(id=item_id, **payload.model_dump())
        _items[idx] = updated
    return updated


@app.delete(
    "/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
def delete_item(item_id: int) -> None:
    """Delete an item identified by *item_id*."""
    with _lock:
        item = _find_item(item_id)
        _items.remove(item)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
