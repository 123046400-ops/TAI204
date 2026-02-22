#importaciones
from fastapi import FastAPI,status,HTTPException
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

@app.get("/v1/ParametroOb/{id}",tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje": "usuario encontrado",
            "usuario":id,
             "status":"200" }

@app.get("/v1/ParametroOp/",tags=['Parametro Opcional'])
async def consultatodos(id:Optional[int]=None):
    if id is not None:
         for usuarioK in usuarios:
             if usuarioK["id"] == id:
                 return{"mensaje":"usuario encontrado","usuario":usuarioK}
         return{"mensaje":"usuario no encontrado","status":"200"}  
    else:
        return{"mensaje":"No se proporciono id","status":"200"}   
    
@app.get("/v1/usuarios/{id}",tags=['CRUD HTTP'])
async def consultaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/{id}",tags=['CRUD HTTP'])
async def agregar_usuario(usuario:dict): #recibe un diccionario con los datos del nuevo usuario
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code= 400,
                detail="El ID ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "Usuario agregado",
        "usuario": usuario,
        "status": "200"
    }        

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict):  
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre")
            usr["edad"] = usuario.get("edad")
            
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):  
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado",
                "usuario": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

