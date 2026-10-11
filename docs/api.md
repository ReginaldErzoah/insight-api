# API Reference

Insight API is a REST API built with FastAPI that provides sales analytics from processed sales data. It exposes read-only endpoints that return sales performance metrics in JSON format.

## Base URLs

### Local development

When running the API locally:

```text
http://127.0.0.1:8000
```

### Production

The deployed API is available at:

- **API base URL:** https://insight-api-vk5ztwb7gq-bq.a.run.app
- **Interactive API documentation:** https://insight-api-vk5ztwb7gq-bq.a.run.app/docs
- **Health check:** https://insight-api-vk5ztwb7gq-bq.a.run.app/health

The production API is deployed on Google Cloud Run.

## Endpoints

All six endpoints use the HTTP `GET` method.

### 1. Health Check

**Endpoint:** `GET /health`

Checks whether the API is responding.

**Example response:**

```json
{
  "status": "healthy"
}
```

**Try it:** [Production health check](https://insight-api-vk5ztwb7gq-bq.a.run.app/health)

### 2. Sales Summary

**Endpoint:** `GET /sales/summary`

Returns the main sales performance metrics across the available sales records.

**Response fields:**

| Field | Description |
|---|---|
| `total_revenue` | Total revenue across all sales records |
| `total_units_sold` | Total units sold |
| `average_revenue_per_record` | Average revenue per sales record |
| `average_revenue_per_unit` | Total revenue divided by total units sold |

**Example response from the deployed API:**

```json
{
  "total_revenue": 358400.0,
  "total_units_sold": 474,
  "average_revenue_per_record": 7314.285714285715,
  "average_revenue_per_unit": 756.1181434599156
}
```

These values reflect the dataset currently used by the deployed API.

**Try it:** [Sales summary](https://insight-api-vk5ztwb7gq-bq.a.run.app/sales/summary)

### 3. Sales by Product

**Endpoint:** `GET /sales/by-product`

Returns aggregated revenue and units sold for each product.

**Response fields:**

- `revenue_by_product`: Revenue grouped by product.
- `units_by_product`: Units sold grouped by product.

**Illustrative response:**

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

The product names and values above are illustrative.

### 4. Sales by Region

**Endpoint:** `GET /sales/by-region`

Returns aggregated revenue and units sold for each region.

**Response fields:**

- `revenue_by_region`: Revenue grouped by region.
- `units_by_region`: Units sold grouped by region.

The response contains the aggregated results for the regions represented in the processed dataset.

### 5. Sales by Month

**Endpoint:** `GET /sales/by-month`

Returns aggregated revenue and units sold for each monthly reporting period.

**Response fields:**

- `revenue_by_month`: Revenue grouped by month.
- `units_by_month`: Units sold grouped by month.

The monthly reporting period is derived from the sales date during data processing.

### 6. Top Product

**Endpoint:** `GET /sales/top-product`

Returns the product with the highest total revenue.

**Response field:**

- `top_product`: The name of the product with the highest aggregated revenue.

**Illustrative response:**

```json
{
  "top_product": "Laptop"
}
```

The product name above is illustrative.

## How to Test the Endpoints

### Option 1: Interactive API documentation

FastAPI automatically generates interactive API documentation.

1. Open the [production API documentation](https://insight-api-vk5ztwb7gq-bq.a.run.app/docs), or start the API locally and visit `http://127.0.0.1:8000/docs`.
2. Expand the endpoint you want to test.
3. Select **Try it out**.
4. Select **Execute**.
5. Inspect the HTTP status code and JSON response.

### Option 2: Using curl

To test the local API, first start it from the project root:

```bash
uv run uvicorn insight_api.main:app --reload
```

Then open another terminal and run:

```bash
curl http://127.0.0.1:8000/health
```

To test the sales summary:

```bash
curl http://127.0.0.1:8000/sales/summary
```

To test the deployed API instead:

```bash
curl https://insight-api-vk5ztwb7gq-bq.a.run.app/health
```

```bash
curl https://insight-api-vk5ztwb7gq-bq.a.run.app/sales/summary
```

### Option 3: Using a browser

You can open the production health check and sales summary endpoints directly in your browser. Because these endpoints use `GET`, no request body is required.

## How the API Works

At a high level, the API follows this flow:

1. **Data processing:** The raw sales data is processed and saved as a Parquet file.
2. **Data access:** The data access layer loads the processed data.
3. **Business logic:** The analytics service calculates the requested metrics.
4. **API routes:** FastAPI exposes the analytics through HTTP endpoints.
5. **JSON response:** The API returns the results to clients, including the Streamlit dashboard.

The API reads from the processed dataset rather than accepting sales records for creation or modification.

## Notes and Limitations

- All six endpoints use the HTTP `GET` method.
- Successful analytics responses are returned in JSON format.
- Analytics depend on the processed Parquet file being available and readable.
- The API currently provides read-only sales analytics.
- The API's health check confirms that the health endpoint responds; it does not necessarily verify that the processed dataset is available or that every analytics endpoint is working.
- The examples marked illustrative are not guaranteed to match the current dataset.
- The deployed API runs on Google Cloud Run, which can incur charges depending on usage and associated cloud resources.
