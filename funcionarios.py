from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class Funcionario(BaseModel):
    nome: str
    admissao: str
    salario: int

table_funcionario = [
    Funcionario(
        nome = "jose",
        admissao = "a",
        salario = 4000
    ),
    Funcionario(
        nome = "ana",
        admissao = "b",
        salario = 8000
    ),
    Funcionario(
        nome = "bruno",
        admissao = "c",
        salario = 9000
    ),
    Funcionario(
        nome = "silvio",
        admissao = "d",
        salario = 12000
    )
]


@app.get("/funcionarios")
async def get_funcionario():
    return table_funcionario

@app.get("/funcionarios/{salario}")
async def get_maiorsalario(salario: int):

    data = table_funcionario
    listaf = []

    for f in data:
        if f.salario >= salario:
            listaf.append(f)
    return listaf
