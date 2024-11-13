from db_setup.db_connect import db

def get_avg_order():
    try:
        with db.cursor() as mycursor:
            # Correct SQL for calculating average sales
            sql = "SELECT SUM(sub_total) / NULLIF(SUM(quantity), 0) FROM tbl_purchase_order"
            mycursor.execute(sql)
            result = mycursor.fetchone()

            # Check if result is not None
            sales_total = result[0] if result is not None and result[0] is not None else 0
    except Exception as e:
        print(f"Error fetching total sales: {e}")
        sales_total = None
    return sales_total
