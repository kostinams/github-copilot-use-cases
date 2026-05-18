"""FastAPI CRUD app with an in-memory list data store."""

from threading import Lock

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
import uvicorn


class ItemBase(BaseModel):
    """Common item payload fields."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=300)


class ItemCreate(ItemBase):
    """Payload model for creating an item."""


class ItemUpdate(ItemBase):
    """Payload model for updating an item."""


class Item(ItemBase):
    """Stored item model including identifier."""

    id: int


app = FastAPI(title="Creative Items API")

items: list[Item] = [
    Item(
        id=1,
        name="Nebula Notebook",
        description="A journal that glows softly under moonlight.",
    ),
    Item(
        id=2,
        name="Quantum Quill",
        description="A pen that switches ink color based on mood.",
    ),
    Item(
        id=3,
        name="Aurora Mug",
        description="A mug that reveals constellations with hot drinks.",
    ),
    Item(
        id=4,
        name="Echo Lantern",
        description="A lantern that hums calming forest sounds.",
    ),
    Item(
        id=5,
        name="Pixel Plant",
        description="A desk plant with programmable LED leaves.",
    ),
    Item(
        id=6,
        name="Comet Compass",
        description="A compass that points to your saved destinations.",
    ),
    Item(
        id=7,
        name="Nimbus Cushion",
        description="A smart cushion that adjusts firmness automatically.",
    ),
    Item(
        id=8,
        name="Prism Speaker",
        description="A speaker that syncs ambient light with music.",
    ),
    Item(
        id=9,
        name="Orbit Timer",
        description="A timer that tracks sessions with planet animations.",
    ),
    Item(
        id=10,
        name="Solar Sketchpad",
        description="A reusable sketchpad charged by sunlight.",
    ),
]
items_lock = Lock()


@app.get("/", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    """Return a basic service health message."""
    return {"message": "API is healthy"}


@app.get("/items", response_model=list[Item], status_code=status.HTTP_200_OK)
def get_items() -> list[Item]:
    """Return all items from the in-memory store."""
    with items_lock:
        return list(items)


@app.get(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
)
def get_item_by_id(item_id: int) -> Item:
    """Return one item by its ID or raise 404 if not found."""
    with items_lock:
        item = next(
            (stored_item for stored_item in items if stored_item.id == item_id),
            None,
        )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    """Create a new item and return it."""
    with items_lock:
        next_id = max((item.id for item in items), default=0) + 1
        created_item = Item(id=next_id, **payload.model_dump())
        items.append(created_item)
    return created_item


@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    """Update an existing item by ID or raise 404 if not found."""
    with items_lock:
        for index, stored_item in enumerate(items):
            if stored_item.id == item_id:
                updated_item = Item(id=item_id, **payload.model_dump())
                items[index] = updated_item
                return updated_item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with ID {item_id} not found",
    )


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> Response:
    """Delete an item by ID or raise 404 if not found."""
    with items_lock:
        for index, stored_item in enumerate(items):
            if stored_item.id == item_id:
                items.pop(index)
                return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with ID {item_id} not found",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
