from pydantic import BaseModel, validator, constr
import re
from typing import Optional
from datetime import datetime

# Модели для валидации запросов и ответов API
class ContainerBase(BaseModel):
    container_number: str
    cost: float

    @validator('container_number')
    def validate_container_number(cls, v):
        pattern = r'^[A-Z]{3}U\d{7}$'
        if not re.match(pattern, v):
            raise ValueError('Container number must be in format: Three uppercase letters + "U" + seven digits')
        return v

    @validator('cost')
    def validate_cost(cls, v):
        if v <= 0:
            raise ValueError('Cost must be a positive number')
        return round(v, 2)

class ContainerCreate(ContainerBase):
    pass

class Container(ContainerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ContainerResponse(BaseModel):
    id: int
    container_number: str
    cost: float
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime