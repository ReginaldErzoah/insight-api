# Insight API

Insight API is a sales analytics application that exposes business insights through a REST API built with **FastAPI** and presents them in an interactive dashboard built with **Streamlit**.

The project demonstrates how to separate data processing, analytical logic, API endpoints, and the user interface into distinct components.

## Why Not Just Use Power BI?

I could have built a Sales Analytics dashboard in Power BI in a few hours. So why spend days building an API, a data pipeline, and a separate frontend?

Because my goal goes beyond creating dashboards. I want to understand how data systems work behind the scenes—from processing and validating data to building APIs, testing applications, and eventually deploying them to production.

**Power BI helps me communicate insights. Insight API helps me learn to engineer the systems that deliver them.**

The extra time is an investment in becoming a better DataOps and MLOps professional.

## Features

- **Sales data processing:** Loads raw sales data from CSV, validates required columns and numeric fields, checks for missing values, and derives monthly reporting periods.
- **Processed data storage:** Saves processed sales data in Parquet format.
- **REST API:** Exposes sales metrics and aggregated results through FastAPI endpoints.
- **Interactive dashboard:** Presents key performance indicators and sales breakdowns using Streamlit.
- **Automated tests:** Uses pytest to test data processing, data loading, analytical functions, and API responses.

## Technology Stack

- Python
- FastAPI
- Streamlit
- Pandas
- Parquet / PyArrow
- Requests
- pytest
- uv

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API health |
| GET | `/sales/summary` | Returns key sales metrics |
| GET | `/sales/by-product` | Returns revenue and units sold by product |
| GET | `/sales/by-region` | Returns revenue and units sold by region |
| GET | `/sales/by-month` | Returns revenue and units sold by month |
| GET | `/sales/top-product` | Returns the product with the highest total revenue |

When the API is running, interactive endpoint documentation is available at `/docs`.

## Project Structure

```text
insight-api/
├── data/
│   ├── raw/
│   │   └── sales.csv
│   └── processed/
│       └── sales.parquet
├── docs/
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
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12 or a compatible version allowed by `pyproject.toml`
- uv
- Git

### 1. Clone the repository

```bash
git clone https://github.com/ReginaldErzoah/insight-api.git
cd insight-api
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Process the sales data

Run the processing pipeline to validate the raw CSV and generate the processed Parquet file:

```bash
uv run python -m insight_api.processing
```

### 4. Start the API

```bash
uv run uvicorn insight_api.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Explore the API interactively at:

`http://127.0.0.1:8000/docs`

### 5. Start the dashboard

Open a second terminal in the project directory and run:

```bash
uv run streamlit run streamlit_app.py
```

Streamlit will display the local dashboard URL in your terminal, usually `http://localhost:8501`.

The dashboard requires the API to be running.

## Running Tests

Run the test suite with:

```bash
uv run pytest
```

The tests cover data processing, processed-data loading, analytical functions, and API response structures.

## Configuration

The Streamlit application can use an `.env` file to configure the API address:

```dotenv
API_BASE_URL=http://127.0.0.1:8000
```

Keep `.env` out of version control. Do not commit secrets or credentials.

## Documentation

- [System Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Development Guide](docs/development.md)

## Roadmap

Planned improvements include:

- Containerising the API and dashboard with Docker
- Implementing continuous integration and delivery with GitHub Actions
- Improving test coverage and input validation
- Deploying the application to a cloud platform

## Project Status

Insight API is an active learning and portfolio project focused on building practical data applications with Python, data processing, APIs, and software engineering practices.