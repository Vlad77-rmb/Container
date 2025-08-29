from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from app import schemas, auth, crud

load_dotenv()

app = FastAPI(title="Container Service API", docs_url="/docs")
security = HTTPBasic()

# Подключение к базе данных
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {e}"
        )

#
@app.get("/api/containers", response_model=List[schemas.Container])
def get_containers(
    q: Optional[str] = None,
    credentials: HTTPBasicCredentials = Depends(security),
    db = Depends(get_db_connection)
):
    auth.authenticate_user(credentials, db)
    return crud.get_containers(db, q)

@app.get("/api/containers/by-cost", response_model=List[schemas.Container])
def get_containers_by_cost(
    cost: Optional[float] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None,
    credentials: HTTPBasicCredentials = Depends(security),
    db = Depends(get_db_connection)
):
    auth.authenticate_user(credentials, db)
    return crud.get_containers_by_cost(db, cost, min_cost, max_cost)

@app.post("/api/containers", response_model=schemas.Container)
def create_container(
    container: schemas.ContainerCreate,
    credentials: HTTPBasicCredentials = Depends(security),
    db = Depends(get_db_connection)
):
    auth.authenticate_user(credentials, db)
    return crud.create_container(db, container)