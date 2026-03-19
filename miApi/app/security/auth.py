#Seguridad con HTTP Basic (practica6)
from fastapi import status,HTTPException,Depends 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
    
security= HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuarioAut = secrets.compare_digest(credenciales.username, "Lupita")
    contraAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (usuarioAut and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
        )

    return credenciales.username
    
