"""Rutas del recurso /api/empleados/{id}/vacaciones."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from basedatos import obtener_sesion
from esquemas import SaldoVacaciones, SolicitudVacacion, VacacionRespuesta
from modelos import Empleado, Vacacion
from vacaciones import DIAS_POR_ANIO, ErrorVacacion, dias_usados_en_anio, validar_y_calcular_dias

router = APIRouter(prefix="/empleados", tags=["vacaciones"])


def _obtener_empleado_o_404(id: int, sesion: Session) -> Empleado:
    empleado = sesion.get(Empleado, id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.post("/{id}/vacaciones", response_model=VacacionRespuesta, status_code=201)
def solicitar_vacaciones(
    id: int, datos: SolicitudVacacion, sesion: Session = Depends(obtener_sesion)
) -> VacacionRespuesta:
    empleado = _obtener_empleado_o_404(id, sesion)
    try:
        dias = validar_y_calcular_dias(sesion, empleado, datos.fecha_inicio, datos.fecha_fin)
    except ErrorVacacion as error:
        raise HTTPException(status_code=error.codigo, detail=error.detail) from error

    vacacion = Vacacion(
        empleado_id=empleado.id,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        dias_habiles=dias,
    )
    sesion.add(vacacion)
    sesion.commit()
    sesion.refresh(vacacion)

    usados = dias_usados_en_anio(sesion, empleado.id, datos.fecha_inicio.year)
    return VacacionRespuesta(
        id=vacacion.id,
        empleado_id=vacacion.empleado_id,
        fecha_inicio=vacacion.fecha_inicio,
        fecha_fin=vacacion.fecha_fin,
        dias_habiles=vacacion.dias_habiles,
        dias_restantes=DIAS_POR_ANIO - usados,
    )


@router.get("/{id}/vacaciones", response_model=SaldoVacaciones)
def consultar_saldo(
    id: int,
    anio: int | None = Query(default=None),
    sesion: Session = Depends(obtener_sesion),
) -> SaldoVacaciones:
    empleado = _obtener_empleado_o_404(id, sesion)
    anio_consulta = anio or date.today().year

    solicitudes = sesion.execute(
        select(Vacacion)
        .where(
            Vacacion.empleado_id == empleado.id,
            Vacacion.fecha_inicio >= date(anio_consulta, 1, 1),
            Vacacion.fecha_inicio <= date(anio_consulta, 12, 31),
        )
        .order_by(Vacacion.fecha_inicio)
    ).scalars().all()

    dias_usados = sum(solicitud.dias_habiles for solicitud in solicitudes)
    return SaldoVacaciones(
        empleado_id=empleado.id,
        anio=anio_consulta,
        dias_usados=dias_usados,
        dias_disponibles=DIAS_POR_ANIO - dias_usados,
        solicitudes=solicitudes,
    )
