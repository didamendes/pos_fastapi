from fastapi import Depends, FastAPI

from api.routers.llm_router import router as llm_router
from api.routers.operacoes_router import router as operacoes_router
from api.utils import common_api_token

app = FastAPI(dependencies=[Depends(common_api_token)])

app.include_router(router=llm_router, tags=["IA"])
app.include_router(router=operacoes_router, tags=["Operações matemáticas"])
