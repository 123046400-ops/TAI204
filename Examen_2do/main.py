from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Instancia del servidor
app = FastAPI(
    title="Sistema de turnos Bancarios",
    description="Maria Guadalupe Jiménez Ruiz"
)

# MODELOS

class CrearCliente(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=20, example="lupitajr")
    edad: int = Field(..., gt=1, le=100, description="Edad válida entre 1 y 100")

class TipoTramite(BaseModel):
    deposito: int = Field(..., gt=0, description="Cantidad a depositar")
    retiro: int = Field(..., gt=0, description="Cantidad a retirar")
    consulta: Optional[str] = Field(None, description="Consulta del cliente")

# Seguridad con HTTP Basic
security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuarioAut = secrets.compare_digest(credenciales.username, "banco")
    contraAuth = secrets.compare_digest(credenciales.password, "2468")

    if not (usuarioAut and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
            headers={"WWW-Authenticate": "Basic"}
        )

    return credenciales.username


# ENDPOINTS

# Crear turno
@app.post("/v1/usuarios/", tags=["CRUD HTTP"])
async def crear_turno(cliente: CrearCliente, usuario: str = Depends(verificar_peticion)):
    return {
        "mensaje": "Turno creado correctamente",
        "cliente": cliente
    }


# Listar turnos
@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def listar_turnos(usuario: str = Depends(verificar_peticion)):
    return {"mensaje": "Lista de turnos"}


# Consultar turno por ID
@app.get("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def consultar_turno(id: int, usuario: str = Depends(verificar_peticion)):
    return {"mensaje": f"Consulta del turno con ID {id}"}


# Marcar como atendido
@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def atender_turno(id: int, usuario: str = Depends(verificar_peticion)):
    return {"mensaje": f"Turno {id} marcado como atendido"}


# Eliminar turno
@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_turno(id: int, usuario: str = Depends(verificar_peticion)):
    return {"mensaje": f"Turno con ID {id} eliminado exitosamente"}