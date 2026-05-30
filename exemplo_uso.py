"""
exemplo_uso.py
--------------
Demonstração de como usar a biblioteca client.py.

Execute com:
    python exemplo_uso.py
"""

from client import APIClient, TipoOperacao, APIError, TokenInvalidoError

# -----------------------------------------------------------
# 1. Instanciar o cliente
# -----------------------------------------------------------
client = APIClient(
    base_url="http://localhost:8000",
    api_token="123",
)

# -----------------------------------------------------------
# 2. Operações matemáticas
# -----------------------------------------------------------

# GET /soma/{numero1}/{numero2}
resultado = client.soma(10, 5)
print(f"soma (path params):      {resultado}")  # 15

# POST /soma_formato2  (query params)
resultado = client.soma_formato2(20, 3)
print(f"soma_formato2 (query):   {resultado}")  # 23

# POST /soma_formato3  (body JSON)
resultado = client.soma_formato3(7, 8)
print(f"soma_formato3 (body):    {resultado}")  # 15

# POST /operacao_matematica
for op in TipoOperacao:
    resultado = client.operacao_matematica(10, 2, op)
    print(f"operacao_matematica ({op.value:>14}): {resultado}")

# -----------------------------------------------------------
# 3. IA — Gerar história
# -----------------------------------------------------------
print("\nGerando história, aguarde...")
historia = client.gerar_historia("um robô que aprende a sentir emoções")
print(f"\nHistória gerada:\n{historia}\n")

# -----------------------------------------------------------
# 4. Tratamento de erros
# -----------------------------------------------------------
print("Testando token inválido...")
client_invalido = APIClient(base_url="http://localhost:8000", api_token="errado")
try:
    client_invalido.soma(1, 1)
except TokenInvalidoError as e:
    print(f"Erro capturado corretamente: {e}")
except APIError as e:
    print(f"Erro genérico da API: {e}")
