from fastapi import HTTPException, status
import re
from mysql.connector import Error
from app import schemas

def validate_container_number(container_number):
    pattern = r'^[A-Z]{3}U\d{7}$'
    if not re.match(pattern, container_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Container number must be in format: Three uppercase letters + 'U' + seven digits (e.g., CXXU7788345)"
        )


def get_containers(db, q: str = None):
    cursor = db.cursor(dictionary=True)
    try:
        if q:
            cursor.execute(
                "SELECT id, container_number, cost, created_at FROM containers WHERE container_number LIKE %s LIMIT 50",
                (f"%{q}%",))
        else:
            cursor.execute("SELECT id, container_number, cost, created_at FROM containers LIMIT 50")

        containers = cursor.fetchall()
        for container in containers:
            if 'cost' in container:
                container['cost'] = float(container['cost'])

        return containers
    finally:
        cursor.close()


def get_containers_by_cost(db, cost: float = None, min_cost: float = None, max_cost: float = None):
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT id, container_number, cost, created_at FROM containers"
        params = []

        if cost is not None:
            query += " WHERE cost = %s"
            params.append(cost)
        elif min_cost is not None and max_cost is not None:
            query += " WHERE cost BETWEEN %s AND %s"
            params.extend([min_cost, max_cost])
        elif min_cost is not None:
            query += " WHERE cost >= %s"
            params.append(min_cost)
        elif max_cost is not None:
            query += " WHERE cost <= %s"
            params.append(max_cost)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one cost parameter must be provided"
            )

        cursor.execute(query, params)
        containers = cursor.fetchall()

        for container in containers:
            if 'cost' in container:
                container['cost'] = float(container['cost'])

        return containers
    finally:
        cursor.close()


def create_container(db, container: schemas.ContainerCreate):
    validate_container_number(container.container_number)

    if container.cost <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cost must be a positive number"
        )

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO containers (container_number, cost) VALUES (%s, %s)",
            (container.container_number, container.cost)
        )
        db.commit()
        container_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, container_number, cost, created_at FROM containers WHERE id = %s",
            (container_id,)
        )
        new_container = cursor.fetchone()

        if new_container and 'cost' in new_container:
            new_container['cost'] = float(new_container['cost'])

        return new_container
    except Error as e:
        db.rollback()
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Container with this number already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create container: {e}"
        )
    finally:
        cursor.close()