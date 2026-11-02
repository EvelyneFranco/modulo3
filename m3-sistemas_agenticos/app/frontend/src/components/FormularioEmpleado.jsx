import { useEffect, useState } from "react";
import { actualizarEmpleado, crearEmpleado, obtenerDepartamentos } from "../api/empleados";

const ESTADO_INICIAL = {
  nombre: "",
  correo: "",
  puesto: "",
  departamento: "",
  fecha_ingreso: "",
};

function FormularioEmpleado({ empleado, onEmpleadoCreado, onEmpleadoActualizado, onCancelar }) {
  const [datos, setDatos] = useState(ESTADO_INICIAL);
  const [departamentos, setDepartamentos] = useState([]);
  const [mensajeExito, setMensajeExito] = useState("");
  const [mensajeError, setMensajeError] = useState("");
  const editando = Boolean(empleado);

  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => setDepartamentos([]));
  }, []);

  useEffect(() => {
    setMensajeExito("");
    setMensajeError("");
    setDatos(
      empleado
        ? {
            nombre: empleado.nombre,
            correo: empleado.correo,
            puesto: empleado.puesto,
            departamento: empleado.departamento,
            fecha_ingreso: empleado.fecha_ingreso,
          }
        : ESTADO_INICIAL
    );
  }, [empleado]);

  function manejarCambio(evento) {
    const { name, value } = evento.target;
    setDatos((anterior) => ({ ...anterior, [name]: value }));
  }

  async function manejarEnvio(evento) {
    evento.preventDefault();
    setMensajeExito("");
    setMensajeError("");
    try {
      if (editando) {
        const actualizado = await actualizarEmpleado(empleado.id, {
          puesto: datos.puesto,
          departamento: datos.departamento,
        });
        setMensajeExito(`Empleado ${actualizado.numero_empleado} actualizado con éxito`);
        onEmpleadoActualizado(actualizado);
      } else {
        const creado = await crearEmpleado(datos);
        setMensajeExito(`Empleado ${creado.numero_empleado} registrado con éxito`);
        setDatos(ESTADO_INICIAL);
        onEmpleadoCreado(creado);
      }
    } catch (error) {
      setMensajeError(error.message);
    }
  }

  return (
    <form onSubmit={manejarEnvio}>
      <h2>{editando ? "Editar empleado" : "Registrar empleado"}</h2>
      <div>
        <label htmlFor="nombre">Nombre</label>
        <input
          id="nombre"
          name="nombre"
          data-testid="empleado-nombre"
          value={datos.nombre}
          onChange={manejarCambio}
          disabled={editando}
          required
        />
      </div>
      <div>
        <label htmlFor="correo">Correo</label>
        <input
          id="correo"
          name="correo"
          type="email"
          data-testid="empleado-correo"
          value={datos.correo}
          onChange={manejarCambio}
          disabled={editando}
          required
        />
      </div>
      <div>
        <label htmlFor="puesto">Puesto</label>
        <input
          id="puesto"
          name="puesto"
          data-testid="empleado-puesto"
          value={datos.puesto}
          onChange={manejarCambio}
          required
        />
      </div>
      <div>
        <label htmlFor="departamento">Departamento</label>
        <select
          id="departamento"
          name="departamento"
          data-testid="empleado-departamento"
          value={datos.departamento}
          onChange={manejarCambio}
          required
        >
          <option value="">Selecciona un departamento</option>
          {departamentos.map((departamento) => (
            <option key={departamento} value={departamento}>
              {departamento}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="fecha-ingreso">Fecha de ingreso</label>
        <input
          id="fecha-ingreso"
          name="fecha_ingreso"
          type="date"
          data-testid="empleado-fecha-ingreso"
          value={datos.fecha_ingreso}
          onChange={manejarCambio}
          disabled={editando}
          required
        />
      </div>
      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>
      {editando && (
        <button type="button" onClick={onCancelar}>
          Cancelar
        </button>
      )}
      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  );
}

export default FormularioEmpleado;
