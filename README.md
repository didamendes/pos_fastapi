# 🚀 pos_fastapi

Projeto desenvolvido como parte da **Pós-Graduação na UFG**, com o objetivo de estudar e praticar o desenvolvimento de APIs RESTful utilizando o framework **FastAPI**.

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

Este projeto é uma API REST construída com **FastAPI**, um framework moderno, rápido e de alto desempenho para Python. Ele serve como base de estudos para a disciplina de desenvolvimento de APIs na pós-graduação, demonstrando conceitos como:

- Criação de rotas (endpoints) com métodos `GET` e `POST`
- Parâmetros de caminho (path parameters) e query parameters
- Validação de dados com **Pydantic** (`BaseModel` e `Field`)
- Uso de **Enums** para restringir valores aceitos
- Autenticação via **API Token** com dependências globais (`Depends`)
- Tratamento de erros com `HTTPException` e códigos de status HTTP
- Integração com **IA generativa** via API da **Groq** (modelo LLaMA 3.1)
- Gerenciamento de variáveis de ambiente com **python-dotenv**
- Marcação de endpoints como **deprecated**
- Organização de endpoints por **tags**
- Documentação interativa automática (Swagger UI / ReDoc)

---

## 🛠 Tecnologias Utilizadas

| Tecnologia     | Versão       | Descrição                                       |
|----------------|--------------|--------------------------------------------------|
| Python         | >= 3.13      | Linguagem de programação                         |
| FastAPI        | >= 0.136.1   | Framework web para construção de APIs            |
| Pydantic       | —            | Validação e serialização de dados                |
| Uvicorn        | >= 0.47.0    | Servidor ASGI de alto desempenho                 |
| Groq SDK       | >= 1.2.0     | Cliente Python para a API de IA da Groq          |
| python-dotenv  | —            | Carregamento de variáveis de ambiente via `.env`  |
| Ruff           | >= 0.15.13   | Linter e formatter para Python                   |
| uv             | —            | Gerenciador de pacotes e ambientes virtuais       |

---

## ✅ Pré-requisitos

