"""
Router de geração de conteúdo via LLM.
Prefixo: /ia
"""

from fastapi import APIRouter

from api.models import Historia, HistoriaResponse
from api.utils import gerar_historia

router = APIRouter(prefix="/ia")


@router.post(
    "/gerar_historia",
    response_model=HistoriaResponse,
    summary="Gerar história",
    description=(
        "Gera uma história sobre o tema fornecido usando inteligência artificial (Groq/Llama)."
    ),
)
def gerar_historia_endpoint(historia: Historia) -> HistoriaResponse:
    """Gera uma história usando o modelo LLM da Groq."""
    texto = gerar_historia(historia)
    return HistoriaResponse(historia=texto)
