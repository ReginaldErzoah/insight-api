# Insight API

**A containerised sales analytics application built with FastAPI and Streamlit, deployed on Google Cloud Run.**

Insight API processes sales data, exposes business metrics through a REST API, and presents those insights through an interactive dashboard. The project demonstrates how data processing, analytical logic, API services, and user interfaces can be developed, tested, containerised, and deployed using modern software engineering and DevOps practices.

## Live Application

- **Interactive dashboard:** [Open Insight Dashboard](https://insight-dashboard-854268296659.africa-south1.run.app)
- **REST API:** [Open Insight API](https://insight-api-vk5ztwb7gq-bq.a.run.app)
- **Interactive API documentation:** [Explore API endpoints](https://insight-api-vk5ztwb7gq-bq.a.run.app/docs)
- **API health check:** [Check API health](https://insight-api-vk5ztwb7gq-bq.a.run.app/health)

The dashboard communicates with the deployed API to retrieve sales analytics. The API and dashboard run as separate services on Google Cloud Run.

## Why Not Just Use Power BI?

I could have built a sales analytics dashboard in Power BI in a few hours. So why spend days building an API, a data pipeline, automated tests, containers, and a separate frontend?

Because my goal goes beyond creating dashboards. I want to understand how data systems work behind the scenes—from processing and validating data to designing APIs, testing applications, automating deployments, and operating reliable services.

**Power BI helps me communicate insights. Insight API helps me learn to engineer the systems that deliver them.**

This project is part of my journey toward Data Engineering, DataOps, and MLOps, with an emphasis on building reliable, maintainable, and production-oriented data applications.

## Features

- **Sales data processing:** Loads raw sales data from CSV, validates required columns and numeric fields, checks for missing values, and derives monthly reporting periods.
- **Processed data storage:** Stores processed sales data in Parquet format.
- **REST API:** Exposes sales metrics and aggregations through FastAPI.
- **Interactive dashboard:** Uses Streamlit to present key performance indicators, charts, and sales breakdowns.
- **Separation of concerns:** Organises data processing, data access, analytical functions, API routes, and presentation into distinct components.
- **Automated testing:** Uses pytest to test data processing, data loading, analytical functions, and API responses.
- **Containerisation:** Packages the application using Docker, with separate configurations for the API and dashboard services.
- **Local orchestration:** Uses Docker Compose to run the application services together during development.
- **Cloud deployment:** Hosts the API and dashboard as separate services on Google Cloud Run.
- **Continuous integration:** Uses GitHub Actions to run tests, build the Docker image, validate Docker Compose, and check local service responses.
- **Continuous deployment:** Automatically builds and pushes a commit-specific image to Google Artifact Registry and deploys the API and dashboard to Cloud Run after successful CI on pushes to `main`.
- **Secure cloud authentication:** Uses Workload Identity Federation to authenticate GitHub Actions to Google Cloud without storing a long-lived service-account key in GitHub.

## Dataset and Data Source

Insight API uses synthetic sales data generated for deminstration.

## Architecture

### Application architecture

```text
              Raw Sales Data (CSV)
                       |
                       v
              Data Processing
          Validation and Transformation
                       |
                       v
              Processed Data (Parquet)
                       |
                       v
                Data Access
                       |
                       v
              Analytics Services
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

The API provides analytical results as JSON responses. The Streamlit dashboard requests those results over HTTP and presents them to users.

### CI/CD and deployment architecture

```text
             GitHub Repository
                      |
                      v
               GitHub Actions
                      |
             +--------+--------+
             |                 |
             v                 v
        Install and        Build Docker
        Run Tests             Image
             |                 |
             +--------+--------+
                      |
                      v
            Validate Compose Setup
                      |
                      v
            Start and Check Services
                      |
                      v
            CI Job Must Succeed
                      |
                      v
          Push to main Branch Only
                      |
                      v
       Authenticate Using Workload
            Identity Federation
                      |
                      v
          Build Commit-Specific Image
                      |
                      v
             Artifact Registry
                      |
              +-------+-------+
              |               |
              v               v
          Cloud Run API   Cloud Run Dashboard
              |               |
              +-------+-------+
                      |
                      v
               Live Application
```

The API and dashboard use the same Docker image with different startup commands and port configurations. They are deployed as separate Cloud Run services.

The dashboard uses the `API_BASE_URL` environment variable to determine which API to call. This allows it to communicate with a local API during development, an API container through Docker Compose, or the deployed API in the cloud.

See [System Architecture](docs/architecture.md) for further details.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming language | Python 3.12 |
| API framework | FastAPI |
| ASGI server | Uvicorn |
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
| CI/CD automation | GitHub Actions |
| Cloud authentication | Workload Identity Federation |

## API Endpoints

All sales endpoints use the HTTP `GET` method.

| Endpoint | Description |
|---|---|
| `/health` | Checks basic API health |
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

These values reflect a response observed during deployment verification. Actual results depend on the dataset currently loaded by the application.

For endpoint details, example responses, and testing instructions, see the [API Reference](docs/api.md).

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
│       └── ci.yaml
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
| `dashboard-service.yaml` | Defines the dashboard's Cloud Run configuration |
| `.github/workflows/ci.yaml` | Defines automated checks and deployment |

## Getting Started

### Prerequisites

Install the following tools:

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for containerised development

Docker is optional when running the application directly through Python.

### 1. Clone the repository

```bash
git clone https://github.com/ReginaldErzoah/insight-api.git
cd insight-api
```

### 2. Install dependencies

```bash
uv sync --locked --group dev
```

This installs the project dependencies, including the development dependency group, using the versions recorded in `uv.lock`.

Verify the Python version:

```bash
uv run python --version
```

### 3. Process the sales data

```bash
uv run python -m insight_api.processing
```

This validates the raw sales data and generates the processed Parquet dataset.

Ensure the expected input file, `data/raw/sales.csv`, exists before running the pipeline.

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

The API must be running, and the dashboard must be configured to use the correct API address.

### 6. Configure the API URL

For local development, the dashboard's `API_BASE_URL` should point to the local API:

```text
API_BASE_URL=http://127.0.0.1:8000
```

For Docker Compose, use the API service's name and internal port. For example, if the service is named `api`:

```text
API_BASE_URL=http://api:8000
```

For the deployed dashboard, the configured value is:

```text
API_BASE_URL=https://insight-api-vk5ztwb7gq-bq.a.run.app
```

Configure the variable using the mechanism supported by the application and your development environment. Keep local `.env` files and credentials out of version control.

## Running Tests

Run the automated test suite:

```bash
uv run --locked pytest
```

Run tests before committing changes to catch regressions early.

The CI workflow also runs the tests automatically on pushes and pull requests.

## Running with Docker

Build the image:

```bash
docker build -t insight-api:local .
```

Run the API container:

```bash
docker run --rm -p 8000:8000 insight-api:local
```

The API should then be available at http://localhost:8000.

To run the services together using Docker Compose:

```bash
docker compose up --build
```

To stop and remove the Compose containers and network:

```bash
docker compose down
```

See [Development Guide](docs/development.md) for more details about local setup, Docker networking, testing, and troubleshooting.

## CI/CD and Cloud Deployment

Insight API uses GitHub Actions to automate testing and deployment to Google Cloud Run.

### Continuous integration

The CI job runs on pushes and pull requests. It:

1. Checks out the repository.
2. Sets up Python and uv.
3. Installs dependencies.
4. Runs automated tests.
5. Builds the Docker image.
6. Validates the Docker Compose configuration.
7. Starts the API and dashboard.
8. Checks that both local services respond.

### Continuous deployment

When a push to `main` occurs and the CI job succeeds, the deployment job:

1. Authenticates to Google Cloud using Workload Identity Federation.
2. Builds a Docker image tagged with the commit SHA.
3. Pushes the image to Google Artifact Registry.
4. Deploys the API service to Cloud Run.
5. Updates the dashboard configuration to use the same image.
6. Deploys the dashboard service to Cloud Run.

This provides a repeatable path from code changes to a deployed application without requiring a long-lived Google Cloud service-account key in GitHub.

The current workflow checks the local services before deployment. Post-deployment smoke tests and automated rollback procedures remain potential improvements.

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
- [x] Publish container images to Google Artifact Registry.
- [x] Deploy the API and dashboard to Google Cloud Run.
- [x] Automate CI checks with GitHub Actions.
- [x] Automate deployment to Cloud Run from successful pushes to `main`.
- [ ] Expand test coverage and strengthen data validation.
- [ ] Add post-deployment smoke tests.
- [ ] Improve structured logging, error handling, and observability.
- [ ] Introduce deployment rollback procedures.
- [ ] Improve monitoring, performance, and reliability.
- [ ] Explore automated data pipeline execution and data quality monitoring.

## Project Status

Insight API is an active learning and portfolio project focused on practical data applications and software engineering.

The application has a deployed API and dashboard, containerised services, automated tests, and a GitHub Actions pipeline that performs CI/CD.

The next phase focuses on strengthening reliability, observability, data quality, and operational practices as the project evolves.

## Author

**Reginald Erzoah**

- GitHub: [ReginaldErzoah](https://github.com/ReginaldErzoah)
- Portfolio: [reginalderzoah.github.io](https://reginalderzoah.github.io)
