from fastapi import APIRouter, Depends, HTTPException
from app.usecase.pet_usecase import PetUseCase
from app.adapters.http.schemas import PetStateResponse, PetMessageResponse, SimpleMessageResponse
from app.di import get_pet_usecase # DI

router = APIRouter(prefix="/pet-state", tags=["Pet State"])

@router.post("/create/{user_id}", response_model=PetMessageResponse)
async def create_pet(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    pet = await usecase.create_pet(user_id)
    return {"message": f"Pet created for {user_id}", "state": pet}

@router.get("/{user_id}", response_model=PetStateResponse)
async def get_state(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    state = await usecase.get_state(user_id)
    if not state:
        raise HTTPException(status_code=404, detail="Pet not found")
    return state
    
@router.delete("/{user_id}", response_model=SimpleMessageResponse)
async def delete_pet(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    deleted = await usecase.delete_pet(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"message": f"Pet for user {user_id} deleted"}
    
@router.post("/increase-mood/{user_id}", response_model=PetMessageResponse)
async def increase_mood(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    state = await usecase.increase_mood(user_id)
    return {"message": "Mood increased", "state": state}

@router.post("/decrease-mood/{user_id}", response_model=PetMessageResponse)
async def decrease_mood(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    state = await usecase.decrease_mood(user_id)
    return {"message": "Mood decreased", "state": state}
    
@router.post("/decrease-health/{user_id}", response_model=PetMessageResponse)
async def decrease_health(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    state = await usecase.decrease_health(user_id)
    return {"message": "Health decreased", "state": state}

@router.post("/increase-health/{user_id}", response_model=PetMessageResponse)
async def increase_health(user_id: str, usecase: PetUseCase = Depends(get_pet_usecase)):
    state = await usecase.increase_health(user_id)
    return {"message": "Health increased", "state": state}