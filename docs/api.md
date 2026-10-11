# API Reference

Insight API is a REST API built with FastAPI that provides sales analytics from processed sales data.

## Base URL

When running locally:

```text
http://127.0.0.1:8000
```

FastAPI's interactive documentation is available at:

`http://127.0.0.1:8000/docs`

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

Checks whether the API is responding.

**Example response:**

```json
{
  "status": "healthy"
}
```

### 2. Sales Summary

**Endpoint:** `GET /sales/summary`

Returns the main sales performance metrics.

**Response fields:**

| Field | Description |
|---|---|
| `total_revenue` | Total revenue across all sales records |
| `total_units_sold` | Total units sold |
| `average_revenue_per_record` | Average revenue per sales record |
| `average_revenue_per_unit` | Total revenue divided by total units sold |

**Example response:**

```json
{
  "total_revenue": 125000.0,
  "total_units_sold": 450,
  "average_revenue_per_record": 2500.0,
  "average_revenue_per_unit": 277.78
}
```

*The values above are illustrative examples, not actual project results.*

### 3. Sales by Product

**Endpoint:** `GET /sales/by-product`

Returns total revenue and units sold for each product.

**Response fields:**

- `revenue_by_product`: Revenue grouped by product.
- `units_by_product`: Units sold grouped by product.

**Example response:**

```json
{
  "revenue_by_product": {
    "Laptop": 50000.0,
    "Phone": 35000.0
  },
  "units_by_product": {
    "Laptop": 20,
    "Phone": 35
  }
}
```

### 4. Sales by Region

**Endpoint:** `GET /sales/by-region`

Returns total revenue and units sold for each region.

**Response fields:**

- `revenue_by_region`: Revenue grouped by region.
- `units_by_region`: Units sold grouped by region.

### 5. Sales by Month

**Endpoint:** `GET /sales/by-month`

Returns total revenue and units sold for each monthly reporting period.

**Response fields:**

- `revenue_by_month`: Revenue grouped by month.
- `units_by_month`: Units sold grouped by month.

The monthly reporting period is derived from the sales date during data processing.

### 6. Top Product

**Endpoint:** `GET /sales/top-product`

Returns the product with the highest total revenue.

**Response field:**

- `top_product`: Name of the product with the highest aggregated revenue.

**Example response:**

```json
{
  "top_product": "Laptop"
}
```

*The product name is illustrative.*

## How to Test the Endpoints

Start the API from the project root:

```bash
uv run uvicorn insight_api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` in your browser.

Expand an endpoint, select **Try it out**, and click **Execute** to send a request and inspect the response.

You can also test an endpoint from the terminal:

```bash
curl http://127.0.0.1:8000/health
```

## Notes

- All six endpoints use the HTTP `GET` method.
- Responses are returned in JSON format.
- The API reads data from the processed Parquet file.
- The API currently exposes read-only analytics; it does not create or modify sales records.
- The API expects the processed data file to exist before analytics endpoints are called.