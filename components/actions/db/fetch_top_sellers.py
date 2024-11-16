from db_setup.db_connect import db

def get_top_selling_items():
    try:
        mycursor = db.cursor()
        query = """
        SELECT product_name, SUM(quantity) as sales_count
        FROM tbl_sales
        GROUP BY product_name
        ORDER BY sales_count DESC
        LIMIT 5;
        """
        mycursor.execute(query)
        top_selling_items = mycursor.fetchall()
    except Exception as e:
        print(f"Error fetching top selling items: {e}")
        top_selling_items = [] 
    finally:
        mycursor.close()
    
    return top_selling_items

# DALE - Details for top selling items
def get_top_selling_item_details(product_name):
    try:
        mycursor = db.cursor()
        query = """
            SELECT product_name, product_category, SUM(quantity) AS total_sales, unit_price, SUM(sub_total) AS total_revenue
            FROM tbl_sales
            WHERE product_name = %s
            GROUP BY product_name, product_category, unit_price
        """
        mycursor.execute(query, (product_name,))
        # Fetch details and store them in a structured way
        result = mycursor.fetchone()
        if result:
            product_details = {
                "product_name": result[0],
                "product_category": result[1],
                "total_sales": result[2],
                "unit_price": result[3],
                "total_revenue": result[4]
            }
        else:
            product_details = None
    except Exception as e:
        print(f"Error fetching product details for {product_name}: {e}")
        product_details = None
    finally:
        mycursor.close()
    
    return product_details
