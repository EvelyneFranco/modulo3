"""Esquemas Pydantic del recurso de empleados."""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

from constantes import DEPARTAMENTOS, DOMINIO_CORREO


class EmpleadoCrear(BaseModel):
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, valor: str) -> str:
        valor = valor.strip()
        if not (2 <= len(valor) <= 80):
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres")
        return valor

    @field_validator("puesto")
    @classmethod
    def validar_puesto(cls, valor: str) -> str:
        valor = valor.strip()
        if not (2 <= len(valor) <= 60):
            raise ValueError("El puesto debe tener entre 2 y 60 caracteres")
        return valor

    @field_validator("departamento")
    @classmethod
    def validar_departamento(cls, valor: str) -> str:
        if valor not in DEPARTAMENTOS:
            raise ValueError("El departamento debe ser uno del catálogo válido")
        return valor

    @field_validator("correo")
    @classmethod
    def validar_correo(cls, valor: str) -> str:
        valor = valor.strip().lower()
        if not valor.endswith(DOMINIO_CORREO):
            raise ValueError("Usa el correo corporativo @empresa.com")
        return valor

    @field_validator("fecha_ingreso")
    @classmethod
    def validar_fecha_ingreso(cls, valor: date) -> date:
        if valor > date.today():
            raise ValueError("La fecha de ingreso no puede ser futura")
        return valor


class EmpleadoActualizar(BaseModel):
    puesto: str | None = None
    departamento: str | None = None

    @field_validator("puesto")
    @classmethod
    def validar_puesto(cls, valor: str | None) -> str | None:
        if valor is None:
            return valor
        valor = valor.strip()
        if not (2 <= len(valor) <= 60):
            raise ValueError("El puesto debe tener entre 2 y 60 caracteres")
        return valor

    @field_validator("departamento")
    @classmethod
    def validar_departamento(cls, valor: str | None) -> str | None:
        if valor is None:
            return valor
        if valor not in DEPARTAMENTOS:
            raise ValueError("El departamento debe ser uno del catálogo válido")
        return valor


class BajaEmpleado(BaseModel):
    fecha_baja: date


class EmpleadoSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_empleado: str
    nombre: str
    correo: str
    puesto: str
    departamento: str
    fecha_ingreso: date
    estado: str
    fecha_baja: date | None
    creado_en: datetime


class SolicitudVacacion(BaseModel):
    fecha_inicio: date
    fecha_fin: date


class VacacionRespuesta(BaseModel):
    id: int
    empleado_id: int
    fecha_inicio: date
    fecha_fin: date
    dias_habiles: int
    dias_restantes: int


class SolicitudResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_inicio: date
    fecha_fin: date
    dias_habiles: int


class SaldoVacaciones(BaseModel):
    empleado_id: int
    anio: int
    dias_usados: int
    dias_disponibles: int
    solicitudes: list[SolicitudResumen]
