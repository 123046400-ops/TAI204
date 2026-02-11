#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional 

#instancias
app = FastAPI(
    title= "Mi primera API",
    description="Maria Guadalupe Jiménez Ruiz",
    version="1.0"
)


#tabla ficticia
usuarios=[
    {"id":1,"nombre":"Diego","edad":21},
    {"id":2,"nombre":"Coral","edad":21},
    {"id":3,"nombre":"Saul","edad":21},
]

#endpoints
@app.get("/",tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "¡Bienvenido a  FastAPI"}
             
@app.get("/hola mundo",tags=['Asincronia'])
async def bienvenido():
    await asyncio.sleep(5) #peticion,consultaDB,Archivo
    return {"mensaje": "¡Hola Mundo FastAPI",
          "sataus" :"200" }

@app.get("/v1/usuario/{id}",tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje": "usuario encontrado",
            "usuario":id,
             "status":"200" }

@app.get("/v1/usuarios/",tags=['Parametro Opcional'])
async def consultatodos(id:Optional[int]=None):
    if id is not None:
         for usuarioK in usuarios:
             if usuarioK["id"] == id:
                 return{"mensaje":"usuario encontrado","usuario":usuarioK}
         return{"mensaje":"usuario no encontrado","status":"200"}  
    else:
        return{"mensaje":"No se proporciono id","status":"200"}   