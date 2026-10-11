Let's create the three documentation files for Insight API. We'll start with `docs/architecture.md`, then document the API endpoints, and finally explain how to develop and run the project.

## Step 1: Create `docs/architecture.md`

In VS Code, right-click the `docs` folder, select New File, and name it `architecture.md`.

Paste this content:

# System Architecture

Insight API separates data processing, analytical logic, API endpoints, and the user interface into distinct components.

## Architecture Overview

```
Raw Sales Data (CSV)
        |
        v
Data Processing Pipeline
  - Validate columns
  - Check numeric fields
  - Check missing values
  - Transform dates
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
Streamlit Dashboard
```

## Main Components

### 1. Data Processing

**File:** `src/insight_api/processing.py`

Loads raw sales data from CSV, validates the data, derives a monthly reporting field, and saves the processed data in Parquet format.

### 2. Data Access

**File:** `src/insight_api/data_access/loader.py`

Loads the processed Parquet file into a Pandas DataFrame for analysis. It raises an error if the file cannot be found.

### 3. Analytics Services

**File:** `src/insight_api/services/analysis.py`

Contains reusable functions for calculating sales metrics, including total revenue, units sold, average revenue, and sales breakdowns by product, region, and month.

### 4. API Layer

**Files:** `src/insight_api/main.py` and `src/insight_api/api/routes.py`

FastAPI exposes the analytical results through HTTP endpoints and returns responses in JSON format.

### 5. Frontend

**File:** `streamlit_app.py`

Provides an interactive dashboard that requests data from the API and displays key metrics, charts, and tables.

## Design Approach

The project separates responsibilities so that data processing, business calculations, API handling, and presentation can be developed and tested independently.

This structure also provides a foundation for future improvements, including Docker containerisation, automated CI/CD workflows, and cloud deployment.

Save the file.

## Step 2: Create `docs/api.md`

Create another file named `api.md` inside `docs/`, then paste:

# API Reference

Insight API provides sales analytics through REST endpoints built with FastAPI.

## Base URL

When running locally:

```
http://127.0.0.1:8000
```

Interactive API documentation is available at `/docs`.

## Endpoints

### `GET /health`

Checks whether the API is responding.

Example response:

```
{
  "status": "healthy"
}
```

### `GET /sales/summary`

Returns the main sales metrics.

Example response structure:

```
{
  "total_revenue": 125000.0,
  "total_units_sold": 450,
  "average_revenue_per_record": 2500.0,
  "average_revenue_per_unit": 277.78
}
```

The figures above are illustrative, not measured project results.

### `GET /sales/by-product`

Returns revenue and units sold grouped by product.

Response fields:

- `revenue_by_product`
- `units_by_product`

### `GET /sales/by-region`

Returns revenue and units sold grouped by region.

Response fields:

- `revenue_by_region`
- `units_by_region`

### `GET /sales/by-month`

Returns revenue and units sold grouped by month.

Response fields:

- `revenue_by_month`
- `units_by_month`

### `GET /sales/top-product`

Returns the product with the highest total revenue.

Example response:

```
{
  "top_product": "Laptop"
}
```

The product name is illustrative.

## Notes

All endpoints use the HTTP `GET` method. The API reads processed sales data and returns analytics in JSON format.

Save the file.

## Step 3: Create `docs/development.md`

Create `development.md` inside `docs/` and paste:

# Development Guide

This guide explains how to set up, run, and test Insight API locally.

## Prerequisites

- Python 3.12 or a compatible version
- uv
- Git

## Install Dependencies

From the project root:

```
uv sync
```

## Process the Sales Data

Generate the processed Parquet file from the raw CSV:

```
uv run python -m insight_api.processing
```

The pipeline validates required columns, numeric fields, and missing values before saving the processed data.

## Run the API

```
uv run uvicorn insight_api.main:app --reload
```

API URL: `http://127.0.0.1:8000`

Interactive documentation: `http://127.0.0.1:8000/docs`

## Run the Dashboard

Open a second terminal in the project root:

```
uv run streamlit run streamlit_app.py
```

Use the local URL displayed in the terminal. The API must be running for the dashboard to retrieve sales data.

## Run Tests

```
uv run pytest
```

The test suite covers data processing, data loading, analytical functions, and API responses.

## Environment Configuration

The dashboard can use a `.env` file containing:

```
API_BASE_URL=http://127.0.0.1:8000
```

Keep `.env` out of version control.

## Current Limitations

- The API relies on a locally available processed Parquet file.
- The application has not yet been containerised.
- CI/CD and cloud deployment are planned future improvements.

Save the file.

## Step 4: Verify your documentation

In Git Bash, run:

```
git status --short
```

You should see your changed `README.md` and the three new files under `docs/`.

One final check: the example API figures are explicitly labelled illustrative, so nobody mistakes them for actual sales results.

Once these files are saved, your documentation foundation is ready. The next step will be to review the README links and run the tests before committing the changes.