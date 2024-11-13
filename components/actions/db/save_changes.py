from db_setup.db_connect import db




def save_product_changes(old_product_name, new_product_name, new_price, new_category, modal):
    """Save changes made to a product."""
    try:
        mycursor = db.cursor()

        # Check if the old product name exists
        mycursor.execute("SELECT unit_name FROM tbl_product_unit WHERE unit_name = %s", (old_product_name,))
        result = mycursor.fetchone()
        if result is None:
            print(f"Error: The product name '{old_product_name}' does not exist in tbl_product_unit.")
            return

        # Check if the new product name exists
        mycursor.execute("SELECT unit_name FROM tbl_product_unit WHERE unit_name = %s", (new_product_name,))
        result = mycursor.fetchone()
        if result is None:
            # Update both tables within a transaction
            sql_update_product_unit = """
                UPDATE tbl_product_unit
                SET unit_name = %s
                WHERE unit_name = %s
            """
            mycursor.execute(sql_update_product_unit, (new_product_name, old_product_name))

            sql_update_products = """
                UPDATE tbl_products
                SET product_name = %s, product_price = %s, product_category = %s
                WHERE product_name = %s
            """
            mycursor.execute(sql_update_products, (new_product_name, new_price, new_category, old_product_name))

            db.commit()
            modal.destroy()
        else:
            print(f"Error: The product name '{new_product_name}' already exists.")
            return

    except Exception as e:
        print(f"Error saving product changes: {e}")
        db.rollback()

    finally:
        mycursor.close()


def update_unit_product_name(old_product_name, new_product_name):
    """Update the product name in the related unit table."""
    try:
        mycursor = db.cursor()


        if old_product_name != new_product_name:
            sql_update_unit = """
                UPDATE tbl_product_unit 
                SET unit_name = %s 
                WHERE unit_name = %s
            """
            mycursor.execute(sql_update_unit, (new_product_name, old_product_name))

        db.commit()

    except Exception as e:
        print(f"Error updating product unit name: {e}")

    finally:
        mycursor.close()
