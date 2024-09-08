from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Dict
from pydantic import BaseModel
from ..auth import User, Token, create_access_token, fake_hash_password, get_current_user
from datetime import timedelta
from application.services import RetrieverService

class RankingResponse(BaseModel):
    llm_model: str
    avg_value: float
    std_dev: float

def create_router(retriever_service: RetrieverService):
    router = APIRouter()

    @router.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        # This is a mock authentication. In a real app, you'd verify against a database
        hashed_password = fake_hash_password(form_data.password)
        if not hashed_password == "fakehashed" + form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @router.get("/ranking/{metric}", response_model=List[RankingResponse])
    def get_ranking(
            metric: str,
            current_user: User = Depends(get_current_user)
    ):
        try:
            ranking = retriever_service.get_ranking(metric)
            return [RankingResponse(**item) for item in ranking]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/metrics", response_model=List[str])
    def get_available_metrics(
        current_user: User = Depends(get_current_user)
    ):
        return retriever_service.get_available_metrics()

    @router.get("/models", response_model=List[str])
    def get_available_models(
        current_user: User = Depends(get_current_user)
    ):
        return retriever_service.get_available_models()

    return router