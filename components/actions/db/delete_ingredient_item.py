from db_setup.db_connect import db, mycursor
from tkinter import messagebox

def delete_inventory_item(ingredient_name, display_inventory, *args):
    try:
        mycursor.execute("DELETE FROM tbl_product_ingredients WHERE ingredient_name = %s", (ingredient_name,))
        db.commit()
        messagebox.showinfo("Success", f"Successfully deleted {ingredient_name}.")

        # Refresh the display
        display_inventory(*args)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete {ingredient_name}: {e}")
