"""Rutas del recurso /api/empleados."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from basedatos import obtener_sesion
from esquemas import EmpleadoCrear, EmpleadoSalida
from modelos import Empleado

router = APIRouter(prefix="/empleados", tags=["empleados"])


def _siguiente_numero_empleado(sesion: Session) -> str:
    ultimo = sesion.execute(
        select(Empleado).order_by(Empleado.id.desc())
    ).scalars().first()
    if ultimo is None:
        return "EMP-0001"
    consecutivo = int(ultimo.numero_empleado.split("-")[1]) + 1
    return f"EMP-{consecutivo:04d}"


@router.post("", response_model=EmpleadoSalida, status_code=status.HTTP_201_CREATED)
def crear_empleado(datos: EmpleadoCrear, sesion: Session = Depends(obtener_sesion)) -> Empleado:
    ya_existe = sesion.execute(
        select(Empleado).where(func.lower(Empleado.correo) == datos.correo)
    ).scalar_one_or_none()
    if ya_existe is not None:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    empleado = Empleado(
        numero_empleado=_siguiente_numero_empleado(sesion),
        nombre=datos.nombre,
        correo=datos.correo,
        puesto=datos.puesto,
        departamento=datos.departamento,
        fecha_ingreso=datos.fecha_ingreso,
        estado="activo",
    )
    sesion.add(empleado)
    sesion.commit()
    sesion.refresh(empleado)
    return empleado


@router.get("", response_model=list[EmpleadoSalida])
def listar_empleados(
    buscar: str | None = Query(default=None),
    departamento: str | None = Query(default=None),
    sesion: Session = Depends(obtener_sesion),
) -> list[Empleado]:
    consulta = select(Empleado)
    if buscar:
        texto = f"%{buscar.strip().lower()}%"
        consulta = consulta.where(
            func.lower(Empleado.nombre).like(texto) | func.lower(Empleado.correo).like(texto)
        )
    if departamento:
        consulta = consulta.where(Empleado.departamento == departamento)
    consulta = consulta.order_by(Empleado.id)
    return list(sesion.execute(consulta).scalars().all())
