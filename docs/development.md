# Development Guide

This guide explains how to set up, run, test, troubleshoot, and deploy Insight API in a local development environment.

Insight API consists of a FastAPI backend, a Streamlit dashboard, and a data processing pipeline. The project uses `uv` for Python dependency management, `pytest` for automated testing, Docker for containerisation, GitHub Actions for CI/CD, and Google Cloud Run for deployment.

## Prerequisites

Install the following tools before starting:

- **Python 3.12** - Python runtime.
- **uv** - Python project and dependency manager. [Installation guide](https://docs.astral.sh/uv/).
- **Git** - Version control.
- **Docker Desktop** - Required for building and running containers. [Installation guide](https://docs.docker.com/desktop/).
- **Visual Studio Code (recommended)** - Code editor.

Docker is optional if you only want to run the application directly on your machine.

## 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/ReginaldErzoah/insight-api.git
cd insight-api
```

If you have already cloned the repository, navigate to its directory instead.

## 2. Install Dependencies

Install the dependencies defined in `pyproject.toml`:

```bash
uv sync --locked --group dev
```

This creates or updates the project's virtual environment and installs the dependency versions recorded in `uv.lock`, including the development dependency group.

Verify the Python version:

```bash
uv run python --version
```

The project uses Python 3.12.

## 3. Process the Sales Data

Run the data processing pipeline:

```bash
uv run python -m insight_api.processing
```

The pipeline:

1. Loads raw sales data from `data/raw/sales.csv`.
2. Validates the required columns and data quality rules implemented by the project.
3. Converts the sales date into a datetime value.
4. Derives the `month_year` reporting field.
5. Saves the processed dataset to `data/processed/sales.parquet`.

The analytics layer reads the processed Parquet file. Run the pipeline again whenever you need to regenerate that dataset from the raw CSV.

## 4. Run the API

Start the FastAPI development server:

```bash
uv run uvicorn insight_api.main:app --reload
```

The `--reload` option restarts the development server when relevant source files change.

The API is available at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Keep this terminal running while using the dashboard in a separate process.

## 5. Run the Streamlit Dashboard

Open a second terminal in the project root and run:

```bash
uv run streamlit run streamlit_app.py
```

Open the local dashboard URL displayed in the terminal, usually http://localhost:8501.

The dashboard sends HTTP requests to the FastAPI backend to retrieve sales metrics and aggregated results.

### Configure the API URL

The dashboard uses the `API_BASE_URL` environment variable to identify the API server.

For local development, set it to:

```text
API_BASE_URL=http://127.0.0.1:8000
```

Configure this variable using the mechanism supported by the application. If the project loads environment variables from a `.env` file, place the setting in that file; otherwise, set it in your terminal or development environment.

For Git Bash, you can set the variable for the current terminal session with:

```bash
export API_BASE_URL=http://127.0.0.1:8000
```

Keep local environment files out of version control. Do not commit secrets or credentials.

## 6. Run the Tests

Run the automated test suite:

```bash
uv run --locked pytest
```

The tests cover the functionality implemented in the project, including data processing and validation, processed-data loading, sales analytics, and API endpoint behaviour.

Before committing changes, run the tests and investigate any failures.

## 7. Run the Application with Docker

Docker packages the application and its dependencies into a container image. This helps make the runtime environment more consistent between local development and deployment.

Ensure Docker Desktop is running before executing Docker commands.

### Build the Docker image

From the project root:

```bash
docker build -t insight-api:local .
```

This builds the image using the instructions in `Dockerfile` and tags it `insight-api:local`.

### Run the API container

```bash
docker run --rm -p 8000:8000 insight-api:local
```

Test the API at http://127.0.0.1:8000/health.

The options mean:

- `--rm` removes the stopped container when it exits.
- `-p 8000:8000` maps port 8000 on your machine to port 8000 inside the container.
- `insight-api:local` identifies the image to run.

Press `Ctrl+C` to stop the foreground container.

### Run the services with Docker Compose

Build and start the services defined in `compose.yaml`:

```bash
docker compose up --build
```

Compose manages the API and dashboard as separate services when configured that way.

Within the Compose network, the dashboard should use the API service name and internal port. For example, if the API service is named `api`:

```text
API_BASE_URL=http://api:8000
```

The hostname `api` must match the service name in `compose.yaml`. It is not generally interchangeable with `localhost`: inside the dashboard container, `localhost` refers to that dashboard container itself.

With the current local configuration, the API is expected on port 8000 and the dashboard on port 8501.

To view service logs:

```bash
docker compose logs
```

To stop and remove the Compose containers and network:

```bash
docker compose down
```

## 8. Project Structure

This is a high-level overview of the project. Refer to the repository for the complete current structure.

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
│       │   └── routes.py
│       ├── data_access/
│       │   └── loader.py
│       ├── services/
│       │   └── analysis.py
│       ├── main.py
│       └── processing.py
├── tests/
├── .github/
│   └── workflows/
│       └── ci.yaml
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
| `processing.py` | Validates and transforms raw sales data |
| `data_access/` | Loads the processed dataset |
| `services/` | Contains sales analytics and business logic |
| `api/routes.py` | Defines API endpoints |
| `main.py` | Creates the FastAPI application |
| `streamlit_app.py` | Provides the interactive dashboard |
| `tests/` | Contains automated tests |
| `Dockerfile` | Defines how to build the application image |
| `compose.yaml` | Defines the local multi-service container setup |
| `dashboard-service.yaml` | Defines the dashboard's Cloud Run service configuration |
| `.github/workflows/ci.yaml` | Defines automated testing, image building, and deployment |

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

Use `http://127.0.0.1:8000` when the dashboard runs directly on your machine and the API is available locally.

When the dashboard runs inside Docker Compose, use the API's Compose service name and internal port instead.

In the cloud, confirm that the dashboard's `API_BASE_URL` points to the deployed API service.

### Tests fail

Review the error output and confirm that:

- Dependencies are installed using `uv sync --locked --group dev`.
- Required data files are available.
- The test environment matches the project's expected configuration.
- Recent code changes have not broken existing behaviour.

### Docker container fails to start

Confirm that Docker Desktop is running and the image built successfully.

For a running or recently stopped Compose application, inspect the logs:

```bash
docker compose logs
```

To see running containers:

```bash
docker compose ps
```

### API works locally but not in the cloud

Check the Cloud Run service logs, configured port, environment variables, and container startup command. Confirm that the application listens on the configured port and binds to `0.0.0.0`.

For the dashboard, also verify that `API_BASE_URL` points to the correct deployed API URL.

### CI/CD workflow fails

Open the repository's **Actions** tab on GitHub and inspect the failed workflow run.

Check the failing step before changing configuration. Common causes include:

- A failing automated test.
- A Docker image build error.
- An invalid Docker Compose configuration.
- Missing GitHub repository variables.
- Workload Identity Federation or Google Cloud IAM permission errors.
- An image push or Cloud Run deployment failure.

The deployment job depends on the CI job succeeding and is restricted to pushes to the `main` branch.

## 10. Current Development and Deployment Status

Insight API has the following implemented capabilities:

- A CSV-to-Parquet data processing pipeline.
- A FastAPI backend with sales analytics endpoints.
- A Streamlit dashboard that consumes the API.
- Automated tests using pytest.
- Docker containerisation and Docker Compose configuration.
- GitHub Actions CI/CD.
- Automated deployment of the API and dashboard to Google Cloud Run.
- An Artifact Registry repository for storing container images.
- Workload Identity Federation for GitHub Actions authentication to Google Cloud.

### Deployed services

- **Dashboard:** https://insight-dashboard-854268296659.africa-south1.run.app
- **API:** https://insight-api-vk5ztwb7gq-bq.a.run.app
- **Interactive API documentation:** https://insight-api-vk5ztwb7gq-bq.a.run.app/docs
- **API health check:** https://insight-api-vk5ztwb7gq-bq.a.run.app/health

These are the configured service URLs; availability should be verified when needed.

### CI/CD workflow

The current GitHub Actions workflow performs the following operations:

1. Runs on pushes and pull requests.
2. Installs Python and project dependencies.
3. Runs automated tests.
4. Builds a Docker image.
5. Validates the Docker Compose configuration.
6. Starts the API and dashboard and checks their local responses.
7. For pushes to `main`, authenticates to Google Cloud using Workload Identity Federation.
8. Builds and pushes a commit-specific image to Artifact Registry.
9. Deploys the API and dashboard to Cloud Run.

The workflow therefore implements both **continuous integration (CI)** and **continuous deployment (CD)**. The local health checks validate the services before deployment; separate post-deployment smoke tests can be added to verify the live services after deployment.

## 11. Recommended Development Workflow

For a typical code change:

1. Create a Git branch for the change.
2. Modify the code or documentation.
3. Run the relevant tests locally.
4. Build or test with Docker when the change affects the container or service configuration.
5. Commit and push the branch.
6. Open a pull request and review the CI results.
7. Merge into `main` when the change is ready.
8. Check the GitHub Actions deployment result and verify the deployed service when appropriate.

**Important:** In the current workflow, every push to `main` that passes CI can trigger deployment, including documentation-only changes. Path filters can be introduced later if you want documentation-only changes to skip deployment.