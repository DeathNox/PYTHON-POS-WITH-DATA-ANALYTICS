import customtkinter as ctk
import tkinter as tk 

class Modal_Add_Ingredient_Display:
 
 
    def __init__(self, refresh_callback):
        self.refresh_callback = refresh_callback
 
    def modal_add_inventory(self):
        
        
        from main import CenterWindowToDisplay
                  
        self.modal = ctk.CTkToplevel()
        self.modal.title(f"Add Ingredient")
        self.modal.geometry(CenterWindowToDisplay(self.modal, 520, 480, self.modal._get_window_scaling()))
        self.modal.resizable(False, False)
        self.modal.configure(fg_color="#30211E")

        container = ctk.CTkFrame(self.modal, fg_color="#EBE0D6")
        container.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="nsew")

        self.modal.grid_rowconfigure(0, weight=1)
        self.modal.grid_columnconfigure(0, weight=1)

        modal_lbl = ctk.CTkLabel(
            container,
            text="Add Ingredient",
            text_color="#1E1E1E",
            font=("Inter", 26, "bold")
        )
        modal_lbl.grid(row=0, column=0, pady=(20, 10), padx=(30, 10), sticky='w')

        # Ingredient Name
        form_ingredient_name_lbl = ctk.CTkLabel(
            container,
            text="Ingredient name",
            text_color="#1E1E1E",
            font=("Inter", 20, "bold")
        )
        form_ingredient_name_lbl.grid(row=1, column=0, pady=(20, 10), padx=(30, 0), sticky='w')
      
        # Ingredient Name - Text Box
        self.form_ingredient_name_entry = ctk.CTkEntry(
            container,
            text_color="#372724",
            fg_color="#F5F5F5",
            font=("Inter", 18),
            width=430,
            height=30,
            corner_radius=3,
            border_width=1  
        )
        self.form_ingredient_name_entry.grid(row=2, column=0, pady=(5, 0), padx=(30, 0), sticky='w')

        # Form Container for Associated Prod and Ingredient Category
        form_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
        form_container.grid(row=3, column=0, pady=(20, 10), padx=(15, 15), sticky="nsew")
        
        # Associated Product Dropdown - Label 
        form_associated_product_lbl = ctk.CTkLabel(
            form_container,
            text_color="#1E1E1E",
            font=("Inter", 20, "bold"),
            text="Associated product"
        )
        form_associated_product_lbl.grid(row=0, column=0, pady=(0, 5), padx=(15, 10), sticky='w')
      
        # Associated Product Dropdown - ComboBox
        self.associated_products = self.get_products() 
        self.form_associated_product_combobox = ctk.CTkComboBox(
            form_container,
            values=self.associated_products,
            font=("Inter", 16),
            fg_color="#F5F5F5",
            text_color="#372724",
            width=200,
            state="readonly",
            cursor="hand2",
            border_width=1,
            corner_radius=3
        )
        self.form_associated_product_combobox.grid(row=1, column=0, pady=(5, 0), padx=(15, 5), sticky='w')
        self.form_associated_product_combobox.set("Select a product")
        
        # Ingredient Category Dropdown - Label
        form_ingredient_category_lbl = ctk.CTkLabel(
            form_container,
            text_color="#1E1E1E",
            font=("Inter", 20, "bold"),
            text="Category"
        )
        form_ingredient_category_lbl.grid(row=0, column=1, pady=(0, 5), padx=(30, 0), sticky='w')  
        
        # Ingredient Category Dropdown - ComboBox
        ingredient_category = ['Toppings', 'Base Liquids', 'Additives', 'Coffee Base']
        
        self.form_ingredient_category_combobox = ctk.CTkComboBox(
            form_container,
            values=ingredient_category,
            font=("Inter", 16),
            fg_color="#F5F5F5",
            text_color="#372724",
            width=200,
            state="readonly",
            cursor="hand2",
            border_width=1,
            corner_radius=3
        )
        self.form_ingredient_category_combobox.grid(row=1, column=1, pady=(5, 0), padx=(30, 0), sticky='w')  
        self.form_ingredient_category_combobox.set("Select a category")
        
        form_ingredient_availability_lbl = ctk.CTkLabel(
            form_container,
            text_color="#1E1E1E",
            font=("Inter", 20, "bold"),
            text="Availability"
        )
        
        ingredient_availability = ['In Stock', 'Low Stock', 'Out of Stock']
        
        form_ingredient_availability_lbl.grid(row=2, column=0, pady=(20, 0), padx=(13, 0), sticky='w')
        
        self.form_ingredient_availability_combobox = ctk.CTkComboBox(
            form_container,
            values=ingredient_availability,
            font=("Inter", 16),
            fg_color="#F5F5F5",
            text_color="#372724",
            width=200,
            state="readonly",
            cursor="hand2",
            border_width=1,
            corner_radius=3
        )
        
        self.form_ingredient_availability_combobox.grid(row=3, column=0, pady=(15, 0), padx=(13, 0), sticky='w')  
        self.form_ingredient_availability_combobox.set("Set status")
        
        # Button container
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
            command=self.save_ingredients
        )

        save_btn.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="e")

    def get_products(self):
        from db_setup.db_connect import db

        if not db.is_connected():
            db.reconnect()

        mycursor = db.cursor()
        mycursor.execute("SELECT product_name FROM tbl_products WHERE product_status = 'Available'") 
        products = mycursor.fetchall()
        mycursor.close()
        
        return [product[0] for product in products]

    def save_ingredients(self):
        from db_setup.db_connect import db
        
        # Get user input values
        ingredient_name = self.form_ingredient_name_entry.get()
        associated_product = self.form_associated_product_combobox.get()
        ingredient_category = self.form_ingredient_category_combobox.get()
        ingredient_availability = self.form_ingredient_availability_combobox.get()

        # Check for required field inputs
        if not ingredient_name or associated_product == "Select a product" or ingredient_category == "Select a category":
            ctk.messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Fetch product_id from associated product name
        if not db.is_connected():
            db.reconnect()
        mycursor = db.cursor()
        
        mycursor.execute("SELECT product_id FROM tbl_products WHERE product_name = %s", (associated_product,))
        product_result = mycursor.fetchone()
        
        if product_result:
            product_id = product_result[0]
            
            # Insert ingredient into tbl_product_ingredients
            try:
                mycursor.execute(
                    """
                    INSERT INTO tbl_product_ingredients 
                    (product_id, ingredient_name, ingredient_category, status) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (product_id, ingredient_name, ingredient_category, ingredient_availability)
                )
                db.commit()
                tk.messagebox.showinfo("Success", "Ingredient added successfully.")
                self.modal.destroy()
                self.refresh_callback() 
                
            except Exception as e:
                db.rollback()
                tk.messagebox.showerror("Error", f"Failed to add ingredient: {str(e)}")
            finally:
                mycursor.close()
