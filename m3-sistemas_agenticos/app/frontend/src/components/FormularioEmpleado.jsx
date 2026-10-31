import { useEffect, useState } from "react";
import { crearEmpleado, obtenerDepartamentos } from "../api/empleados";

const ESTADO_INICIAL = {
  nombre: "",
  correo: "",
  puesto: "",
  departamento: "",
  fecha_ingreso: "",
};

function FormularioEmpleado({ onEmpleadoCreado }) {
  const [datos, setDatos] = useState(ESTADO_INICIAL);
  const [departamentos, setDepartamentos] = useState([]);
  const [mensajeExito, setMensajeExito] = useState("");
  const [mensajeError, setMensajeError] = useState("");

  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => setDepartamentos([]));
  }, []);

  function manejarCambio(evento) {
    const { name, value } = evento.target;
    setDatos((anterior) => ({ ...anterior, [name]: value }));
  }

  async function manejarEnvio(evento) {
    evento.preventDefault();
    setMensajeExito("");
    setMensajeError("");
    try {
      const empleado = await crearEmpleado(datos);
      setMensajeExito(`Empleado ${empleado.numero_empleado} registrado con éxito`);
      setDatos(ESTADO_INICIAL);
      onEmpleadoCreado(empleado);
    } catch (error) {
      setMensajeError(error.message);
    }
  }

  return (
    <form onSubmit={manejarEnvio}>
      <h2>Registrar empleado</h2>
      <div>
        <label htmlFor="nombre">Nombre</label>
        <input
          id="nombre"
          name="nombre"
          data-testid="empleado-nombre"
          value={datos.nombre}
          onChange={manejarCambio}
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
          required
        />
      </div>
      <button type="submit" data-testid="empleado-guardar">
        Guardar
      </button>
      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  );
}

export default FormularioEmpleado;
