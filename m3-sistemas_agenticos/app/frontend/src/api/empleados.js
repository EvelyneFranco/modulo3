const URL_BASE = "/api";

export async function obtenerDepartamentos() {
  const respuesta = await fetch(`${URL_BASE}/departamentos`);
  if (!respuesta.ok) {
    throw new Error("No se pudieron cargar los departamentos");
  }
  return respuesta.json();
}

export async function listarEmpleados(filtros = {}) {
  const parametros = new URLSearchParams();
  if (filtros.buscar) {
    parametros.set("buscar", filtros.buscar);
  }
  if (filtros.departamento) {
    parametros.set("departamento", filtros.departamento);
  }
  const cadena = parametros.toString();
  const respuesta = await fetch(`${URL_BASE}/empleados${cadena ? `?${cadena}` : ""}`);
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

export async function actualizarEmpleado(id, datos) {
  const respuesta = await fetch(`${URL_BASE}/empleados/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "No se pudo actualizar el empleado");
  }
  return cuerpo;
}

export async function darDeBaja(id, fechaBaja) {
  const respuesta = await fetch(`${URL_BASE}/empleados/${id}/baja`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fecha_baja: fechaBaja }),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "No se pudo dar de baja al empleado");
  }
  return cuerpo;
}

export async function solicitarVacaciones(empleadoId, datos) {
  const respuesta = await fetch(`${URL_BASE}/empleados/${empleadoId}/vacaciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos),
  });
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "No se pudo registrar la solicitud de vacaciones");
  }
  return cuerpo;
}

export async function obtenerSaldoVacaciones(empleadoId, anio) {
  const parametros = anio ? `?anio=${anio}` : "";
  const respuesta = await fetch(`${URL_BASE}/empleados/${empleadoId}/vacaciones${parametros}`);
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(cuerpo.detail || "No se pudo consultar el saldo de vacaciones");
  }
  return cuerpo;
}
