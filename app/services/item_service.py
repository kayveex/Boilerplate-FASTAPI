from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemResponse


class ItemService:
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)

    def list_items(self, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
        items = self.repository.get_all(skip=skip, limit=limit)
        return [ItemResponse.model_validate(item) for item in items]

    def get_item(self, item_id: int) -> ItemResponse:
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        return ItemResponse.model_validate(item)

    def create_item(self, payload: ItemCreate) -> ItemResponse:
        created = self.repository.create(payload)
        return ItemResponse.model_validate(created)

    def remove_item(self, item_id: int) -> dict:
        deleted = self.repository.delete(item_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        return {"message": f"Item {item_id} successfully deleted"}
