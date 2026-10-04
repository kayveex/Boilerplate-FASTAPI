from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["Items"])


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(db)


@router.get("", response_model=List[ItemResponse])
def get_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    return service.list_items(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    return service.get_item(item_id)


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service)
):
    return service.create_item(payload)


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    return service.remove_item(item_id)
