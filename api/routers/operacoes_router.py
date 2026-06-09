"""
Router de operações matemáticas.
Prefixo: /operacoes
"""

from fastapi import APIRouter, HTTPException, status

from api.models import Numeros, ResultadoOperacao, TipoOperacao

router = APIRouter(prefix="/operacoes")


@router.get(
    "/soma/{numero1}/{numero2}",
    response_model=ResultadoOperacao,
    summary="Soma via path",
    description="Recebe dois inteiros na URL e retorna a soma.",
)
async def soma(numero1: int, numero2: int) -> ResultadoOperacao:
    """Soma dois números recebidos como parâmetros de path."""
    return ResultadoOperacao(resultado=numero1 + numero2)


@router.post(
    "/soma",
    response_model=ResultadoOperacao,
    summary="Soma via body",
    description="Recebe dois inteiros no corpo da requisição e retorna a soma.",
    status_code=status.HTTP_200_OK,
)
async def soma_body(numeros: Numeros) -> ResultadoOperacao:
    """Soma dois números recebidos no corpo (JSON)."""
    return ResultadoOperacao(resultado=numeros.numero1 + numeros.numero2)


@router.post(
    "/calcular",
    response_model=ResultadoOperacao,
    summary="Operação matemática",
    description="Executa soma, subtração, multiplicação ou divisão entre dois números.",
    status_code=status.HTTP_200_OK,
)
async def operacao_matematica(numeros: Numeros, operacao: TipoOperacao) -> ResultadoOperacao:
    """Executa a operação matemática solicitada entre dois números."""
    if operacao == TipoOperacao.divisao and numeros.numero2 == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Divisão por zero não é permitida.",
        )

    operacoes: dict[TipoOperacao, float] = {
        TipoOperacao.soma: numeros.numero1 + numeros.numero2,
        TipoOperacao.subtracao: numeros.numero1 - numeros.numero2,
        TipoOperacao.multiplicacao: numeros.numero1 * numeros.numero2,
        TipoOperacao.divisao: numeros.numero1 / numeros.numero2,
    }
    return ResultadoOperacao(resultado=operacoes[operacao])
