import fastapi

from api.models import Numeros, TipoOperacao

router = fastapi.APIRouter()


@router.get(
    path="/soma/{numero1}/{numero2}",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
)
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


@router.post(
    path="/soma_formato2",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
)
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


@router.post(
    path="/soma_formato3",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
    status_code=fastapi.status.HTTP_200_OK,
    deprecated=False,
)
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}


@router.post("/operacao_matematica")
def operacao_matematica(numeros: Numeros, operacao: TipoOperacao):
    global resultado
    if operacao == TipoOperacao.soma:
        resultado = numeros.numero1 + numeros.numero2

    elif operacao == TipoOperacao.subtracao:
        resultado = numeros.numero1 - numeros.numero2

    elif operacao == TipoOperacao.multiplicacao:
        resultado = numeros.numero1 * numeros.numero2

    elif operacao == TipoOperacao.divisao:
        resultado = numeros.numero1 / numeros.numero2

    return {"resultado": resultado}
