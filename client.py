"""
client.py
---------
Biblioteca cliente para a API pos_fastapi.

Uso básico::

    from client import APIClient, TipoOperacao

    client = APIClient(base_url="http://localhost:8000", api_token="123")

    # Operações matemáticas
    print(client.soma(10, 5))
    print(client.soma_formato2(10, 5))
    print(client.soma_formato3(10, 5))
    print(client.operacao_matematica(10, 5, TipoOperacao.divisao))

    # IA — gerar história
    print(client.gerar_historia("aventura no espaço"))
"""

from __future__ import annotations

from enum import Enum
from typing import Any

import requests


# ---------------------------------------------------------------------------
# Tipos públicos (espelham os models da API)
# ---------------------------------------------------------------------------


class TipoOperacao(str, Enum):
    """
    Operações matemáticas suportadas pelo endpoint /operacao_matematica.

    Valores disponíveis
    -------------------
    soma
        Adição entre dois números.
    subtracao
        Subtração entre dois números.
    multiplicacao
        Multiplicação entre dois números.
    divisao
        Divisão entre dois números.

    Exemplo::

        from client import TipoOperacao

        op = TipoOperacao.soma         # "soma"
        op = TipoOperacao.subtracao    # "subtracao"
        op = TipoOperacao.multiplicacao  # "multiplicacao"
        op = TipoOperacao.divisao      # "divisao"
    """

    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------


class APIError(Exception):
    """
    Erro retornado pela API (status HTTP >= 400).

    Atributos
    ---------
    status_code : int
        Código HTTP retornado pela API.
    detail : Any
        Mensagem de detalhe retornada pela API.

    Exemplo::

        from client import APIClient, APIError

        client = APIClient(api_token="123")
        try:
            client.soma(10, 5)
        except APIError as e:
            print(e.status_code)  # ex: 422
            print(e.detail)       # ex: "valor inválido"
    """

    def __init__(self, status_code: int, detail: Any) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"[{status_code}] {detail}")


class TokenInvalidoError(APIError):
    """
    Erro lançado quando o token de autenticação é inválido (HTTP 401).

    Herda de :class:`APIError`.

    Exemplo::

        from client import APIClient, TokenInvalidoError

        client = APIClient(api_token="token_errado")
        try:
            client.soma(1, 1)
        except TokenInvalidoError as e:
            print("Token inválido!", e)
    """


# ---------------------------------------------------------------------------
# Cliente principal
# ---------------------------------------------------------------------------


