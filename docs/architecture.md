# System Architecture

Insight API is a sales analytics application that separates data processing, data access, analytical logic, API endpoints, and user interface components. It uses FastAPI to expose sales insights through HTTP endpoints and Streamlit to present those insights in an interactive dashboard.

The application is containerised with Docker and deployed to Google Cloud Run. GitHub Actions automates testing, container image building, and deployment.

## Architecture Overview

### 1. Application Data Flow

```text
Raw Sales Data (CSV)
        |
        v
Data Processing Pipeline
  - Validate required columns
  - Check numeric fields
  - Check for missing values
  - Transform dates
  - Derive monthly reporting fields
        |
        v
Processed Sales Data (Parquet)
        |
        v
Data Loader
        |
        v
Analytics Services
        |
        v
FastAPI Endpoints
        |
        v
JSON Responses
        |
        v
Streamlit Dashboard
        |
        v
Metrics, Charts, and Tables
```

### 2. Deployment Architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +--> Install dependencies
    +--> Run automated tests
    +--> Build Docker image
    +--> Validate Docker Compose
    +--> Start containers and check services
    |
    v
Deployment Job (main branch only)
    |
    v
Authenticate to Google Cloud
using Workload Identity Federation
    |
    v
Build and Push Docker Image
    |
    v
Google Artifact Registry
    |
    +--------------------------+
    |                          |
    v                          v
Cloud Run API Service    Cloud Run Dashboard Service
    |                          |
    v                          v
FastAPI Endpoints          Streamlit Interface
    |                          |
    +------ HTTP Requests -----+
```

The API and dashboard run as separate Cloud Run services using the same application image with different startup commands and port configurations. The dashboard communicates with the API through its deployed URL.

## Main Components

### 1. Data Processing

**File:** `src/insight_api/processing.py`

Loads raw sales data from CSV, validates the input, transforms relevant fields, derives monthly reporting information, and saves the processed dataset in Parquet format.

This separates data preparation from the analytical functions that consume the processed data.

### 2. Data Access

**File:** `src/insight_api/data_access/loader.py`

Loads the processed Parquet dataset into a Pandas DataFrame for analysis. It provides a dedicated access point for retrieving the data and raises an error if the expected file cannot be found.

### 3. Analytics Services

**File:** `src/insight_api/services/analysis.py`

Contains reusable business logic for calculating sales metrics and aggregations, including:

- Total revenue and units sold
- Average revenue per record and per unit
- Revenue and units sold by product
- Revenue and units sold by region
- Monthly sales performance
- Top-performing product

Keeping analytical calculations separate from the API layer makes the business logic easier to test and maintain.

### 4. API Layer

**Files:** `src/insight_api/main.py` and `src/insight_api/api/routes.py`

FastAPI provides HTTP endpoints for accessing the analytical results. The endpoints call the relevant analytics services and return responses in JSON format.

The API also exposes a health endpoint for basic service availability checks and automatically generates interactive API documentation.

### 5. Frontend

**File:** `streamlit_app.py`

The Streamlit application requests analytical data from the FastAPI service and displays it through interactive metrics, charts, and tables.

The dashboard communicates with the API using the `API_BASE_URL` environment variable. This allows the API address to differ between local development and cloud deployment.

### 6. Containerisation

**Files:** `Dockerfile` and `compose.yaml`

Docker packages the application and its dependencies into a reproducible container image.

Docker Compose defines the local application services and allows the API and dashboard to run as separate containers. Each service can have its own startup command, network configuration, and exposed port.

### 7. Continuous Integration and Continuous Deployment

**File:** `.github/workflows/ci.yaml`

GitHub Actions automates the project's testing and deployment workflow.

The CI job runs on pushes and pull requests. It installs dependencies, runs automated tests, builds the Docker image, validates the Docker Compose configuration, starts the local services, and checks that the API and dashboard respond.

The deployment job runs only after the CI job succeeds and only for pushes to the `main` branch. It authenticates to Google Cloud using Workload Identity Federation, builds and pushes a commit-specific Docker image, and deploys the API and dashboard to Cloud Run.

### 8. Cloud Infrastructure

**Services:** Google Artifact Registry and Google Cloud Run

- **Artifact Registry:** Stores the versioned Docker images used for deployment.
- **Cloud Run API service:** Runs the FastAPI application and serves analytical endpoints.
- **Cloud Run dashboard service:** Runs the Streamlit interface and sends requests to the API service.
- **Workload Identity Federation:** Allows GitHub Actions to authenticate to Google Cloud without storing a long-lived service-account key in GitHub.

## Design Principles

The architecture follows several practical software engineering principles:

- **Separation of concerns:** Data preparation, data access, analytical logic, API handling, and presentation have distinct responsibilities.
- **Reusability:** Analytical functions can be used by different endpoints without duplicating business calculations.
- **Testability:** Components and API behavior can be verified through automated tests.
- **Configuration through environment variables:** Deployment-specific settings, such as the API URL, can change without modifying application code.
- **Reproducible environments:** Dependency locking and Docker help maintain consistency across development, testing, and deployment.
- **Automated delivery:** GitHub Actions connects testing and deployment into a repeatable workflow.

## Future Improvements

Potential improvements include:

- Add structured application logging and centralized error reporting.
- Introduce API response schemas and more comprehensive input/output validation.
- Add post-deployment smoke tests to verify the live API and dashboard.
- Improve data validation and monitoring for data quality issues.
- Add deployment rollback procedures and more granular access permissions.
- Introduce versioned datasets and automated data pipeline execution as the project evolves.

These improvements can strengthen the application's reliability, observability, data quality, and operational maturity.
