import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

routerv=APIRouter (tags=['Inicio'])
#endpoints
@routerv.get("/")
async def bienvenido():
    return {"mensaje": "¡Bienvenido a  FastAPI"}
             
@routerv.get("/hola mundo")
async def bienvenido():
    await asyncio.sleep(5) #peticion,consultaDB,Archivo
    return {"mensaje": "¡Hola Mundo FastAPI",
          "sataus" :"200" }

@routerv.get("/v1/ParametroOb/{id}")
async def consultauno(id:int):
    return {"mensaje": "usuario encontrado",
            "usuario":id,
             "status":"200" }

@routerv.get("/v1/ParametroOp/")
async def consultatodos(id:Optional[int]=None):
    if id is not None:
         for usuarioK in usuarios:
             if usuarioK["id"] == id:
                 return{"mensaje":"usuario encontrado","usuario":usuarioK}
         return{"mensaje":"usuario no encontrado","status":"200"}  
    else:
        return{"mensaje":"No se proporciono id","status":"200"}   
    
