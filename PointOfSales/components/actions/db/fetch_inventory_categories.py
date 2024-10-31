from db_setup.db_connect import db

def fetch_inventory_by_category(category):
    try:
        mycursor = db.cursor()
        
        sql = """
        SELECT ingredient_name, ingredient_category, status
        FROM tbl_product_ingredients
        WHERE ingredient_category = %s
        """
        
        mycursor.execute(sql, (category,))
        item_inventory_by_category = mycursor.fetchall()
        
    except Exception as e:
        print(f"Error fetching inventory categories: {e}")
        item_inventory_by_category = []  # Return empty list in case of error
    
    finally:
        mycursor.close()
    
    return item_inventory_by_category
