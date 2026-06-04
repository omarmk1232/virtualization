from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Product])
def list_products(available_only: bool = False, db: Session = Depends(get_db)):
    return crud.get_products(db, available_only=available_only)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.patch("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, updates: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, updates)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)
