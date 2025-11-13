from functools import lru_cache
from fastapi import Depends
from app.domain.repositories import IPetRepository
from app.adapters.repo.mongo_pet_repo import MongoPetRepository
from app.usecase.pet_usecase import PetUseCase

@lru_cache(maxsize=1)
def get_pet_repo() -> IPetRepository:
    """Провайдер для репозитория (синглтон)."""
    return MongoPetRepository()

def get_pet_usecase(
    repo: IPetRepository = Depends(get_pet_repo)
) -> PetUseCase:
    """
    Провайдер для UseCase.
    Автоматически внедряет 'get_pet_repo' в PetUseCase.
    """
    return PetUseCase(repo=repo)