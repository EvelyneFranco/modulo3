const URL_BASE = "/api";

export async function obtenerDepartamentos() {
  const respuesta = await fetch(`${URL_BASE}/departamentos`);
  if (!respuesta.ok) {
    throw new Error("No se pudieron cargar los departamentos");
  }
  return respuesta.json();
}

export async function listarEmpleados() {
  const respuesta = await fetch(`${URL_BASE}/empleados`);
  if (!respuesta.ok) {
    throw new Error("No se pudo cargar el directorio de empleados");
  }
  return respuesta.json();
}

export async function crearEmpleado(datos) {
  const respuesta = await fetch(`${URL_BASE}/empleados`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "No se pudo registrar el empleado");
  }
  return cuerpo;
}
