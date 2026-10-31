"""Rutas de catálogos de la aplicación."""
from fastapi import APIRouter

from constantes import DEPARTAMENTOS

router = APIRouter(tags=["catalogos"])


@router.get("/departamentos")
def listar_departamentos() -> list[str]:
    return DEPARTAMENTOS
