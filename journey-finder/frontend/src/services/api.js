/**
 * API Service - Journey Search API Integration
 *
 * Handles communication with the backend API for journey search functionality.
 * Provides a function to search for journeys by sending GET requests to the
 * backend service with search parameters (origin, destination, date).
 */
import axios from "axios";

const API_URL = "http://localhost:8000/journeys/search";

export const searchJourneys = (params) => {
  return axios.get(API_URL, { params });
};
