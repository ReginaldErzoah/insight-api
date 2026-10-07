def calculate_total_revenue(sales):
    """Calculate the total revenue from sales data"""
    return sales["revenue"].sum()

def calculate_total_units_sold(sales):
    """Calculate total units sold from sales data"""
    return sales["units_sold"].sum()

def revenue_by_product(sales):
    """Calculate total revenue by product"""
    return sales.groupby("product")["revenue"].sum()

def revenue_by_region(sales):
    """Calculate tottal revenue by region"""
    return sales.groupby("region")["revenue"].sum()