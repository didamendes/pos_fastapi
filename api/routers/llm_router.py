from fastapi import APIRouter

from api.models import Historia
from api.utils import gerar_historio

router = APIRouter()


@router.post("/gerar_historia")
def gerar_historia(historia: Historia):
    return {"historia": gerar_historio(historia)}
