#importaciones
from fastapi import FastAPI
import asyncio

#instancias
app = FastAPI()

#endpoints
@app.get("/")
async def bienvenido():
    return {"mensaje": "¡Bienvenido a  FastAPI"}
             
@app.get("/hola mundo")
async def bienvenido():
    await asyncio.sleep(5) #peticion,consultaDB,Archivo
    return {"mensaje": "¡Hola Mundo FastAPI",
          "sataus" :"200" }
             