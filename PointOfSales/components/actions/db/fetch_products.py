from db_setup.db_connect import db



def get_all_products():
      

      try:
            mycursor = db.cursor()
            
            sql = "SELECT product_name, product_category, product_price, product_status FROM tbl_products"
            
            
            mycursor.execute(sql)
            products_display = mycursor.fetchall()
      
      except Exception as e:
            print(f"Error fetching all product: {e}")
            products_display = []
      finally:
            mycursor.close()
            
      return products_display      
      