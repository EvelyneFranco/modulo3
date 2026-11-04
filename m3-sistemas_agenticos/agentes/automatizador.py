"""Sesión 3 · Agente 5, automatizador: casos de prueba -> pruebas con pytest y Playwright.

Uso:  python -m agentes.automatizador HU-01
"""
import sys

from agentes.base import APP, SALIDA
from agentes.claude_code import EDICION, ejecutar_claude_code

INSTRUCCIONES = """Eres el ingeniero de automatización de pruebas del equipo. Conviertes casos de prueba
en pruebas automatizadas. Nunca modificas el código de la aplicación: si una prueba falla
porque la aplicación está mal, lo reportas, no lo arreglas."""

ESCRITURA = ["tests/*"]
PROGRAMAS = {"cd", "ls", "cat", "python", "python3", "pytest"}

TAREA = """Automatiza los casos de prueba de {hu}:

{casos}

Reglas:
- tests/conftest.py define dos fixtures: `url_api` (variable URL_API, por defecto http://localhost:8000)
  y `url_web` (variable URL_WEB, por defecto http://localhost:8080). Si ya existe, consérvalo.
- Casos de nivel "api": tests/api/test_{hu_min}.py con pytest y httpx.
- Casos de nivel "e2e": tests/e2e/test_{hu_min}_e2e.py con pytest-playwright (fixture `page`),
  usando page.get_by_test_id(...) con los data-testid de CLAUDE.md.
- Un test por caso; su docstring empieza con el id del caso (por ejemplo "CP-03: ...").
- Si ya existen pruebas de {hu}, reescríbelas para que coincidan con los casos de arriba: sus datos
  pueden haber cambiado desde la última vez.
- Es Playwright para Python: los argumentos van en snake_case (has_text=..., no hasText=...).
- Cada test crea sus propios datos con correos únicos (uuid) para poder repetirse sin choques.
- Prepara los datos solo a través de la API. Nunca leas ni escribas la base de datos directamente:
  la app corre en Docker y el archivo no se sincroniza a tiempo. Si conftest.py tiene fixtures que
  tocan la base de datos, reemplázalas por llamadas a la API.
- Si un caso trae identificadores fijos (EMP-0001, id 1), usa los del empleado que creó la prueba.
- Un campo deshabilitado se prueba con expect(...).to_be_disabled(); no intentes escribir en él.
- Lo que la pantalla no permite capturar (una opción que no está en un select) se prueba solo en la API.
- Comprueba la sintaxis con `python -m pytest tests --collect-only -q`. No ejecutes las pruebas completas.
Responde con la lista de archivos y cuántos tests escribiste."""



def automatizar(hu: str, errores: str = "") -> tuple[str, float]:
    """Agente 5: convierte los casos de la historia en pruebas de app/tests; devuelve (respuesta, costo USD)."""
    casos = (SALIDA / hu / "casos_prueba.json").read_text(encoding="utf-8")
    prompt = TAREA.format(hu=hu, casos=casos, hu_min=hu.lower().replace("-", "_"))
    if errores:
        prompt += f"\n\nEstas pruebas fallaron y el diagnóstico dice que el error está en la prueba:\n{errores}"
    return ejecutar_claude_code(prompt, agente="automatizador", cwd=APP, herramientas=EDICION,
                                escritura=ESCRITURA, programas=PROGRAMAS, instrucciones=INSTRUCCIONES)


if __name__ == "__main__":
    print(automatizar(sys.argv[1])[0])
