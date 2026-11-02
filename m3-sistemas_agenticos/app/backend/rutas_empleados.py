"""Rutas del recurso /api/empleados."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from basedatos import obtener_sesion
from errores import primer_mensaje
from esquemas import BajaEmpleado, EmpleadoActualizar, EmpleadoCrear, EmpleadoSalida
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


def _obtener_o_404(id: int, sesion: Session) -> Empleado:
    empleado = sesion.get(Empleado, id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="El empleado no existe")
    return empleado


@router.get("/{id}", response_model=EmpleadoSalida)
def obtener_empleado(id: int, sesion: Session = Depends(obtener_sesion)) -> Empleado:
    return _obtener_o_404(id, sesion)


@router.put("/{id}", response_model=EmpleadoSalida)
async def actualizar_empleado(
    id: int, solicitud: Request, sesion: Session = Depends(obtener_sesion)
) -> Empleado:
    empleado = _obtener_o_404(id, sesion)
    if empleado.estado == "baja":
        raise HTTPException(
            status_code=409, detail="No se puede editar a un empleado dado de baja"
        )

    cuerpo = await solicitud.json()
    if "numero_empleado" in cuerpo or "correo" in cuerpo:
        raise HTTPException(
            status_code=422,
            detail="Los campos numero_empleado y correo no se pueden editar",
        )
    try:
        datos = EmpleadoActualizar.model_validate(cuerpo)
    except ValidationError as error:
        raise HTTPException(status_code=422, detail=primer_mensaje(error)) from error

    if datos.puesto is not None:
        empleado.puesto = datos.puesto
    if datos.departamento is not None:
        empleado.departamento = datos.departamento
    sesion.commit()
    sesion.refresh(empleado)
    return empleado


@router.post("/{id}/baja", response_model=EmpleadoSalida)
def dar_de_baja(
    id: int, datos: BajaEmpleado, sesion: Session = Depends(obtener_sesion)
) -> Empleado:
    empleado = _obtener_o_404(id, sesion)
    if empleado.estado == "baja":
        raise HTTPException(status_code=409, detail="El empleado ya está dado de baja")
    if datos.fecha_baja < empleado.fecha_ingreso:
        raise HTTPException(
            status_code=422,
            detail="La fecha de baja no puede ser anterior a la fecha de ingreso",
        )
    empleado.estado = "baja"
    empleado.fecha_baja = datos.fecha_baja
    sesion.commit()
    sesion.refresh(empleado)
    return empleado
