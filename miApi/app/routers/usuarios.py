from fastapi import status,HTTPException,Depends,APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router= APIRouter(
    prefix="/v1/usuarios",tags=['CRUD HTTP']
)

@router.get("/")
async def consultaT(db: Session= Depends(get_db)):

    queryUsuario= db.query(usuarioDB).all()
    return{
        "status": "200",
        "total": len(queryUsuario),
        "usuarios": queryUsuario
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP: crear_usuario,db: Session= Depends(get_db)):
    usuarioNuevo= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad) 
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    

    return{
     "mensaje": "Usuario agregado",
     "usuario": usuarioP,
       
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

    
