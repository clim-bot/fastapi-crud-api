from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str