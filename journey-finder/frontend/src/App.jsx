/**
 * Journey Finder App - Componente Principal de la Aplicación
 *
 * Este componente de React sirve como la interfaz principal de la aplicación para buscar y mostrar
 * información de viajes/journeys. Proporciona una interfaz  con las siguientes funcionalidades:
 *
 * - Search Form: Permite a los usuarios ingresar los parámetros de búsqueda para encontrar journeys
 * - Results Display: Muestra los resultados de la búsqueda en formato de tabla
 * - API Integration: Maneja la comunicación con el servicio backend para obtener los datos de journeys
 * - Utiliza React Bootstrap para un diseño adaptable
 *
 * El componente maneja dos estados principales:
 * - results: Array de datos de journeys devueltos por la API
 * - loading: Booleano para mostrar el indicador de carga durante las llamadas a la API
 */

import React, { useState } from "react";
import { Container, Row, Col, Card } from "react-bootstrap";
import SearchForm from "./components/SearchForm";
import ResultsTable from "./components/ResultsTable";
import { searchJourneys } from "./services/api";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (params) => {
    setLoading(true);
    try {
      const response = await searchJourneys(params);
      if (response.data.length === 0) {
        alert("No se encontraron viajes que coincidan con su búsqueda");
      }
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching journeys:", error);
      alert(
        "Ocurrió un error al buscar los viajes. Intente de nuevo más tarde."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="py-4">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="shadow p-4">
            <h2 className="text-center mb-4">🔍 Búsqueda de Viajes</h2>
            <SearchForm onSearch={handleSearch} />
            <hr />
            <ResultsTable results={results} loading={loading} />
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
