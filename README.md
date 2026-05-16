# 🚀 pos_fastapi

Projeto desenvolvido como parte da **Pós-Graduação na UFG**, com o objetivo de estudar e praticar o desenvolvimento de APIs RESTful utilizando o framework **FastAPI**.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Executando o Projeto](#-executando-o-projeto)
- [Endpoints Disponíveis](#-endpoints-disponíveis)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Licença](#-licença)

---

## 📖 Sobre o Projeto

Este projeto é uma API REST construída com **FastAPI**, um framework moderno, rápido e de alto desempenho para Python. Ele serve como base de estudos para a disciplina de desenvolvimento de APIs na pós-graduação, demonstrando conceitos como:

- Criação de rotas (endpoints)
- Parâmetros de caminho (path parameters)
- Tipagem automática e validação de dados
- Documentação interativa automática (Swagger UI / ReDoc)

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Versão       | Descrição                                  |
|------------|--------------|---------------------------------------------|
| Python     | >= 3.13      | Linguagem de programação                    |
| FastAPI    | >= 0.136.1   | Framework web para construção de APIs       |
| Uvicorn    | >= 0.47.0    | Servidor ASGI de alto desempenho            |
| uv         | —            | Gerenciador de pacotes e ambientes virtuais |

---

## ✅ Pré-requisitos

Antes de começar, verifique se você possui instalado:

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (gerenciador de pacotes)
- [Git](https://git-scm.com/)

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

## 🔗 Endpoints Disponíveis

### `GET /teste`

Retorna uma mensagem de teste.

**Resposta:**

```json
{
  "mensagem": " Hello World"
}
```

---

### `GET /soma/{numero1}/{numero2}`

Realiza a soma de dois números inteiros passados como parâmetros de caminho.

**Parâmetros:**

| Parâmetro  | Tipo  | Descrição              |
|------------|-------|------------------------|
| `numero1`  | `int` | Primeiro número inteiro |
| `numero2`  | `int` | Segundo número inteiro  |

**Exemplo de requisição:**

```
GET /soma/5/3
```

**Resposta:**

```json
{
  "resultado": 8
}
```

---

## 📁 Estrutura do Projeto

```
pos_fastapi/
├── .gitignore          # Regras de arquivos ignorados pelo Git
├── main.py             # Aplicação principal com os endpoints
├── pyproject.toml      # Configuração do projeto e dependências
├── uv.lock             # Lock file das dependências
└── README.md           # Documentação do projeto
```

---

## 📝 Licença

Este projeto é de uso acadêmico, desenvolvido para fins de estudo na **Pós-Graduação — UFG**.