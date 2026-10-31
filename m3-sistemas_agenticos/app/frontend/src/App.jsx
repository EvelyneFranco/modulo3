import { useEffect, useState } from "react";
import DirectorioEmpleados from "./components/DirectorioEmpleados";
import FormularioEmpleado from "./components/FormularioEmpleado";
import { listarEmpleados } from "./api/empleados";
import "./App.css";

function App() {
  const [empleados, setEmpleados] = useState([]);

  useEffect(() => {
    listarEmpleados()
      .then(setEmpleados)
      .catch(() => setEmpleados([]));
  }, []);

  function manejarEmpleadoCreado(empleado) {
    setEmpleados((anteriores) => [...anteriores, empleado]);
  }

  return (
    <main>
      <h1>Gestión de empleados</h1>
      <FormularioEmpleado onEmpleadoCreado={manejarEmpleadoCreado} />
      <DirectorioEmpleados empleados={empleados} />
    </main>
  );
}

export default App;
