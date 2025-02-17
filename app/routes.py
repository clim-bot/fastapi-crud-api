from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import ItemCreate, ItemResponse
from app.crud import create_item, get_item, get_items, update_item, delete_item

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items", response_model=ItemResponse)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/items", response_model=list[ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)

@router.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=ItemResponse)
def update_existing_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    return delete_item(db, item_id)