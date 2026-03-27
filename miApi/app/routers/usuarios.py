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

@router.get("/{id}",status_code=status.HTTP_200_OK)
async def consultaId(id: int,db: Session= Depends(get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not queryUsuario:
        raise HTTPException(
            status_code=404,
            detail= "Usuario no encontrado"
        )
    return{
        "usuarios": queryUsuario
    }


@router.post("/",status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: crear_usuario,db: Session= Depends(get_db)):
    usuarioNuevo= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad) 
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    

    return{
     "mensaje": "Usuario agregado",
     "usuario": usuarioP,
       
  }   

@router.put("/{id}")
async def actualizarUsuario(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = usuarioP.nombre
    usuario.edad = usuarioP.edad
    db.commit()
    db.refresh(usuario)

    return {
        "status": "200",
        "mensaje": "Usuario actualizado",
        "usuario": usuario
    }


@router.patch("/{id}",status_code=status.HTTP_200_OK)
async def actualizarParcial(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not queryUsuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuarioP.nombre:
        queryUsuario.nombre = usuarioP.nombre
    if usuarioP.edad:
        queryUsuario.edad = usuarioP.edad
    db.commit()
    db.refresh(queryUsuario)

    return {
        "mensaje": "Usuario actualizado parcialmente",
        "usuario": queryUsuario
    }

@router.delete("/{id}",status_code=status.HTTP_200_OK)
async def eliminarUsuario(id: int, usuarioAuth: str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    queryUsuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not queryUsuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(queryUsuario)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
    }




    
