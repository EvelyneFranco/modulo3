import { useEffect, useState } from "react";
import DirectorioEmpleados from "./components/DirectorioEmpleados";
import FormularioBaja from "./components/FormularioBaja";
import FormularioEmpleado from "./components/FormularioEmpleado";
import FormularioVacaciones from "./components/FormularioVacaciones";
import { listarEmpleados, obtenerDepartamentos } from "./api/empleados";
import "./App.css";

function App() {
  const [empleados, setEmpleados] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [buscar, setBuscar] = useState("");
  const [departamento, setDepartamento] = useState("");
  const [empleadoEditando, setEmpleadoEditando] = useState(null);
  const [empleadoEnBaja, setEmpleadoEnBaja] = useState(null);
  const [empleadoEnVacaciones, setEmpleadoEnVacaciones] = useState(null);

  useEffect(() => {
    obtenerDepartamentos()
      .then(setDepartamentos)
      .catch(() => setDepartamentos([]));
  }, []);

  useEffect(() => {
    const temporizador = setTimeout(() => {
      listarEmpleados({ buscar, departamento })
        .then(setEmpleados)
        .catch(() => setEmpleados([]));
    }, 300);
    return () => clearTimeout(temporizador);
  }, [buscar, departamento]);

  function manejarEmpleadoCreado(empleado) {
    setEmpleados((anteriores) => [...anteriores, empleado]);
  }

  function reemplazarEnLista(empleadoActualizado) {
    setEmpleados((anteriores) =>
      anteriores.map((empleado) =>
        empleado.id === empleadoActualizado.id ? empleadoActualizado : empleado
      )
    );
  }

  function manejarEmpleadoActualizado(empleadoActualizado) {
    reemplazarEnLista(empleadoActualizado);
  }

  function manejarEmpleadoDadoDeBaja(empleadoActualizado) {
    reemplazarEnLista(empleadoActualizado);
  }

  function manejarEditar(empleado) {
    setEmpleadoEnBaja(null);
    setEmpleadoEditando(empleado);
  }

  function manejarBaja(empleado) {
    setEmpleadoEditando(null);
    setEmpleadoEnBaja(empleado);
  }

  function manejarAbrirVacaciones(empleado) {
    setEmpleadoEditando(null);
    setEmpleadoEnBaja(null);
    setEmpleadoEnVacaciones(empleado);
  }

  return (
    <main>
      <h1>Gestión de empleados</h1>
      <FormularioEmpleado
        empleado={empleadoEditando}
        onEmpleadoCreado={manejarEmpleadoCreado}
        onEmpleadoActualizado={manejarEmpleadoActualizado}
        onCancelar={() => setEmpleadoEditando(null)}
      />
      {empleadoEnBaja && (
        <FormularioBaja
          empleado={empleadoEnBaja}
          onConfirmar={manejarEmpleadoDadoDeBaja}
          onCancelar={() => setEmpleadoEnBaja(null)}
        />
      )}
      {empleadoEnVacaciones && (
        <FormularioVacaciones
          empleado={empleadoEnVacaciones}
          onCancelar={() => setEmpleadoEnVacaciones(null)}
        />
      )}
      <DirectorioEmpleados
        empleados={empleados}
        departamentos={departamentos}
        buscar={buscar}
        onCambiarBuscar={setBuscar}
        departamento={departamento}
        onCambiarDepartamento={setDepartamento}
        onEditar={manejarEditar}
        onBaja={manejarBaja}
        onAbrirVacaciones={manejarAbrirVacaciones}
      />
    </main>
  );
}

export default App;
