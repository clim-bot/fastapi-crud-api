from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from app.database import SessionLocal
from app.schemas import ItemCreate, ItemResponse, UserCreate, UserResponse, UserLogin, Token
from app.crud import (
    SECRET_KEY, ALGORITHM, create_item, get_item, get_items,
    update_item, delete_item, create_user, authenticate_user, create_access_token
)
from app.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    """
    Dependency that provides a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Validates JWT token and retrieves current authenticated user.
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid authentication credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/users", response_model=UserResponse, summary="Register a new user", description="Creates a new user with a hashed password.")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user. If the username is taken, returns a 400 error.
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)

@router.post("/login", response_model=Token, summary="User login", description="Authenticates a user and returns a JWT token.")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and generates a JWT token.
    """
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token({"sub": db_user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/items", response_model=ItemResponse, summary="Create a new item", description="Adds an item to the database and returns it.")
def create_new_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Creates a new item, only accessible to authenticated users.
    """
    return create_item(db, item)

@router.get("/items", response_model=list[ItemResponse], summary="Retrieve all items", description="Returns a list of all items in the database.")
def read_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetches all items in the database, requires authentication.
    """
    return get_items(db)

@router.get("/items/{item_id}", response_model=ItemResponse, summary="Retrieve a specific item", description="Fetches an item by its ID. Returns 404 if not found.")
def read_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetches a single item by ID, requires authentication.
    """
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=ItemResponse, summary="Update an existing item", description="Updates an existing item by ID. Returns 404 if the item is not found.")
def update_existing_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Updates an item by ID, requires authentication.
    """
    updated_item = update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", summary="Delete an item", description="Deletes an item from the database by ID. Returns success or failure message.")
def delete_existing_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes an item by ID, requires authentication.
    """
    return delete_item(db, item_id)
