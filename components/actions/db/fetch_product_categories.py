from db_setup.db_connect import db



def get_product_categories():
      
      try:
            mycursor = db.cursor()
            query = """
            
            SELECT category_id, category_name FROM 
            tbl_product_category
            
            
            """
            mycursor.execute(query)
            product_categories = mycursor.fetchall()
      
      except Exception as e:
            print(f"Error fetching product categories: {e}")
            product_categories = []
      
      finally:
            mycursor.close()
            
      return product_categories      
      
      
      