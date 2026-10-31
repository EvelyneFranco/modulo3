import { useEffect, useState } from "react";
import DirectorioEmpleados from "./components/DirectorioEmpleados";
import FormularioEmpleado from "./components/FormularioEmpleado";
import { listarEmpleados, obtenerDepartamentos } from "./api/empleados";
import "./App.css";

function App() {
  const [empleados, setEmpleados] = useState([]);
  const [departamentos, setDepartamentos] = useState([]);
  const [buscar, setBuscar] = useState("");
  const [departamento, setDepartamento] = useState("");

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

  return (
    <main>
      <h1>Gestión de empleados</h1>
      <FormularioEmpleado onEmpleadoCreado={manejarEmpleadoCreado} />
      <DirectorioEmpleados
        empleados={empleados}
        departamentos={departamentos}
        buscar={buscar}
        onCambiarBuscar={setBuscar}
        departamento={departamento}
        onCambiarDepartamento={setDepartamento}
      />
    </main>
  );
}

export default App;
