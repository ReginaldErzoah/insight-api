
import os

import pandas as pd
import requests
import streamlit as st


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

REQUEST_TIMEOUT = 10


# --------------------------------------------------
# 2. Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="InsightAPI | Sales Dashboard",

    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# 3. API communication
# --------------------------------------------------

def get_api_data(endpoint):
    """Fetch JSON data from a FastAPI endpoint."""
    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json(), None

    except requests.RequestException as error:
        return None, str(error)

    except ValueError as error:
        return None, f"Invalid JSON response: {error}"


def check_api_health():
    """Check whether the backend is responding."""
    data, error = get_api_data("/health")

    if error:
        return False, error

    if not isinstance(data, dict):
        return False, "The API returned an unexpected health response."

    if data.get("status") != "healthy":
        return False, "The API health check did not report healthy status."

    return True, None


# --------------------------------------------------
# 4. Data preparation
# --------------------------------------------------

def series_to_dataframe(data, category_name, value_name):
    """Convert an API dictionary into a chart-ready DataFrame."""
    if not isinstance(data, dict) or not data:
        return pd.DataFrame(columns=[category_name, value_name])

    frame = pd.DataFrame(
        list(data.items()),
        columns=[category_name, value_name],
    )

    frame[value_name] = pd.to_numeric(
        frame[value_name],
        errors="coerce",
    )

    frame = frame.dropna(subset=[value_name])

    return frame.sort_values(
        value_name,
        ascending=False,
    ).reset_index(drop=True)


def show_metric(label, value, help_text=None):
    """Display a consistently formatted KPI."""
    st.metric(
        label=label,
        value=value,
        help=help_text,
    )


# --------------------------------------------------
# 5. Sidebar
# --------------------------------------------------

with st.sidebar:
    st.title("InsightAPI")
    st.caption("Sales analytics platform")

    st.divider()

    st.subheader("Backend status")

    api_is_healthy, health_error = check_api_health()

    if api_is_healthy:
        st.success("API connected")
    else:
        st.error("API unavailable")
        st.caption(
            "Start FastAPI and refresh this page to reconnect."
        )
        with st.expander("Connection details"):
            st.code(health_error or "Unknown connection error")

    st.divider()


    refresh_clicked = st.button(
        "Refresh dashboard",
        use_container_width=True,
    )


if refresh_clicked:
    st.rerun()


# --------------------------------------------------
# 6. Page header
# --------------------------------------------------

st.title("Sales Performance Dashboard")

st.markdown(
    """
    Explore revenue, sales volume, product performance,
    regional performance, and monthly trends using data
    supplied by the InsightAPI backend.
    """
)

st.caption("Data source: FastAPI sales analytics endpoints")


if not api_is_healthy:
    st.error(
        "The dashboard cannot retrieve live data because "
        "the backend health check failed."
    )
    st.info(
        "In another terminal, start the API with: "
        "`uv run uvicorn insight_api.main:app --reload`"
    )
    st.stop()


# --------------------------------------------------
# 7. Retrieve data from the API
# --------------------------------------------------

summary, summary_error = get_api_data("/sales/summary")

products, products_error = get_api_data("/sales/by-product")

regions, regions_error = get_api_data("/sales/by-region")

monthly, monthly_error = get_api_data("/sales/by-month")

top_product_data, top_product_error = get_api_data(
    "/sales/top-product"
)


endpoint_errors = {
    "Sales summary": summary_error,
    "Product analysis": products_error,
    "Regional analysis": regions_error,
    "Monthly analysis": monthly_error,
    "Top product": top_product_error,
}

for endpoint_name, error in endpoint_errors.items():
    if error:
        st.warning(
            f"{endpoint_name} could not be loaded: {error}"
        )


# --------------------------------------------------
# 8. Validate response structures
# --------------------------------------------------

if summary is not None and not isinstance(summary, dict):
    st.warning("The summary endpoint returned an unexpected response.")
    summary = None

if products is not None and not isinstance(products, dict):
    st.warning("The product endpoint returned an unexpected response.")
    products = None

if regions is not None and not isinstance(regions, dict):
    st.warning("The regional endpoint returned an unexpected response.")
    regions = None

if monthly is not None and not isinstance(monthly, dict):
    st.warning("The monthly endpoint returned an unexpected response.")
    monthly = None

