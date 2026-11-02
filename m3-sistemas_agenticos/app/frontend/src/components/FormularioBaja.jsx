import { useState } from "react";
import { darDeBaja } from "../api/empleados";

function FormularioBaja({ empleado, onConfirmar, onCancelar }) {
  const [fechaBaja, setFechaBaja] = useState("");
  const [mensajeExito, setMensajeExito] = useState("");
  const [mensajeError, setMensajeError] = useState("");

  async function manejarConfirmar(evento) {
    evento.preventDefault();
    setMensajeExito("");
    setMensajeError("");
    try {
      const actualizado = await darDeBaja(empleado.id, fechaBaja);
      setMensajeExito(`Empleado ${actualizado.numero_empleado} dado de baja con éxito`);
      onConfirmar(actualizado);
    } catch (error) {
      setMensajeError(error.message);
    }
  }

  return (
    <form onSubmit={manejarConfirmar}>
      <h2>Dar de baja a {empleado.nombre}</h2>
      <div>
        <label htmlFor="fecha-baja">Fecha de baja</label>
        <input
          id="fecha-baja"
          type="date"
          data-testid="empleado-fecha-baja"
          value={fechaBaja}
          onChange={(evento) => setFechaBaja(evento.target.value)}
          required
        />
      </div>
      <button type="submit" data-testid="confirmar-baja">
        Confirmar baja
      </button>
      <button type="button" onClick={onCancelar}>
        Cancelar
      </button>
      {mensajeExito && <p data-testid="mensaje-exito">{mensajeExito}</p>}
      {mensajeError && <p data-testid="mensaje-error">{mensajeError}</p>}
    </form>
  );
}

export default FormularioBaja;
