# System Architecture

Insight API separates data processing, analytical logic, API endpoints, and the user interface into distinct components.

## Architecture Overview

```text
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