if (
    top_product_data is not None
    and not isinstance(top_product_data, dict)
):
    st.warning("The top-product endpoint returned an unexpected response.")
    top_product_data = None


if summary is None and products is None and regions is None and monthly is None:
    st.error(
        "No sales data could be loaded. Check the API logs "
        "and try refreshing the dashboard."
    )
    st.stop()


# --------------------------------------------------
# 9. Prepare chart data
# --------------------------------------------------

revenue_by_product = pd.DataFrame(
    columns=["Product", "Revenue"]
)
units_by_product = pd.DataFrame(
    columns=["Product", "Units Sold"]
)
revenue_by_region = pd.DataFrame(
    columns=["Region", "Revenue"]
)
units_by_region = pd.DataFrame(
    columns=["Region", "Units Sold"]
)
revenue_by_month = pd.DataFrame(
    columns=["Month", "Revenue"]
)
units_by_month = pd.DataFrame(
    columns=["Month", "Units Sold"]
)


if products is not None:
    revenue_by_product = series_to_dataframe(
        products.get("revenue_by_product", {}),
        "Product",
        "Revenue",
    )

    units_by_product = series_to_dataframe(
        products.get("units_by_product", {}),
        "Product",
        "Units Sold",
    )


if regions is not None:
    revenue_by_region = series_to_dataframe(
        regions.get("revenue_by_region", {}),
        "Region",
        "Revenue",
    )

    units_by_region = series_to_dataframe(
        regions.get("units_by_region", {}),
        "Region",
        "Units Sold",
    )


if monthly is not None:
    revenue_by_month = series_to_dataframe(
        monthly.get("revenue_by_month", {}),
        "Month",
        "Revenue",
    )

    units_by_month = series_to_dataframe(
        monthly.get("units_by_month", {}),
        "Month",
        "Units Sold",
    )

    # Months should be displayed chronologically.
    revenue_by_month = revenue_by_month.sort_values("Month")
    units_by_month = units_by_month.sort_values("Month")


# --------------------------------------------------
# 10. KPI cards
# --------------------------------------------------

st.subheader("Business overview")

if summary is not None:
    metric_columns = st.columns(4)

    with metric_columns[0]:
        show_metric(
            "Total revenue",
            f"{float(summary['total_revenue']):,.2f}",
            "Sum of revenue across the available sales records.",
        )

    with metric_columns[1]:
        show_metric(
            "Units sold",
            f"{int(summary['total_units_sold']):,}",
            "Total units sold across the available records.",
        )

    with metric_columns[2]:
        show_metric(
            "Average revenue per record",
            f"{float(summary['average_revenue_per_record']):,.2f}",
            "Average revenue for each sales record.",
        )

    with metric_columns[3]:
        show_metric(
            "Average revenue per unit",
            f"{float(summary['average_revenue_per_unit']):,.2f}",
            "Total revenue divided by total units sold.",
        )
else:
    st.info("Business overview metrics are currently unavailable.")


if top_product_data is not None:
    best_product = top_product_data.get("top_product")

    if best_product is not None:
        st.success(f"Top product by revenue: **{best_product}**")


st.divider()


# --------------------------------------------------
# 11. Interactive analysis tabs
# --------------------------------------------------

overview_tab, product_tab, region_tab, monthly_tab, data_tab = st.tabs(
    [
        "Overview",
        "Products",
        "Regions",
        "Monthly trends",
        "Data explorer",
    ]
)


# --------------------------------------------------
# 12. Overview tab
# --------------------------------------------------

with overview_tab:
    st.subheader("Sales performance at a glance")

    chart_column, region_column = st.columns(2)

    with chart_column:
        st.markdown("#### Revenue by product")

        if not revenue_by_product.empty:
            chart_data = revenue_by_product.set_index("Product")
            st.bar_chart(
                chart_data,
                y="Revenue",
            )
        else:
            st.info("Product revenue data is unavailable.")

    with region_column:
        st.markdown("#### Revenue by region")

        if not revenue_by_region.empty:
            chart_data = revenue_by_region.set_index("Region")
            st.bar_chart(
                chart_data,
                y="Revenue",
            )
        else:
            st.info("Regional revenue data is unavailable.")

    st.markdown("#### Monthly revenue trend")

    if not revenue_by_month.empty:
        chart_data = revenue_by_month.set_index("Month")
        st.line_chart(
            chart_data,
            y="Revenue",
        )
    else:
        st.info("Monthly revenue data is unavailable.")


