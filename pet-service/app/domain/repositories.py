from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.domain.entities import PetState

class IPetRepository(ABC):
    """
    Интерфейс для работы с данными о состоянии питомца.
    """
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[PetState]:
        """Получить состояние питомца по ID пользователя."""
        pass
    
    @abstractmethod
    async def upsert(self, user_id: str, changes: Dict[str, Any]) -> PetState:
        """
        Создать или обновить состояние питомца.
        'changes' - словарь с полями для обновления (например, {"mood": 60}).
        """
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: str) -> bool:
        """Удалить питомца по ID пользователя."""
        pass