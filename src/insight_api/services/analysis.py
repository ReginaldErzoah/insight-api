def calculate_total_revenue(sales):
    """Calculate the total revenue from sales data"""
    return sales["revenue"].sum()

def calculate_total_units_sold(sales):
    """Calculate total units sold from sales data"""
    return sales["units_sold"].sum()