Antes de começar, verifique se você possui instalado:

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gerenciador de pacotes)
- [Git](https://git-scm.com/)

Além disso, é necessário possuir uma **chave de API da Groq** para utilizar o endpoint de geração de histórias com IA. Crie uma conta gratuita em [console.groq.com](https://console.groq.com/) para obter sua chave.

---

## ⚙ Instalação e Configuração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/pos_fastapi.git
   cd pos_fastapi
   ```

2. **Crie e ative o ambiente virtual:**

   ```bash
   uv venv
   ```

   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```

   - **Linux / macOS:**
     ```bash
     source .venv/bin/activate
     ```

3. **Instale as dependências:**

   ```bash
   uv sync
   ```

4. **Configure as variáveis de ambiente** (veja a seção abaixo).

---

## 🔑 Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para armazenar configurações sensíveis. Crie o arquivo `.env` na raiz do projeto com base no exemplo abaixo:

```env
GROQ_API_KEY=sua_chave_api_aqui
```

| Variável       | Descrição                                                     | Obrigatória |
|----------------|---------------------------------------------------------------|-------------|
| `GROQ_API_KEY` | Chave de API da Groq para acesso aos modelos de IA (LLaMA)   | ✅ Sim       |

> ⚠️ **Importante:** Nunca versione o arquivo `.env` no repositório. Ele já está incluído no `.gitignore`.

---

## ▶ Executando o Projeto

Inicie o servidor de desenvolvimento com o comando:

```bash
fastapi dev main.py
```

Ou, alternativamente, utilizando o Uvicorn diretamente:

```bash
uvicorn main:app --reload
```

A API estará disponível em: **http://127.0.0.1:8000**

### 📚 Documentação Interativa

O FastAPI gera automaticamente uma documentação interativa para a API:

| Ferramenta | URL                                      |
|------------|------------------------------------------|
| Swagger UI | http://127.0.0.1:8000/docs               |
| ReDoc      | http://127.0.0.1:8000/redoc              |

---

## 🔐 Autenticação

Todas as rotas da API são protegidas por um **API Token** global, configurado como dependência do FastAPI via `Depends`.

Para acessar qualquer endpoint, é necessário enviar o parâmetro `api_token` na query string:

```
GET /teste?api_token=123
```

Se o token for inválido ou não fornecido, a API retorna:

```json
{
  "detail": "Token inválido"
}
```

**Status HTTP:** `401 Unauthorized`

---

## 🔗 Endpoints Disponíveis

### `GET /teste`

Retorna uma mensagem de teste.

**Tag:** —

**Exemplo de requisição:**

```
GET /teste?api_token=123
```

**Resposta:**

```json
{
  "mensagem": " Hello World"
}
```

---

### `GET /soma/{numero1}/{numero2}`

Realiza a soma de dois números inteiros passados como **parâmetros de caminho**.

**Tag:** `Operações matemáticas`

**Parâmetros de caminho:**

| Parâmetro  | Tipo  | Descrição              |
|------------|-------|------------------------|
| `numero1`  | `int` | Primeiro número inteiro |
| `numero2`  | `int` | Segundo número inteiro  |

**Exemplo de requisição:**

```
GET /soma/5/3?api_token=123
```

**Resposta:**

```json
{
  "resultado": 8
}
```

---

### `POST /soma_formato2`

Realiza a soma de dois números inteiros passados como **query parameters**.

**Tag:** `Operações matemáticas`

**Query parameters:**

| Parâmetro  | Tipo  | Descrição              |
|------------|-------|------------------------|
| `numero1`  | `int` | Primeiro número inteiro |
| `numero2`  | `int` | Segundo número inteiro  |

**Exemplo de requisição:**

```
POST /soma_formato2?numero1=5&numero2=3&api_token=123
```

**Resposta:**

```json
{
  "resultado": 8
}
```

---

### `POST /soma_formato3` ⚠️ *Deprecated*

Realiza a soma de dois números inteiros enviados no **corpo da requisição** usando o modelo `Numeros`.

> **Nota:** Este endpoint está marcado como **deprecated** e poderá ser removido em versões futuras.

**Tag:** `Operações matemáticas`

**Corpo da requisição (JSON):**

```json
{
  "numero1": 5,
  "numero2": 3
}
```

**Exemplo com cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/soma_formato3?api_token=123" \
  -H "Content-Type: application/json" \
  -d '{"numero1": 5, "numero2": 3}'
```

**Resposta:**

```json
{
  "resultado": 8
}
```

---

### `POST /operacao_matematica`

Realiza uma operação matemática (soma, subtração, multiplicação ou divisão) entre dois números, de acordo com o tipo de operação informado via query parameter.

**Tag:** `Operações matemáticas`

**Query parameters:**

| Parâmetro  | Tipo             | Descrição                                                |
|------------|------------------|----------------------------------------------------------|
| `operacao` | `TipoOperacao`   | Tipo da operação: `soma`, `subtracao`, `multiplicacao`, `divisao` |

**Corpo da requisição (JSON):**

```json
{
  "numero1": 10,
  "numero2": 4
}
```

**Exemplo com cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/operacao_matematica?operacao=multiplicacao&api_token=123" \
  -H "Content-Type: application/json" \
  -d '{"numero1": 10, "numero2": 4}'
```

**Resposta:**

```json
{
  "resultado": 40
}
```

**Valores aceitos para `operacao`:**

| Valor            | Operação        |
|------------------|-----------------| 
| `soma`           | Adição          |
| `subtracao`      | Subtração       |
| `multiplicacao`  | Multiplicação   |
| `divisao`        | Divisão         |

---

### `POST /gerar_historia` 🤖

Gera uma história criativa utilizando **Inteligência Artificial** (modelo **LLaMA 3.1 8B** via API da **Groq**) com base em um tema fornecido pelo usuário.

**Tag:** —

**Corpo da requisição (JSON):**

```json
{
  "tema": "um astronauta perdido em Marte"
}
```

| Campo  | Tipo   | Obrigatório | Descrição                              |
|--------|--------|-------------|----------------------------------------|
| `tema` | `str`  | ✅ Sim       | O tema da história a ser gerada        |

**Exemplo com cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/gerar_historia?api_token=123" \
  -H "Content-Type: application/json" \
  -d '{"tema": "um astronauta perdido em Marte"}'
```

**Resposta:**

```json
{
  "historia": "Era uma vez um astronauta chamado Lucas, que embarcou em uma missão solitária rumo a Marte..."
}
```

> 💡 **Nota:** Este endpoint depende da variável de ambiente `GROQ_API_KEY` configurada corretamente no arquivo `.env`.

---

## 📦 Modelos de Dados

### `Numeros` (Pydantic BaseModel)

Modelo utilizado para receber dois números inteiros no corpo das requisições.

```python
class Numeros(BaseModel):
    numero1: int
    numero2: int
```

### `TipoOperacao` (Enum)

Enumeração que define os tipos de operações matemáticas disponíveis.

```python
class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"
```

### `Historia` (Pydantic BaseModel)

Modelo utilizado para receber o tema da história a ser gerada pela IA.

```python
class Historia(BaseModel):
    tema: str = Field(..., description="O tema da historia a ser gerada")
```

---

## 📁 Estrutura do Projeto

```
pos_fastapi/
├── .env                # Variáveis de ambiente (não versionado)
├── .gitignore          # Regras de arquivos ignorados pelo Git
├── main.py             # Aplicação principal com os endpoints
├── pyproject.toml      # Configuração do projeto e dependências
├── uv.lock             # Lock file das dependências
└── README.md           # Documentação do projeto
```

---

## 📝 Licença

Este projeto é de uso acadêmico, desenvolvido para fins de estudo na **Pós-Graduação — UFG**.