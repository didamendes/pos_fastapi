# Usando a imagem do Python slim
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o código para o diretório de trabalho
COPY . .

# Instala as dependências e o projeto
RUN pip install uv
RUN uv sync --no-dev

# Comando para iniciar a aplicação
CMD ["uv", "run", "fastapi", "run", "api/main.py"]
