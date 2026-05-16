from fastapi import FastAPI
app = FastAPI()

@app.get("/teste")
def hello_world():
    return {"mensagem": " Hello World"}

@app.get("/soma/{numero1}/{numero2}")
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}