# Development Guide

This guide explains how to set up, run, and test Insight API on your local machine.

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Git

## 1. Clone the Repository

```bash
git clone https://github.com/ReginaldErzoah/insight-api.git
cd insight-api
```

## 2. Install Dependencies

Install the project dependencies using uv:

```bash
uv sync
```

This installs the dependencies specified in `pyproject.toml` and the locked versions recorded in `uv.lock`.

## 3. Process the Sales Data

Run the data processing pipeline:

```bash
uv run python -m insight_api.processing
```

The pipeline:

1. Loads the raw sales data from `data/raw/sales.csv`.
2. Validates required columns, numeric fields, and missing values.
3. Converts the sales date into a datetime value.
4. Derives the `month_year` reporting field.
5. Saves the processed data to `data/processed/sales.parquet`.

The processed file is required by the API's analytics endpoints.

## 4. Run the API

Start the FastAPI application:

```bash
uv run uvicorn insight_api.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

Health check:

`http://127.0.0.1:8000/health`

Keep this terminal running while using the dashboard.

## 5. Run the Streamlit Dashboard

Open a second terminal in the project root and run:

```bash
uv run streamlit run streamlit_app.py
```

Open the local URL shown in the terminal, usually:

`http://localhost:8501`

The dashboard communicates with the FastAPI backend to retrieve sales metrics and aggregated results.

### Environment Configuration

The dashboard can read its API base URL from a `.env` file in the project root:

```dotenv
API_BASE_URL=http://127.0.0.1:8000
```

Keep `.env` out of version control.

## 6. Run the Tests

Run the test suite:

```bash
uv run pytest
```

The current tests cover:

- Data processing and validation
- Processed-data loading
- Sales analytics functions
- API endpoint response structures

## 7. Project Structure

```text
insight-api/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── src/
│   └── insight_api/
│       ├── api/
│       ├── data_access/
│       ├── services/
│       ├── main.py
│       └── processing.py
├── tests/
├── streamlit_app.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Troubleshooting

**Processed data file not found**

Run the data processing pipeline and check that `data/processed/sales.parquet` exists.

**Dashboard cannot connect to the API**

Confirm that the API is running and that `API_BASE_URL` in `.env` points to the correct address.

**Tests fail**

Review the error output, confirm that dependencies are installed with `uv sync`, and check that the required data files are available.

## Current Development Status

Insight API currently runs locally with a FastAPI backend, a Streamlit dashboard, a CSV-to-Parquet processing pipeline, and pytest tests.

Docker containerisation, CI/CD automation, and cloud deployment are planned future improvements.