class APIClient:
    """
    Cliente para a API pos_fastapi.

    Encapsula todos os endpoints da API em métodos Python simples,
    injetando automaticamente o token de autenticação em cada requisição.

    Parâmetros
    ----------
    base_url : str
        URL base da API. Padrão: ``"http://localhost:8000"``.
    api_token : str
        Token de autenticação configurado no servidor (variável ``API_TOKEN`` no ``.env``).
    timeout : int
        Tempo limite em segundos para cada requisição. Padrão: ``30``.

    Exemplo de instanciação::

        from client import APIClient

        # Configuração mínima
        client = APIClient(api_token="123")

        # Configuração completa
        client = APIClient(
            base_url="http://meu-servidor.com",
            api_token="meu_token_secreto",
            timeout=60,
        )
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_token: str = "",
        timeout: int = 30,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout
        self._session = requests.Session()

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _params_auth(self, extra: dict | None = None) -> dict:
        """Retorna os query params base com o token de autenticação."""
        params = {"api_token": self.api_token}
        if extra:
            params.update(extra)
        return params

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict | None = None,
        json: dict | None = None,
    ) -> Any:
        """Executa uma requisição HTTP e trata erros de forma unificada."""
        url = f"{self.base_url}{path}"
        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=self.timeout,
        )
        if response.status_code == 401:
            raise TokenInvalidoError(
                401, response.json().get("detail", "Token inválido")
            )
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise APIError(response.status_code, detail)
        return response.json()

    # ------------------------------------------------------------------
    # Tag: Operações matemáticas
    # ------------------------------------------------------------------

    def soma(self, numero1: int, numero2: int) -> int:
        """
        Soma dois números inteiros via path parameters.

        Chama ``GET /soma/{numero1}/{numero2}``.

        Parâmetros
        ----------
        numero1 : int
            Primeiro número inteiro.
        numero2 : int
            Segundo número inteiro.

        Retorna
        -------
        int
            Resultado da soma de ``numero1`` e ``numero2``.

        Exemplo::

            from client import APIClient

            client = APIClient(api_token="123")

            resultado = client.soma(10, 5)
            print(resultado)  # 15

            resultado = client.soma(-3, 8)
            print(resultado)  # 5
        """
        data = self._request(
            "GET",
            f"/soma/{numero1}/{numero2}",
            params=self._params_auth(),
        )
        return data["resultado"]

    def soma_formato2(self, numero1: int, numero2: int) -> int:
        """
        Soma dois números inteiros via query parameters.

        Chama ``POST /soma_formato2?numero1=...&numero2=...``.

        Parâmetros
        ----------
        numero1 : int
            Primeiro número inteiro.
        numero2 : int
            Segundo número inteiro.

        Retorna
        -------
        int
            Resultado da soma de ``numero1`` e ``numero2``.

        Exemplo::

            from client import APIClient

            client = APIClient(api_token="123")

            resultado = client.soma_formato2(20, 3)
            print(resultado)  # 23

            resultado = client.soma_formato2(0, 100)
            print(resultado)  # 100
        """
        data = self._request(
            "POST",
            "/soma_formato2",
            params=self._params_auth({"numero1": numero1, "numero2": numero2}),
        )
        return data["resultado"]

    def soma_formato3(self, numero1: int, numero2: int) -> int:
        """
        Soma dois números inteiros via corpo JSON.

        Chama ``POST /soma_formato3`` enviando ``{"numero1": ..., "numero2": ...}``
        no corpo da requisição (modelo ``Numeros``).

        Parâmetros
        ----------
        numero1 : int
            Primeiro número inteiro.
        numero2 : int
            Segundo número inteiro.

        Retorna
        -------
        int
            Resultado da soma de ``numero1`` e ``numero2``.

        Exemplo::

            from client import APIClient

            client = APIClient(api_token="123")

            resultado = client.soma_formato3(7, 8)
            print(resultado)  # 15

            resultado = client.soma_formato3(50, 50)
            print(resultado)  # 100
        """
        data = self._request(
            "POST",
            "/soma_formato3",
            params=self._params_auth(),
            json={"numero1": numero1, "numero2": numero2},
        )
        return data["resultado"]

    def operacao_matematica(
        self,
        numero1: int,
        numero2: int,
        operacao: TipoOperacao,
    ) -> float:
        """
        Executa uma operação matemática entre dois números.

        Chama ``POST /operacao_matematica`` enviando os números no corpo JSON
        e a operação como query parameter.

        Parâmetros
        ----------
        numero1 : int
            Primeiro número inteiro.
        numero2 : int
            Segundo número inteiro.
        operacao : TipoOperacao
            Operação desejada. Use os valores do enum :class:`TipoOperacao`:

            - ``TipoOperacao.soma``          → adição
            - ``TipoOperacao.subtracao``     → subtração
            - ``TipoOperacao.multiplicacao`` → multiplicação
            - ``TipoOperacao.divisao``       → divisão

        Retorna
        -------
        float
            Resultado numérico da operação.

        Levanta
        -------
        APIError
            Se ``numero2`` for ``0`` e a operação for ``divisao``,
            a API retornará erro (divisão por zero).

        Exemplo::

            from client import APIClient, TipoOperacao

            client = APIClient(api_token="123")

            # Soma
            print(client.operacao_matematica(10, 2, TipoOperacao.soma))
            # 12

            # Subtração
            print(client.operacao_matematica(10, 2, TipoOperacao.subtracao))
            # 8

            # Multiplicação
            print(client.operacao_matematica(10, 2, TipoOperacao.multiplicacao))
            # 20

            # Divisão
            print(client.operacao_matematica(10, 2, TipoOperacao.divisao))
            # 5.0

            # Iterando por todas as operações
            for op in TipoOperacao:
                resultado = client.operacao_matematica(10, 2, op)
                print(f"{op.value}: {resultado}")
        """
        data = self._request(
            "POST",
            "/operacao_matematica",
            params=self._params_auth({"operacao": operacao.value}),
            json={"numero1": numero1, "numero2": numero2},
        )
        return data["resultado"]

    # ------------------------------------------------------------------
    # Tag: IA
    # ------------------------------------------------------------------

    def gerar_historia(self, tema: str) -> str:
        """
        Gera uma história usando IA (Groq / LLaMA 3) com base no tema informado.

        Chama ``POST /gerar_historia`` enviando ``{"tema": ...}`` no corpo JSON.

        .. note::
            Este endpoint pode levar alguns segundos para responder,
            pois faz uma chamada à API da Groq. Considere aumentar
            o ``timeout`` ao instanciar o cliente para temas complexos.

        Parâmetros
        ----------
        tema : str
            Tema livre da história a ser gerada. Quanto mais descritivo,
            melhor tende a ser o resultado gerado pela IA.

        Retorna
        -------
        str
            Texto completo da história gerada pela IA.

        Exemplo::

            from client import APIClient

            # Recomendado aumentar o timeout para chamadas de IA
            client = APIClient(api_token="123", timeout=120)

            # Tema simples
            historia = client.gerar_historia("um gato astronauta")
            print(historia)

            # Tema mais detalhado (tende a gerar histórias melhores)
            historia = client.gerar_historia(
                "uma princesa guerreira que descobre ter poderes mágicos "
                "durante uma batalha no século XII"
            )
            print(historia)

            # Salvando a história em um arquivo
            historia = client.gerar_historia("dragões medievais")
            with open("historia.txt", "w", encoding="utf-8") as f:
                f.write(historia)
        """
        data = self._request(
            "POST",
            "/gerar_historia",
            params=self._params_auth(),
            json={"tema": tema},
        )
        return data["historia"]
