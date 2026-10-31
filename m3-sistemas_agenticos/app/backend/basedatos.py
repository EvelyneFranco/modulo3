"""Configuración de la base de datos SQLite con SQLAlchemy 2."""
import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DIR_DATOS = os.path.join(os.path.dirname(__file__), "datos")
os.makedirs(DIR_DATOS, exist_ok=True)
RUTA_BD = os.path.join(DIR_DATOS, "empleados.db")

engine = create_engine(f"sqlite:///{RUTA_BD}", connect_args={"check_same_thread": False})
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def obtener_sesion() -> Generator[Session, None, None]:
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
