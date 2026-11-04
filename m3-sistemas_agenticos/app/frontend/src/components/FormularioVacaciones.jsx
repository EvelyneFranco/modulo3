import { useEffect, useState } from "react";
import { obtenerSaldoVacaciones, solicitarVacaciones } from "../api/empleados";

function FormularioVacaciones({ empleado, onCancelar }) {
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [saldo, setSaldo] = useState(null);
  const [mensaje, setMensaje] = useState("");

  function cargarSaldo(anio) {
    obtenerSaldoVacaciones(empleado.id, anio)
      .then(setSaldo)
      .catch(() => setSaldo(null));
  }

  useEffect(() => {
    cargarSaldo();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [empleado.id]);

  async function manejarEnvio(evento) {
    evento.preventDefault();
    setMensaje("");
    try {
      const resultado = await solicitarVacaciones(empleado.id, {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      });
      const anio = resultado.fecha_inicio.slice(0, 4);
      setMensaje(
        `Solicitud registrada: ${resultado.dias_habiles} días hábiles. Te quedan ${resultado.dias_restantes} días hábiles en ${anio}.`
      );
      cargarSaldo(Number(anio));
    } catch (error) {
      setMensaje(error.message);
    }
  }

  return (
    <form onSubmit={manejarEnvio}>
      <h2>Solicitar vacaciones de {empleado.nombre}</h2>
      {saldo && (
        <p data-testid="vacaciones-disponibles">
          Días disponibles en {saldo.anio}: {saldo.dias_disponibles}
        </p>
      )}
      <div>
        <label htmlFor="vacaciones-fecha-inicio">Fecha de inicio</label>
        <input
          id="vacaciones-fecha-inicio"
          type="date"
          data-testid="vacaciones-fecha-inicio"
          value={fechaInicio}
          onChange={(evento) => setFechaInicio(evento.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="vacaciones-fecha-fin">Fecha de fin</label>
        <input
          id="vacaciones-fecha-fin"
          type="date"
          data-testid="vacaciones-fecha-fin"
          value={fechaFin}
          onChange={(evento) => setFechaFin(evento.target.value)}
          required
        />
      </div>
      <button type="submit" data-testid="vacaciones-enviar">
        Enviar solicitud
      </button>
      <button type="button" onClick={onCancelar}>
        Cancelar
      </button>
      {mensaje && <p data-testid="vacaciones-mensaje">{mensaje}</p>}
    </form>
  );
}

export default FormularioVacaciones;
