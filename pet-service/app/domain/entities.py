from pydantic import BaseModel
from typing import Optional

class PetState(BaseModel):
    id: Optional[str] = None
    user_id: str
    mood: int
    health: int