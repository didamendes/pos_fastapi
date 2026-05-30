from fastapi import Depends, FastAPI

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from api.routers.llm_router import router as llm_router  # noqa: E402
from api.routers.operacoes_router import router as operacoes_router  # noqa: E402
from api.utils import common_api_token  # noqa: E402

app = FastAPI(dependencies=[Depends(common_api_token)])

app.include_router(router=llm_router, tags=["IA"])
app.include_router(router=operacoes_router, tags=["Operações matemáticas"])
