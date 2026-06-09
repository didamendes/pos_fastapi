"""
Ponto de entrada da aplicação FastAPI.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_settings
from api.routers.auth_router import router as auth_router
from api.routers.llm_router import router as llm_router
from api.routers.operacoes_router import router as operacoes_router
from api.security import get_current_active_user

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Gerencia o ciclo de vida da aplicação (startup / shutdown)."""
    # Inicialização: coloque aqui conexões a banco, warm-up de modelos etc.
    yield
    # Encerramento: feche conexões, libere recursos etc.


app = FastAPI(
    title="Pos FastAPI",
    description=(
        "API de exemplo com autenticação JWT, operações matemáticas "
        "e geração de histórias via IA (Groq/Llama)."
    ),
    version="0.1.0",
    contact={"name": "Equipe UFG"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_router, tags=["Autenticação"])
app.include_router(
    router=llm_router,
    tags=["IA"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    router=operacoes_router,
    tags=["Operações matemáticas"],
    dependencies=[Depends(get_current_active_user)],
)
