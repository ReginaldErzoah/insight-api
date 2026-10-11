# Development Guide

This guide explains how to set up, run, test, and troubleshoot Insight API in a local development environment.

Insight API consists of a FastAPI backend, a Streamlit dashboard, and a data processing pipeline. The project uses `uv` for Python dependency management and `pytest` for automated testing.

## Prerequisites

Install the following tools before starting:

- **Python 3.12** - Python runtime.
- **uv** - Python project and dependency manager. [Installation guide](https://docs.astral.sh/uv/).
- **Git** - Version control.
- **Docker Desktop** - Required for building and running containers. [Installation guide](https://docs.docker.com/desktop/).

Docker is optional if you only want to run the application directly on your machine.

## 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/ReginaldErzoah/insight-api.git
cd insight-api
```

## 2. Install Dependencies

Install the dependencies defined in `pyproject.toml`:

```bash
uv sync
```

This creates or updates the project's virtual environment and installs the locked dependency versions recorded in `uv.lock`.

To verify the Python version used by the project:

```bash
uv run python --version
```

## 3. Process the Sales Data

Run the data processing pipeline:

```bash
uv run python -m insight_api.processing
```

The pipeline performs the following operations:

1. Loads the raw sales data from `data/raw/sales.csv`.
2. Validates the required columns and data quality rules implemented by the project.
3. Converts the sales date into a datetime value.
4. Derives the `month_year` reporting field.
5. Saves the processed data to `data/processed/sales.parquet`.

The processed Parquet file is required by the analytics layer. Run the pipeline whenever you need to regenerate the processed dataset from the raw CSV.

## 4. Run the API

Start the FastAPI application:

```bash
uv run uvicorn insight_api.main:app --reload
```

The `--reload` option automatically restarts the development server when relevant source files change.

The API will be available at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Keep this terminal running while using the dashboard in a separate process.

## 5. Run the Streamlit Dashboard

Open a second terminal in the project root and run:

```bash
uv run streamlit run streamlit_app.py
```

Open the local dashboard URL shown in the terminal, usually:

http://localhost:8501

The dashboard sends requests to the FastAPI backend to retrieve sales metrics and aggregated results.

### Configure the API URL

The dashboard uses the `API_BASE_URL` environment variable to identify the API server.

For local development, the value should be:

```dotenv
API_BASE_URL=http://127.0.0.1:8000
```

If your application reads this variable from a `.env` file, create that file in the project root and confirm that the application loads it correctly. If the application reads environment variables directly, set the variable in your terminal or development environment instead.

Keep local environment files out of version control. Do not commit secrets or credentials.

## 6. Run the Tests

Run the automated test suite:

```bash
uv run pytest
```

The tests cover the functionality implemented in the project, including data processing and validation, processed-data loading, sales analytics, and API endpoint behaviour.

When making changes, run the relevant tests before committing your work.

## 7. Run the Application with Docker

Docker lets you package the application and run its services in containers, reducing differences between development and deployment environments.

Ensure Docker Desktop is running before executing these commands.

### Build the API image

From the project root:

```bash
docker build -t insight-api:local .
```

### Run the API container

```bash
docker run --rm -p 8000:8000 insight-api:local
```

Test the API at http://127.0.0.1:8000/health.

The `--rm` option removes the stopped container when it exits. The `-p 8000:8000` option maps port 8000 on your machine to port 8000 in the container.

### Run the services with Docker Compose

To build and start the services defined in `compose.yaml`:

```bash
docker compose up --build
```

If the Compose configuration defines the API and dashboard as separate services, Compose starts them according to that configuration. The dashboard should use the API service name as its hostname when communicating with the API inside the Compose network.

For example:

```dotenv
API_BASE_URL=http://api:8000
```

Here, `api` must match the actual API service name in `compose.yaml`.

To stop the services:

```bash
docker compose down
```

## 8. Project Structure

The following is a high-level overview of the project. Refer to the repository for the complete current structure.

```text
insight-api/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── api.md
│   ├── architecture.md
│   └── development.md
├── src/
│   └── insight_api/
│       ├── api/
│       ├── data_access/
│       ├── services/
│       ├── main.py
│       └── processing.py
├── tests/
├── .github/
│   └── workflows/
├── Dockerfile
├── compose.yaml
├── dashboard-service.yaml
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

### Key components

| Component | Responsibility |
|---|---|
| `processing.py` | Validates and transforms the raw sales data |
| `data_access/` | Loads the processed data |
| `services/` | Contains sales analytics and business logic |
| `api/` | Defines the API endpoints |
| `main.py` | Creates the FastAPI application |
| `streamlit_app.py` | Provides the interactive dashboard |
| `tests/` | Contains automated tests |
| `Dockerfile` | Defines how to build the API container image |
| `compose.yaml` | Defines the local multi-service container setup |
| `dashboard-service.yaml` | Defines the dashboard's Cloud Run service configuration |

## 9. Troubleshooting

### Processed data file not found

Run the data processing pipeline:

```bash
uv run python -m insight_api.processing
```

Then check that `data/processed/sales.parquet` exists at the location expected by the application.

### Dashboard cannot connect to the API

Check that:

1. The API is running.
2. The API responds at its health-check endpoint.
3. `API_BASE_URL` points to the correct address.
4. Both services can reach each other in their current environment.

Use `http://127.0.0.1:8000` when the dashboard runs directly on your machine and the API is available locally. When the dashboard runs inside Docker Compose, use the API's Compose service name and internal port instead.

### Tests fail

Review the error output and confirm that:

- Dependencies are installed with `uv sync`.
- Required data files are available.
- The test environment matches the project's expected configuration.
- Recent code changes have not broken existing behaviour.

### Docker container fails to start

Check the container logs and confirm that the image was built successfully.

For a Compose-based application, use:

```bash
docker compose logs
```

### API works locally but not in the cloud

Check the Cloud Run service logs, configured port, environment variables, and container startup command. Confirm that the application listens on the port provided by the deployment environment.

## 10. Current Development and Deployment Status

Insight API has the following implemented capabilities:

- A CSV-to-Parquet data processing pipeline.
- A FastAPI backend with sales analytics endpoints.
- A Streamlit dashboard that consumes the API.
- Automated tests using pytest.
- Docker containerisation and Docker Compose configuration.
- A GitHub Actions workflow for continuous integration checks.
- Deployment of the API and dashboard to Google Cloud Run.
- An Artifact Registry repository for storing the container image.

The application is publicly accessible through the following deployed services:

- **Dashboard:** https://insight-dashboard-854268296659.africa-south1.run.app
- **API:** https://insight-api-vk5ztwb7gq-bq.a.run.app
- **API documentation:** https://insight-api-vk5ztwb7gq-bq.a.run.app/docs

Continuous integration and continuous deployment are different: the existing GitHub Actions workflow performs CI checks, while automatic deployment from GitHub to Cloud Run is not yet configured.

