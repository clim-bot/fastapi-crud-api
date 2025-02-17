from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import ItemCreate, ItemResponse
from app.crud import create_item, get_item, get_items, update_item, delete_item

router = APIRouter()

def get_db():
    """
    Creates a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items", response_model=ItemResponse, summary="Create a new item", description="Adds an item to the database and returns it.")
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/items", response_model=list[ItemResponse], summary="Retrieve all items", description="Returns a list of all items in the database.")
def read_items(db: Session = Depends(get_db)):
    return get_items(db)

@router.get("/items/{item_id}", response_model=ItemResponse, summary="Retrieve a specific item", description="Fetches an item by its ID. Returns 404 if not found.")
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=ItemResponse, summary="Update an existing item", description="Updates an existing item by ID. Returns 404 if the item is not found.")
def update_existing_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", summary="Delete an item", description="Deletes an item from the database by ID. Returns success or failure message.")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db, item_id)
