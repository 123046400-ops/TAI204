from fastapi import status,HTTPException,Depends,APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

router= APIRouter(
    prefix="/v1/usuarios",tags=['CRUD HTTP']
)

@router.get("/")
async def consultaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@router.post("/")
async def crear_usuario(usuario: crear_usuario):
    for usr in usuarios:
         if usr["id"] == usuario.id:
                raise HTTPException(
                    status_code=400,
                    detail="El id ya existe"
                )
    usuarios.append(usuario) 
    return{
     "mensaje": "Usuario agregado",
     "usuario": usuario,
       "status": "200"
  }   

@router.put("/{id}")
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


@router.delete("/{id}")
async def eliminar_usuario(id: int,usuarioAuth:str = Depends(verificar_peticion)):  
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "usuario": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

    
