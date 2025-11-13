from pydantic import BaseModel
from typing import Optional
from app.domain.entities import PetState

class PetStateResponse(PetState):
    """Схема ответа для состояния питомца (наследуется от сущности)."""
    pass

class PetMessageResponse(BaseModel):
    """Схема ответа 'сообщение + состояние'."""
    message: str
    state: Optional[PetStateResponse] = None

class SimpleMessageResponse(BaseModel):
    """Схема для простых ответов (например, при удалении)."""
    message: str