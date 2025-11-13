from app.domain.repositories import IPetRepository
from app.domain.entities import PetState
from app.infrastructure.db import db
from typing import Optional, Dict, Any

def _pet_serializer(pet) -> Optional[PetState]:
    """
    Приватный сериализатор (из crud.py).
    Конвертирует документ MongoDB в Pydantic-модель PetState.
    """
    if not pet:
        return None
    return PetState(
        id=str(pet["_id"]),
        user_id=pet["user_id"],
        mood=pet.get("mood", 50),
        health=pet.get("health", 100)
    )

class MongoPetRepository(IPetRepository):
    
    async def get_by_user_id(self, user_id: str) -> Optional[PetState]:
        """Реализация get_pet_state из crud.py"""
        pet = db.pet_states.find_one({"user_id": user_id})
        return _pet_serializer(pet)

    async def upsert(self, user_id: str, changes: Dict[str, Any]) -> PetState:
        """
        Реализация create_or_update_pet_state из crud.py.
        Объединяет 'create' и 'update' в один вызов.
        """
        pet_doc = db.pet_states.find_one({"user_id": user_id})
        
        if not pet_doc:
            # Логика создания
            state = {
                "user_id": user_id,
                "mood": 50,
                "health": 100
            }
            state.update(changes)
            result = db.pet_states.insert_one(state)
            new_pet = db.pet_states.find_one({"_id": result.inserted_id})
        else:
            # Логика обновления
            db.pet_states.update_one({"user_id": user_id}, {"$set": changes})
            new_pet = db.pet_states.find_one({"user_id": user_id})
        
        return _pet_serializer(new_pet)

    async def delete_by_user_id(self, user_id: str) -> bool:
        """Реализация delete_pet_state из crud.py"""
        result = db.pet_states.delete_one({"user_id": user_id})
        return result.deleted_count > 0