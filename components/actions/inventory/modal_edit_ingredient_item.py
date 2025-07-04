
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class IngredientManager:
    
    def __init__(self):
       pass 
   
   
    def edit_ingredient_item(self, ingredient_name, display_inventory, inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category):
        try:
            # fetch ingredient_id 
            ingredient_id = self.get_ingredient_id_by_name(ingredient_name)
            if not ingredient_id:
                messagebox.showerror("Error", "Ingredient not found!")
                return

            # Modal Display 
            from main import CenterWindowToDisplay
            
            self.modal = ctk.CTkToplevel()
            self.modal.title("Edit Ingredient")
            self.modal.geometry(CenterWindowToDisplay(self.modal, 520, 480, self.modal._get_window_scaling()))
            self.modal.resizable(False, False)
            self.modal.configure(fg_color="#30211E")
            
            container = ctk.CTkFrame(self.modal, fg_color="#EBE0D6")
            container.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="nsew")
            
            self.modal.grid_rowconfigure(0, weight=1)
            self.modal.grid_columnconfigure(0, weight=1)
            
            # Modal label
            modal_lbl = ctk.CTkLabel(
                container,
                text="Edit Ingredient",
                text_color="#1E1E1E",
                font=("Inter", 26, "bold")
            )
            modal_lbl.grid(row=0, column=0, pady=(20, 10), padx=(30, 10), sticky='w')

            # Ingredient Name
            ingredient_name_label = ctk.CTkLabel(
                container,
                text="Ingredient Name",
                text_color="#1E1E1E",
                font=("Inter", 20, "bold")
            )
            ingredient_name_label.grid(row=1, column=0, padx=(30, 10), pady=(10, 5), sticky="w")
            
            # Ingredient Name - Text Box
            ingredient_name_entry = ctk.CTkEntry(
                container,
                text_color="#372724",
                fg_color="#F5F5F5",
                font=("Inter", 18),
                width=430,
                height=30,
                corner_radius=3,
                border_width=1
            )
            ingredient_name_entry.insert(0, ingredient_name)  # Populate with the existing ingredient name
            ingredient_name_entry.grid(row=2, column=0, padx=(30, 10), pady=(5, 10), sticky="w")

            # Form Container for Associated Product and Ingredient Category
            form_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
            form_container.grid(row=3, column=0, pady=(20, 10), padx=(15, 15), sticky="nsew")
            
            # Associated Product Dropdown - Label 
            form_associated_product_lbl = ctk.CTkLabel(
                form_container,
                text_color="#1E1E1E",
                font=("Inter", 20, "bold"),
                text="Associated Product"
            )
            form_associated_product_lbl.grid(row=0, column=0, pady=(0, 5), padx=(15, 10), sticky='w')
            
            # Associated Product Dropdown - ComboBox
            associated_products = self.get_products()  # This function needs to be defined or imported
            product_combobox = ctk.CTkComboBox(
                form_container,
                values=associated_products,
                font=("Inter", 16),
                fg_color="#F5F5F5",
                text_color="#372724",
                width=200,
                state="readonly",
                cursor="hand2",
                border_width=1,
                corner_radius=3
            )
            product_combobox.set("Select a product")
            product_combobox.grid(row=1, column=0, pady=(5, 0), padx=(15, 5), sticky='w')

            # Ingredient Category Dropdown - Label
            form_ingredient_category_lbl = ctk.CTkLabel(
                form_container,
                text_color="#1E1E1E",
                font=("Inter", 20, "bold"),
                text="Category"
            )
            form_ingredient_category_lbl.grid(row=0, column=1, pady=(0, 5), padx=(30, 0), sticky='w')
            
            # Ingredient Category Dropdown - ComboBox
            category_combobox = ctk.CTkComboBox(
                form_container,
                values=['Toppings', 'Base Liquids', 'Additives', 'Coffee Base'],
                font=("Inter", 16),
                fg_color="#F5F5F5",
                text_color="#372724",
                width=200,
                state="readonly",
                cursor="hand2",
                border_width=1,
                corner_radius=3
            )
            category_combobox.set("Select a category")
            category_combobox.grid(row=1, column=1, pady=(5, 0), padx=(30, 0), sticky='w')

            # Ingredient Availability Dropdown - Label
            form_ingredient_availability_lbl = ctk.CTkLabel(
                form_container,
                text_color="#1E1E1E",
                font=("Inter", 20, "bold"),
                text="Availability"
            )
            form_ingredient_availability_lbl.grid(row=2, column=0, pady=(20, 0), padx=(13, 0), sticky='w')
            
            # Ingredient Availability Dropdown - ComboBox
            availability_combobox = ctk.CTkComboBox(
                form_container,
                values=['In Stock', 'Low Stock', 'Out of Stock'],
                font=("Inter", 16),
                fg_color="#F5F5F5",
                text_color="#372724",
                width=200,
                state="readonly",
                cursor="hand2",
                border_width=1,
                corner_radius=3
            )
            availability_combobox.set("Set status")
            availability_combobox.grid(row=3, column=0, pady=(15, 0), padx=(13, 0), sticky='w')

            # Button Container
            button_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
            button_container.grid(row=5, column=0, columnspan=2, padx=(30, 0), pady=(50, 10), sticky="ew")
            
            button_container.grid_columnconfigure(0, weight=1)  
            
            # Cancel Button
            cancel_btn = ctk.CTkButton(
                button_container,
                text="Cancel",
                command=self.modal.destroy,
                font=("Inter", 20, "bold"),
                width=100,
                fg_color="#F5F5F5",
                text_color="#2C2C2C"
            )
            cancel_btn.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="e")
            
            # Save Button
            save_btn = ctk.CTkButton(
                button_container,
                text="Save",
                font=("Inter", 20, "bold"),
                width=100,
                fg_color="#5482C7",
                text_color="#F5F5F5",
                command=lambda: self.save_ingredient_changes(
                    ingredient_id, 
                    ingredient_name_entry.get(), 
                    product_combobox.get(), 
                    category_combobox.get(), 
                    availability_combobox.get()
                )
            )
            save_btn.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="e")
            
        except Exception as e:
            print(f"Error: {e}")


    def save_ingredient_changes(self, ingredient_id, ingredient_name, associated_product, ingredient_category, ingredient_availability):
        from db_setup.db_connect import db
        
        if not db.is_connected():
            db.reconnect()

        mycursor = db.cursor()

        mycursor.execute("SELECT product_id FROM tbl_products WHERE product_name = %s", (associated_product,))
        product_result = mycursor.fetchone()

        if product_result:
            product_id = product_result[0]

            mycursor.execute("""
                SELECT ingredient_name, ingredient_category, status 
                FROM tbl_product_ingredients 
                WHERE ingredient_id = %s
            """, (ingredient_id,))
            current_values = mycursor.fetchone()

            if current_values:
                current_ingredient_name, current_category, current_status = current_values

                if (current_ingredient_name == ingredient_name and 
                    current_category == ingredient_category and 
                    current_status == ingredient_availability):
                    messagebox.showwarning("No Changes", "The ingredient is already up to date.")
                    self.modal.destroy()
                    return

                # if yung availability is still "Set status", keep the current status
                if ingredient_availability == "Set status":
                    ingredient_availability = current_status 

                try:
                    mycursor.execute("""
                        UPDATE tbl_product_ingredients 
                        SET ingredient_name = %s, ingredient_category = %s, status = %s 
                        WHERE ingredient_id = %s
                    """, (ingredient_name, ingredient_category, ingredient_availability, ingredient_id))
                    db.commit()

                    if mycursor.rowcount > 0:
                        messagebox.showinfo("Success", "Ingredient updated successfully.")
                    else:
                        messagebox.showwarning("No Changes", "No changes were made to the ingredient.")

                    self.modal.destroy()
                except Exception as e:
                    db.rollback()
                    messagebox.showerror("Error", f"Failed to update ingredient: {str(e)}")
                finally:
                    mycursor.close()
            else:
                messagebox.showerror("Error", "Ingredient not found in the database.")
        else:
            messagebox.showerror("Error", "Product not found in the database.")



    def get_products(self):
        from db_setup.db_connect import db

        if not db.is_connected():
            db.reconnect()

        mycursor = db.cursor()
        mycursor.execute("SELECT product_name FROM tbl_products WHERE product_status = 'Available'")
        products = [row[0] for row in mycursor.fetchall()]
        mycursor.close()

        return products

    def get_ingredient_id_by_name(self, ingredient_name):
        from db_setup.db_connect import db
        
        if not db.is_connected():
            db.reconnect()

        mycursor = db.cursor()
        mycursor.execute("SELECT ingredient_id FROM tbl_product_ingredients WHERE ingredient_name = %s", (ingredient_name,))
        result = mycursor.fetchone()
        mycursor.close()

        if result:
            return result[0]
        return None