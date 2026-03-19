#importaciones
from fastapi import FastAPI
from  app.routers import usuarios,varios

#instancias(servidor)
app = FastAPI(
    title= "Mi primera API",
    description="Maria Guadalupe Jiménez Ruiz",
    version="1.0"
)

#Router de Endpoints disponibles
app.include_router(usuarios.router)
app.include_router(varios.routerv)



