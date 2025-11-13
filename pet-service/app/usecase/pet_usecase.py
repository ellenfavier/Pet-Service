from datetime import datetime
from app.domain.repositories import IPetRepository
from app.domain.entities import PetState
from app.settings import settings
import httpx
import logging # Import logging
from typing import Optional

# Get Logger
log = logging.getLogger(__name__)

class PetUseCase:
    """
    Contains all business logic related to the Pet.
    """
    def __init__(self, repo: IPetRepository):
        self.repo = repo
        self.client = httpx.AsyncClient()

    async def get_state(self, user_id: str) -> Optional[PetState]:
        return await self.repo.get_by_user_id(user_id)

    async def create_pet(self, user_id: str) -> PetState:
        # Create pet with default values
        pet = await self.repo.upsert(user_id, {"mood": 50, "health": 100})
        log.info(f"Pet created for user: {user_id}")
        
        try:
            await self.client.post(
                f"{settings.NOTIFICATION_SERVICE_URL}/notifications",
                json={
                    "user_id": user_id,
                    "message": "New pet created for you!",
                    "type": "pet",
                },
                timeout=5,
            )
        except httpx.RequestError as e:
            log.warning(f"Failed to notify notification-service for {user_id}: {e}")
        return pet

    async def delete_pet(self, user_id: str) -> bool:
        deleted = await self.repo.delete_by_user_id(user_id)
        if not deleted:
            return False
        
        log.info(f"Pet deleted for user: {user_id}")
        try:
            await self.client.post(
                f"{settings.NOTIFICATION_SERVICE_URL}/notifications",
                json={
                    "user_id": user_id,
                    "message": "Your pet was deleted.",
                    "type": "pet",
                },
                timeout=5,
            )
        except httpx.RequestError:
            pass 
        return True

    async def _get_or_create_state(self, user_id: str) -> PetState:
        state = await self.repo.get_by_user_id(user_id)
        if not state:
            state = await self.repo.upsert(user_id, {"mood": 50, "health": 100})
        return state

    async def increase_mood(self, user_id: str) -> PetState:
        state = await self._get_or_create_state(user_id)
        new_mood = min(state.mood + 10, 100)
        log.info(f"Mood increased for {user_id} to {new_mood}")
        return await self.repo.upsert(user_id, {"mood": new_mood, "last_update": datetime.utcnow()})

    async def decrease_mood(self, user_id: str) -> PetState:
        state = await self._get_or_create_state(user_id)
        new_mood = max(state.mood - 10, 0)
        updated_state = await self.repo.upsert(user_id, {"mood": new_mood, "last_update": datetime.utcnow()})
        
        log.info(f"Mood decreased for {user_id} to {new_mood}")

        if updated_state.mood < 30:
            try:
                await self.client.post(f"{settings.NOTIFICATION_SERVICE_URL}/notify/pet-low-mood/{user_id}", timeout=5)
            except httpx.RequestError:
                pass 
        return updated_state

    async def increase_health(self, user_id: str) -> PetState:
        state = await self._get_or_create_state(user_id)
        new_health = min(state.health + 10, 100)
        log.info(f"Health increased for {user_id} to {new_health}")
        return await self.repo.upsert(user_id, {"health": new_health, "last_update": datetime.utcnow()})

    async def decrease_health(self, user_id: str) -> PetState:
        state = await self._get_or_create_state(user_id)
        new_health = max(state.health - 10, 0)
        updated_state = await self.repo.upsert(user_id, {"health": new_health, "last_update": datetime.utcnow()})

        log.info(f"Health decreased for {user_id} to {new_health}")

        if updated_state.health < 30:
            try:
                await self.client.post(f"{settings.NOTIFICATION_SERVICE_URL}/notify/pet-low-health/{user_id}", timeout=5)
            except httpx.RequestError:
                pass 
        return updated_state