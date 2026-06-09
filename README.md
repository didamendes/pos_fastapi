# 🚀 pos_fastapi

Projeto desenvolvido como parte da **Pós-Graduação na UFG**, com o objetivo de estudar e praticar o desenvolvimento de APIs RESTful utilizando o framework **FastAPI** com boas práticas de mercado.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Executando o Projeto](#-executando-o-projeto)
- [Autenticação](#-autenticação)
- [Endpoints Disponíveis](#-endpoints-disponíveis)
- [Modelos de Dados](#-modelos-de-dados)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Licença](#-licença)

---

## 📖 Sobre o Projeto

Este projeto é uma API REST construída com **FastAPI**, demonstrando conceitos e boas práticas como:

- Organização em pacotes com **routers**, **models**, **config** e **security** separados
- Autenticação via **JWT (JSON Web Token)** com OAuth2 Password Flow
- Validação de dados com **Pydantic v2** (`BaseModel`, `Field`, `StrEnum`)
- Configurações centralizadas via arquivo `config.py` com `lru_cache`
- Camada de segurança isolada em `security.py` (hashing de senhas, criação e validação de JWT)
- Tratamento de erros com `HTTPException` e códigos de status HTTP semânticos
- Integração com **IA generativa** via API da **Groq** (modelo LLaMA 3.1 8B)
- Gerenciamento de variáveis de ambiente com **python-dotenv**
- Ciclo de vida da aplicação com **`lifespan`** (substituto moderno de `@app.on_event`)
- **CORS Middleware** configurado
- Documentação interativa automática (Swagger UI / ReDoc)
- Linting e formatação com **Ruff**

---

## 🛠 Tecnologias Utilizadas

| Tecnologia    | Versão      | Descrição                                      |
|---------------|-------------|------------------------------------------------|
| Python        | >= 3.13     | Linguagem de programação                       |
| FastAPI       | >= 0.136.1  | Framework web para construção de APIs          |
| Pydantic      | v2          | Validação e serialização de dados              |
| Uvicorn       | >= 0.47.0   | Servidor ASGI de alto desempenho               |
| PyJWT         | >= 2.13.0   | Criação e validação de tokens JWT              |
| pwdlib        | >= 0.3.0    | Hashing seguro de senhas (Argon2)              |
| Groq SDK      | >= 1.2.0    | Cliente Python para a API de IA da Groq        |
| python-dotenv | >= 1.2.2    | Carregamento de variáveis de ambiente via `.env` |
| Ruff          | >= 0.15.13  | Linter e formatter para Python                 |
| uv            | —           | Gerenciador de pacotes e ambientes virtuais    |

---

## ✅ Pré-requisitos

Antes de começar, verifique se você possui instalado:

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gerenciador de pacotes)
- [Git](https://git-scm.com/)

Além disso, é necessário possuir uma **chave de API da Groq** para utilizar o endpoint de geração de histórias. Crie uma conta gratuita em [console.groq.com](https://console.groq.com/) para obter sua chave.

---

## ⚙ Instalação e Configuração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/pos_fastapi.git
   cd pos_fastapi
   ```

2. **Instale as dependências:**

   ```bash
   uv sync
   ```

3. **Configure as variáveis de ambiente** (veja a seção abaixo).

---

## 🔑 Variáveis de Ambiente

Copie o arquivo de exemplo e preencha com seus valores reais:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=sua_chave_api_groq_aqui
API_TOKEN=seu_token_seguro_aqui
SECRET_KEY=sua_chave_secreta_aqui
```

Para gerar uma `SECRET_KEY` segura:

```bash
openssl rand -hex 32
```

| Variável                   | Descrição                                              | Obrigatória |
|----------------------------|--------------------------------------------------------|-------------|
| `GROQ_API_KEY`             | Chave de API da Groq para acesso aos modelos de IA     | ✅ Sim      |
| `API_TOKEN`                | Token simples de acesso à API (legado)                 | ✅ Sim      |
| `SECRET_KEY`               | Chave secreta para assinar os tokens JWT               | ✅ Sim      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do JWT em minutos (padrão: 30)   | ❌ Não      |

> ⚠️ **Importante:** Nunca versione o arquivo `.env` no repositório. Ele já está incluído no `.gitignore`.

---

## ▶ Executando o Projeto

Inicie o servidor de desenvolvimento:

```bash
uv run uvicorn api.main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000**

### 📚 Documentação Interativa

O FastAPI gera automaticamente uma documentação interativa:

| Ferramenta | URL                             |
|------------|---------------------------------|
| Swagger UI | http://127.0.0.1:8000/docs      |
| ReDoc      | http://127.0.0.1:8000/redoc     |

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)** com o fluxo **OAuth2 Password**. Todos os endpoints de operações matemáticas e IA são protegidos.

### Passo 1 — Obter o token

```bash
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secret"
```

**Resposta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Passo 2 — Usar o token nas requisições

Inclua o token no cabeçalho `Authorization`:

```
Authorization: Bearer <token>
```

> 💡 No **Swagger UI** (`/docs`), clique em **Authorize** e insira as credenciais diretamente pela interface.

**Usuário de teste disponível:**

| Campo      | Valor     |
|------------|-----------|
| `username` | `johndoe` |
| `password` | `secret`  |

---

## 🔗 Endpoints Disponíveis

### Tag: Autenticação

---

#### `POST /token`
Autentica o usuário e retorna um token JWT.

**Corpo** (`application/x-www-form-urlencoded`):

| Campo      | Tipo     | Descrição            |
|------------|----------|----------------------|
| `username` | `string` | Nome de usuário      |
| `password` | `string` | Senha do usuário     |

**Resposta:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

#### `GET /users/me/`
Retorna os dados do usuário autenticado. 🔒 *Requer token*

**Resposta:**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

---

#### `GET /users/me/items/`
Retorna os itens do usuário autenticado. 🔒 *Requer token*

**Resposta:**
```json
[
  { "item_id": "Foo", "owner": "johndoe" }
]
```

---

### Tag: Operações matemáticas 🔒 *Requer token*

---

#### `GET /operacoes/soma/{numero1}/{numero2}`
Soma dois inteiros passados como **parâmetros de caminho**.

**Exemplo:**
```
GET /operacoes/soma/10/5
```

**Resposta:**
```json
{ "resultado": 15.0 }
```

---

#### `POST /operacoes/soma`
Soma dois inteiros passados no **corpo JSON**.

**Corpo:**
```json
{ "numero1": 10, "numero2": 5 }
```

**Resposta:**
```json
{ "resultado": 15.0 }
```

---

#### `POST /operacoes/calcular`
Executa uma operação matemática entre dois números.

**Query parameter:**

| Parâmetro  | Tipo           | Valores aceitos                                   |
|------------|----------------|---------------------------------------------------|
| `operacao` | `TipoOperacao` | `soma`, `subtracao`, `multiplicacao`, `divisao`   |

**Corpo:**
```json
{ "numero1": 10, "numero2": 4 }
```

**Exemplo com cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/operacoes/calcular?operacao=multiplicacao" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"numero1": 10, "numero2": 4}'
```

**Resposta:**
```json
{ "resultado": 40.0 }
```

> ⚠️ Divisão por zero retorna `HTTP 422 Unprocessable Entity`.

---

### Tag: IA 🔒 *Requer token*

---

#### `POST /ia/gerar_historia`
Gera uma história criativa com **Inteligência Artificial** (LLaMA 3.1 8B via Groq).

**Corpo:**
```json
{ "tema": "um astronauta perdido em Marte" }
```

**Exemplo com cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/ia/gerar_historia" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"tema": "um astronauta perdido em Marte"}'
```

**Resposta:**
```json
{
  "historia": "Era uma vez um astronauta chamado Lucas, que embarcou em uma missão solitária rumo a Marte..."
}
```

> 💡 Este endpoint pode levar alguns segundos, pois faz uma chamada externa à API da Groq.

---

## 📦 Modelos de Dados

### `Numeros`
```python
class Numeros(BaseModel):
    numero1: int
    numero2: int
```

### `ResultadoOperacao`
```python
class ResultadoOperacao(BaseModel):
    resultado: float
```

### `TipoOperacao`
```python
class TipoOperacao(StrEnum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"
```

### `Historia`
```python
class Historia(BaseModel):
    tema: str = Field(..., description="O tema da história a ser gerada")
```

### `Token`
```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

### `User`
```python
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
```

---

## 📁 Estrutura do Projeto

```
pos_fastapi/
├── api/
│   ├── __init__.py
│   ├── config.py           # Configurações centralizadas (env vars)
│   ├── main.py             # Ponto de entrada da aplicação
│   ├── models.py           # Schemas Pydantic (request/response)
│   ├── security.py         # JWT, hashing de senhas e dependências de auth
│   ├── utils.py            # Integração com o LLM (Groq)
│   └── routers/
│       ├── __init__.py
│       ├── auth_router.py       # Endpoints de autenticação
│       ├── llm_router.py        # Endpoints de IA
│       └── operacoes_router.py  # Endpoints de operações matemáticas
├── .env                    # Variáveis de ambiente (não versionado)
├── .env.example            # Template do .env (seguro para commitar)
├── .gitignore
├── .pre-commit-config.yaml # Hooks de pre-commit (ruff, etc.)
├── client.py               # Biblioteca cliente de exemplo para a API
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml          # Configuração do projeto e dependências
├── REFATORACAO.txt         # Histórico das melhorias aplicadas
├── uv.lock
└── README.md
```

---

## 📝 Licença

Este projeto é de uso acadêmico, desenvolvido para fins de estudo na **Pós-Graduação — UFG**.
