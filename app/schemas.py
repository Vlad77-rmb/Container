from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Схемы для сериализации данных
class ContainerBase(BaseModel):
    container_number: str
    cost: float

class ContainerCreate(ContainerBase):
    pass

class Container(ContainerBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ContainerSearch(BaseModel):
    q: Optional[str] = None

class ContainerCostFilter(BaseModel):
    cost: Optional[float] = None
    min_cost: Optional[float] = None
    max_cost: Optional[float] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None