from db_setup.db_connect import db

def update_ingredient_status(ingredient_name, new_status):
    
    try:
        mycursor = db.cursor()
        sql = "UPDATE tbl_product_ingredients SET status = %s WHERE ingredient_name = %s"
        mycursor.execute(sql, (new_status, ingredient_name))
        db.commit()  
    except Exception as e:
        print(f"Error updating ingredient status: {e}")
    finally:
        mycursor.close()