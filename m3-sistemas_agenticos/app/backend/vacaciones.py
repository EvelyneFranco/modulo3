"""Reglas de negocio de vacaciones (HU-10)."""
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelos import Vacacion

ANIOS_VALIDOS = {2026, 2027}
DIAS_POR_ANIO = 12

FESTIVOS: dict[int, set[date]] = {
    2026: {
        date(2026, 1, 1),
        date(2026, 2, 2),
        date(2026, 3, 16),
        date(2026, 5, 1),
        date(2026, 9, 16),
        date(2026, 11, 16),
        date(2026, 12, 25),
    },
    2027: {
        date(2027, 1, 1),
        date(2027, 2, 1),
        date(2027, 3, 15),
        date(2027, 5, 1),
        date(2027, 9, 16),
        date(2027, 11, 15),
        date(2027, 12, 25),
    },
}


class ErrorVacacion(Exception):
    """Error de negocio con el código HTTP y el mensaje exacto que debe mostrarse."""

    def __init__(self, codigo: int, detail: str) -> None:
        super().__init__(detail)
        self.codigo = codigo
        self.detail = detail


def es_festivo(fecha: date) -> bool:
    return fecha in FESTIVOS.get(fecha.year, set())


def dias_habiles_en(inicio: date, fin: date) -> int:
    dias = 0
    actual = inicio
    while actual <= fin:
        if actual.weekday() < 5 and not es_festivo(actual):
            dias += 1
        actual += timedelta(days=1)
    return dias


def cumple_antiguedad(fecha_ingreso: date, fecha_inicio: date) -> bool:
    try:
        aniversario = fecha_ingreso.replace(year=fecha_ingreso.year + 1)
    except ValueError:
        # 29 de febrero: en un año no bisiesto el aniversario cae el 1 de marzo.
        aniversario = date(fecha_ingreso.year + 1, 3, 1)
    return fecha_inicio >= aniversario


def dias_usados_en_anio(sesion: Session, empleado_id: int, anio: int) -> int:
    solicitudes = sesion.execute(
        select(Vacacion).where(
            Vacacion.empleado_id == empleado_id,
            Vacacion.fecha_inicio >= date(anio, 1, 1),
            Vacacion.fecha_inicio <= date(anio, 12, 31),
        )
    ).scalars().all()
    return sum(solicitud.dias_habiles for solicitud in solicitudes)


def validar_y_calcular_dias(
    sesion: Session, empleado, fecha_inicio: date, fecha_fin: date
) -> int:
    """Aplica las reglas de negocio en orden y regresa los días hábiles de la solicitud."""
    if empleado.estado == "baja":
        raise ErrorVacacion(
            409, "No se pueden solicitar vacaciones para un empleado dado de baja"
        )
    if fecha_fin < fecha_inicio:
        raise ErrorVacacion(400, "La fecha de fin no puede ser anterior a la fecha de inicio")
    if fecha_inicio.year != fecha_fin.year:
        raise ErrorVacacion(400, "Las vacaciones deben estar dentro de un mismo año calendario")
    if fecha_inicio.year not in ANIOS_VALIDOS:
        raise ErrorVacacion(400, "Solo se pueden solicitar vacaciones en 2026 y 2027")
    if not cumple_antiguedad(empleado.fecha_ingreso, fecha_inicio):
        raise ErrorVacacion(
            400, "Se requiere al menos un año de antigüedad a la fecha de inicio"
        )
    dias = dias_habiles_en(fecha_inicio, fecha_fin)
    if dias == 0:
        raise ErrorVacacion(400, "El periodo no incluye días hábiles")
    usados = dias_usados_en_anio(sesion, empleado.id, fecha_inicio.year)
    disponibles = DIAS_POR_ANIO - usados
    if dias > disponibles:
        raise ErrorVacacion(
            400,
            f"La solicitud excede los días disponibles: quedan {disponibles} días hábiles",
        )
    return dias
