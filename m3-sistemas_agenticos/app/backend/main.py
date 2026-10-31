"""Punto de entrada de la API de gestión de empleados."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import modelos  # noqa: F401  (registra el modelo en Base.metadata antes de create_all)
from basedatos import Base, engine
from rutas_catalogos import router as router_catalogos
from rutas_empleados import router as router_empleados

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestión de empleados")


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
    mensaje = exc.errors()[0]["msg"]
    prefijo = "Value error, "
    if mensaje.startswith(prefijo):
        mensaje = mensaje[len(prefijo):]
    return JSONResponse(status_code=422, content={"detail": mensaje})


@app.get("/api/salud")
def salud() -> dict[str, str]:
    return {"estado": "ok"}


app.include_router(router_empleados, prefix="/api")
app.include_router(router_catalogos, prefix="/api")
