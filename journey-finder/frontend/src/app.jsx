/**
 * Journey Finder App - Main Application Component
 *
 * This React component serves as the main application interface for searching and displaying
 * journey/travel information. It provides a user-friendly interface with the following features:
 *
 * - Search Form: Allows users to input search parameters for finding journeys
 * - Results Display: Shows search results in a table format with loading states
 * - API Integration: Handles communication with the backend service to fetch journey data
 * - Responsive Design: Uses React Bootstrap for mobile-friendly layout
 *
 * The component manages two main pieces of state:
 * - results: Array of journey data returned from the API
 * - loading: Boolean flag to show loading indicator during API calls
 *
 * When a search is performed, it calls the searchJourneys API service and updates the
 * results state with the returned data, handling errors.
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
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching journeys:", error);
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