# --------------------------------------------------
# 13. Products tab
# --------------------------------------------------

with product_tab:
    st.subheader("Product performance")

    product_chart_column, product_units_column = st.columns(2)

    with product_chart_column:
        st.markdown("#### Revenue by product")

        if not revenue_by_product.empty:
            st.bar_chart(
                revenue_by_product.set_index("Product"),
                y="Revenue",
            )
        else:
            st.info("No product revenue data is available.")

    with product_units_column:
        st.markdown("#### Units sold by product")

        if not units_by_product.empty:
            st.bar_chart(
                units_by_product.set_index("Product"),
                y="Units Sold",
            )
        else:
            st.info("No product unit data is available.")

    if not revenue_by_product.empty:
        st.markdown("#### Product revenue ranking")

        st.dataframe(
            revenue_by_product,
            hide_index=True,
            use_container_width=True,
        )


# --------------------------------------------------
# 14. Regions tab
# --------------------------------------------------

with region_tab:
    st.subheader("Regional performance")

    region_revenue_column, region_units_column = st.columns(2)

    with region_revenue_column:
        st.markdown("#### Revenue by region")

        if not revenue_by_region.empty:
            st.bar_chart(
                revenue_by_region.set_index("Region"),
                y="Revenue",
            )
        else:
            st.info("No regional revenue data is available.")

    with region_units_column:
        st.markdown("#### Units sold by region")

        if not units_by_region.empty:
            st.bar_chart(
                units_by_region.set_index("Region"),
                y="Units Sold",
            )
        else:
            st.info("No regional unit data is available.")

    if not revenue_by_region.empty:
        st.markdown("#### Regional revenue ranking")

        st.dataframe(
            revenue_by_region,
            hide_index=True,
            use_container_width=True,
        )


# --------------------------------------------------
# 15. Monthly trends tab
# --------------------------------------------------

with monthly_tab:
    st.subheader("Monthly sales trends")

    monthly_revenue_column, monthly_units_column = st.columns(2)

    with monthly_revenue_column:
        st.markdown("#### Revenue by month")

        if not revenue_by_month.empty:
            st.line_chart(
                revenue_by_month.set_index("Month"),
                y="Revenue",
            )
        else:
            st.info("No monthly revenue data is available.")

    with monthly_units_column:
        st.markdown("#### Units sold by month")

        if not units_by_month.empty:
            st.line_chart(
                units_by_month.set_index("Month"),
                y="Units Sold",
            )
        else:
            st.info("No monthly unit data is available.")

    if not revenue_by_month.empty:
        st.markdown("#### Monthly revenue records")

        st.dataframe(
            revenue_by_month,
            hide_index=True,
            use_container_width=True,
        )


# --------------------------------------------------
# 16. Data explorer tab
# --------------------------------------------------

with data_tab:
    st.subheader("Explore aggregated sales data")

    dataset_choice = st.selectbox(
        "Choose a dataset",
        [
            "Revenue by product",
            "Units by product",
            "Revenue by region",
            "Units by region",
            "Revenue by month",
            "Units by month",
        ],
    )

    datasets = {
        "Revenue by product": revenue_by_product,
        "Units by product": units_by_product,
        "Revenue by region": revenue_by_region,
        "Units by region": units_by_region,
        "Revenue by month": revenue_by_month,
        "Units by month": units_by_month,
    }

    selected_data = datasets[dataset_choice]

    if selected_data.empty:
        st.info("No data is available for this selection.")
    else:
        st.dataframe(
            selected_data,
            hide_index=True,
            use_container_width=True,
        )

        csv_data = selected_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download this table as CSV",
            data=csv_data,
            file_name=(
                dataset_choice.lower().replace(" ", "_") + ".csv"
            ),
            mime="text/csv",
        )


# --------------------------------------------------
# 17. Footer
# --------------------------------------------------

st.divider()

st.caption(
    "InsightAPI | Sales analytics powered by FastAPI and Streamlit"
)