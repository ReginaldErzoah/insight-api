
def total_revenue(sales):
    """Calculate the total revenue from sales data."""
    return sales["revenue"].sum()

def total_units_sold(sales):
    """Calculate total units sold from sales data."""
    return sales["units_sold"].sum()

def average_revenue_per_record(sales):
    """Calculate average revenue per sales record."""
    return sales["revenue"].mean()

def average_revenue_per_unit(sales):
    """Calculate average revenue per unit sold."""
    return sales["revenue"].sum()/sales["units_sold"].sum()


def revenue_by_product(sales):
    """Calculate total revenue by product."""
    return sales.groupby("product")["revenue"].sum()

def units_by_product(sales):
    """Calculate units sold by product."""
    return sales.groupby("product")["units_sold"].sum()

def top_product(sales):
    """Return the product with the highest total revenue."""
    revenue_by_product = sales.groupby("product")["revenue"].sum()
    return revenue_by_product.idxmax()


def revenue_by_region(sales):
    """Calculate total revenue by region."""
    return sales.groupby("region")["revenue"].sum()

def units_by_region(sales):
    """Calculate units sold by region."""
    return sales.groupby("region")["units_sold"].sum()


def revenue_by_month(sales):
    """Calculate total revenue per month year."""
    return sales.groupby("month_year")["revenue"].sum()

def units_by_month(sales):
    """Calculate total units sold per month year."""
    return sales.groupby("month_year")["units_sold"].sum()
