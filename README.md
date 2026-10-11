# Insight API

**A containerised sales analytics application built with FastAPI and Streamlit, deployed on Google Cloud Run.**

Insight API processes sales data, exposes business metrics through a REST API, and presents those insights through an interactive dashboard. The project demonstrates how data processing, analytical logic, API services, and user interfaces can be developed, tested, containerised, and deployed as separate components.

## Live Application

- **Interactive dashboard:** [Open Insight Dashboard](https://insight-dashboard-854268296659.africa-south1.run.app)
- **REST API:** [Open Insight API](https://insight-api-vk5ztwb7gq-bq.a.run.app)
- **Interactive API documentation:** [Explore API endpoints](https://insight-api-vk5ztwb7gq-bq.a.run.app/docs)
- **Health check:** [Check API health](https://insight-api-vk5ztwb7gq-bq.a.run.app/health)

The dashboard communicates with the deployed API to retrieve sales analytics. Both applications run as separate services on Google Cloud Run.

## Why Not Just Use Power BI?

I could have built a sales analytics dashboard in Power BI in a few hours. So why spend days building an API, a data pipeline, automated tests, containers, and a separate frontend?

Because my goal goes beyond creating dashboards. I want to understand how data systems work behind the scenes—from processing and validating data to designing APIs, testing applications, and deploying reliable services.

**Power BI helps me communicate insights. Insight API helps me learn to engineer the systems that deliver them.**

This project is part of my journey toward Data Engineering, DataOps, and MLOps, with an emphasis on building reliable, maintainable, and production-oriented data applications.

## Features

- **Sales data processing:** Loads raw sales data from CSV, validates required columns and numeric fields, checks for missing values, and derives monthly reporting periods.
- **Processed data storage:** Stores processed sales data in Parquet format.
- **REST API:** Exposes sales metrics and aggregations through FastAPI.
- **Interactive dashboard:** Uses Streamlit to present key performance indicators and sales breakdowns.
- **Separation of concerns:** Organises data processing, data access, analytical functions, API routes, and presentation into distinct components.
- **Automated testing:** Uses pytest to test data processing, data loading, analytical functions, and API responses.
- **Containerisation:** Packages the application using Docker, with separate configurations for the API and dashboard services.
- **Local orchestration:** Uses Docker Compose to run the application services together during development.
- **Cloud deployment:** Hosts the API and dashboard as separate services on Google Cloud Run.
- **Continuous integration:** Uses GitHub Actions to automate configured project checks.

## Architecture

```text
                    Sales CSV
                        |
                        v
               Data Processing
             Validation and Cleaning
                        |
                        v
                 Sales Parquet
                        |
                        v
                Data Access Layer
                        |
                        v
                 Analysis Services
                        |
                        v
                   FastAPI
                 REST Endpoints
                        ^
                        |
                 HTTP Requests
                        |
                        |
                 Streamlit UI
                 Sales Dashboard
                        |
                        v
                     User
```

The API and dashboard are packaged as separate containerised services and deployed independently to Google Cloud Run.

The dashboard uses the `API_BASE_URL` environment variable to determine which API to call. In local development, this can point to the local API or the API service in Docker Compose. In the cloud, it points to the deployed FastAPI service.

See [System Architecture](docs/architecture.md) for more details.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| API | FastAPI, Uvicorn |
| Dashboard | Streamlit |
| Data processing | Pandas |
| Data storage | CSV, Parquet, PyArrow |
| HTTP communication | Requests |
| Dependency management | uv |
| Testing | pytest |
| Containerisation | Docker |
| Local orchestration | Docker Compose |
| Container registry | Google Artifact Registry |
| Cloud deployment | Google Cloud Run |
| Continuous integration | GitHub Actions |

## API Endpoints

All endpoints use the HTTP `GET` method.

| Endpoint | Description |
|---|---|
| `/health` | Checks API health |
| `/sales/summary` | Returns key sales metrics |
| `/sales/by-product` | Returns revenue and units sold by product |
| `/sales/by-region` | Returns revenue and units sold by region |
| `/sales/by-month` | Returns revenue and units sold by month |
| `/sales/top-product` | Returns the product with the highest total revenue |
| `/docs` | Provides interactive Swagger API documentation |

### Example: Sales Summary

Request:

```bash
curl https://insight-api-vk5ztwb7gq-bq.a.run.app/sales/summary
```

Example response:

```json
{
  "total_revenue": 358400.0,
  "total_units_sold": 474,
  "average_revenue_per_record": 7314.285714285715,
  "average_revenue_per_unit": 756.1181434599156
}
```

These values represent the response observed during deployment verification. The results depend on the dataset currently loaded by the application.

For endpoint details and response examples, see the [API Reference](docs/api.md).

## Project Structure

```text
insight-api/
├── data/
│   ├── raw/
│   │   └── sales.csv
│   └── processed/
│       └── sales.parquet
├── docs/
│   ├── architecture.md
│   ├── api.md
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
├── .dockerignore
├── .gitignore
├── Dockerfile
├── compose.yaml
├── dashboard-service.yaml
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

Install the following tools:

- Python 3.12 or a compatible version supported by `pyproject.toml`
- [uv](https://docs.astral.sh/uv/)
- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for containerised development

### 1. Clone the repository

```bash
git clone https://github.com/ReginaldErzoah/insight-api.git
cd insight-api
```

### 2. Install dependencies

```bash
uv sync
```

The `uv.lock` file helps maintain reproducible dependency versions.

### 3. Process the sales data

```bash
uv run python -m insight_api.processing
```

This runs the processing module to validate the raw sales data and generate the processed Parquet file.

Ensure the expected input data exists before running the pipeline.

### 4. Start the API

```bash
uv run uvicorn insight_api.main:app --reload
```

The API will be available at:

- Base URL: http://127.0.0.1:8000
- Interactive documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 5. Start the dashboard

Open a second terminal in the project directory and run:

```bash
uv run streamlit run streamlit_app.py
```

Streamlit will display its local URL, usually http://localhost:8501.

The dashboard requires the API to be running and configured at the correct address.

### 6. Configure the API URL

The dashboard uses `API_BASE_URL` to determine the API base address.

For local development, the value is typically:

```dotenv
API_BASE_URL=http://127.0.0.1:8000
```

For Docker Compose, the API service can be addressed by its service name, such as `http://api:8000`, when that matches the Compose configuration.

For the deployed dashboard, the configured value is:

```text
https://insight-api-vk5ztwb7gq-bq.a.run.app
```

Set environment variables using your chosen development or deployment configuration. Keep local `.env` files and credentials out of version control.

## Running Tests

Run the test suite with:

```bash
uv run pytest
```

The tests cover data processing, processed-data loading, analytical functions, and API response structures.

Run tests before committing changes so regressions are caught early.

## Running with Docker

Docker provides a consistent environment for running the application beyond your local Python setup.

Build the image:

```bash
docker build -t insight-api:local .
```

Run the API container:

```bash
docker run --rm -p 8000:8000 insight-api:local
```

The API should then be available at http://localhost:8000.

To run the API and dashboard together using the project's Docker Compose configuration:

```bash
docker compose up --build
```

Use `Ctrl+C` to stop the running services. To stop and remove the Compose containers and network, run:

```bash
docker compose down
```

Refer to the Dockerfile and Compose configuration for the exact service commands, ports, and environment variables.

## Deployment

Insight API is deployed on Google Cloud Run using separate services for the FastAPI backend and Streamlit dashboard.

### Deployment components

- **Google Artifact Registry:** Stores the Docker image.
- **Cloud Run — API:** Runs the FastAPI application on port `8000`.
- **Cloud Run — dashboard:** Runs the Streamlit application on port `8080`.
- **Environment configuration:** Connects the dashboard to the deployed API using `API_BASE_URL`.

### Current deployment URLs

| Service | URL |
|---|---|
| API | https://insight-api-vk5ztwb7gq-bq.a.run.app |
| Dashboard | https://insight-dashboard-854268296659.africa-south1.run.app |

### Current deployment workflow

The initial deployment was performed manually:

1. Build the Docker image.
2. Tag and push the image to Google Artifact Registry.
3. Deploy the API service to Cloud Run.
4. Deploy the dashboard service with its Streamlit startup command.
5. Configure public access and the dashboard's API URL.
6. Verify the health and sales summary endpoints and open the dashboard.

GitHub Actions currently supports configured CI checks. Automatic deployment from GitHub to Cloud Run has not yet been configured.

See the [Development Guide](docs/development.md) for development commands and the deployment documentation for the current manual workflow.

**Cost note:** Cloud Run and Artifact Registry may incur charges depending on usage, region, storage, and data transfer. Budget alerts are notifications, not hard spending limits.

## Documentation

- [System Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Development Guide](docs/development.md)

## Roadmap

- [x] Build a sales data processing pipeline.
- [x] Expose sales analytics through a FastAPI REST API.
- [x] Build an interactive Streamlit dashboard.
- [x] Add automated tests using pytest.
- [x] Containerise the application with Docker.
- [x] Run the API and dashboard as separate services.
- [x] Publish a container image to Google Artifact Registry.
- [x] Deploy the API and dashboard to Google Cloud Run.
- [x] Verify the deployed API endpoints and dashboard.
- [ ] Expand test coverage and strengthen data validation.
- [ ] Improve operational logging, error handling, and observability.
- [ ] Automate image publishing and Cloud Run deployment with GitHub Actions.
- [ ] Add deployment verification and rollback procedures.
- [ ] Explore monitoring, performance, and reliability improvements.

## Project Status

Insight API is an active learning and portfolio project focused on practical data applications and software engineering.

The first cloud deployment is complete. The next phase focuses on improving reliability, automating deployment, and building stronger operational practices.

## Author

**Reginald Erzoah**

GitHub: [ReginaldErzoah](https://github.com/ReginaldErzoah)
