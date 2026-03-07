#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets

#instancias(servidor)
app = FastAPI(
    title="Mi primera API",
    description="Maria Guadalupe Jiménez Ruiz",
    version="2.0 - JWT"
)

#modelos de validacion de pydantic
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanito Doe")
    edad: int = Field(..., gt=1, le=125, description="Edad valida entre 1 y 125")

#Configuración OAuth2 
SECRET_KEY = "clave-secreta-super-segura-miApiJWT-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Usuario de prueba 
USUARIO_FAKE = {
    "username": "Lupita",
    "password": "123456"
}

# Generación de token JWT
def crear_token(data: dict) -> str:
    payload = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Validación de token JWT
def verificar_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Endpoint de login – genera el token
@app.post("/token", tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario_ok  = secrets.compare_digest(form_data.username, USUARIO_FAKE["username"])
    password_ok = secrets.compare_digest(form_data.password, USUARIO_FAKE["password"])

    if not (usuario_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = crear_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

#tabla ficticia
usuarios = [
    {"id": 1, "nombre": "Diego", "edad": 21},
    {"id": 2, "nombre": "Coral", "edad": 21},
    {"id": 3, "nombre": "Saul",  "edad": 21},
]

#endpoints
@app.get("/", tags=["Inicio"])
async def bienvenido():
    return {"mensaje": "¡Bienvenido a FastAPI"}

@app.get("/hola mundo", tags=["Asincronia"])
async def hola_mundo():
    await asyncio.sleep(5)
    return {"mensaje": "¡Hola Mundo FastAPI", "status": "200"}

@app.get("/v1/ParametroOb/{id}", tags=["Parametro Obligatorio"])
async def consultauno(id: int):
    return {"mensaje": "usuario encontrado", "usuario": id, "status": "200"}

@app.get("/v1/ParametroOp/", tags=["Parametro Opcional"])
async def consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK}
        return {"mensaje": "usuario no encontrado", "status": "200"}
    else:
        return {"mensaje": "No se proporciono id", "status": "200"}

@app.get("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario.dict())
    return {
        "mensaje": "Usuario agregado",
        "usuario": usuario,
        "status": "200"
    }

# Endpoints protegidos con JWT
@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(
    id: int,
    usuario: dict,
    usuario_auth: str = Depends(verificar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre")
            usr["edad"]   = usuario.get("edad")
            return {
                "mensaje": f"Usuario actualizado por {usuario_auth}",
                "usuario": usr,
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(
    id: int,
    usuario_auth: str = Depends(verificar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {usuario_auth}",
                "usuario": usr,
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")