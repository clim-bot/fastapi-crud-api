from sqlalchemy.orm import Session
from app.models import Item
from app.schemas import ItemCreate, ItemResponse

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session):
    return db.query(Item).all()

def create_item(db: Session, item: ItemCreate) -> ItemResponse:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemCreate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"message": "Item deleted"}
    return {"message": "Item not found"}