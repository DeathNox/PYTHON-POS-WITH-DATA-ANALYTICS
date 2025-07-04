import customtkinter as ctk
from PIL import Image
import mysql.connector

from main import CenterWindowToDisplay
from components.actions.machine_learn.suggest_prod.based_off_inventory.generate_new_product import load_data_ing
from db_setup.db_connect import db 

class Modal_Add_Generate_Product:
    def __init__(self):
          
          
        # Load the data (products, ingredients)
        self.products_df, self.ingredients_df = load_data_ing()
        self.selected_ingredients = []  

       
        self.categories = self.get_product_categories()

    def modal_add_generated_product(self, ingredients):
        # For debugging
        print(f"Columns in ingredients_df: {self.ingredients_df.columns}")

        ingredient_names = self.ingredients_df[self.ingredients_df['ingredient_name'].isin(ingredients)]['ingredient_name'].tolist()

        # Modal initialization
        self.modal = ctk.CTkToplevel()
        self.modal.title("Selected Generated Product")
        self.modal.geometry(CenterWindowToDisplay(self.modal, 500, 625, self.modal._get_window_scaling()))
        self.modal.resizable(False, False)
        self.modal.configure(fg_color="#30211E")

        container = ctk.CTkFrame(self.modal, fg_color="#EBE0D6")
        container.pack(fill="both", expand=True, padx=15, pady=15)

        # Modal label
        modal_lbl = ctk.CTkLabel(
            container,
            text="Recommended Product Preview",
            text_color="#1E1E1E",
            font=("Inter", 26, "bold")
        )
        modal_lbl.pack(pady=(20, 10), padx=(30, 10), anchor='w')

        # Label for product name
        product_name_lbl = ctk.CTkLabel(
            container,
            text="Product Name",
            text_color="#1E1E1E",
            font=("Inter", 20, "bold")
        )
        product_name_lbl.pack(pady=(10, 5), padx=(30, 10), anchor='w')

        # Product name entry field
        product_name_entry = ctk.CTkEntry(
            container,
            text_color="#372724",
            placeholder_text="Enter product name",
            fg_color="#F5F5F5",
            font=("Inter", 18),
            width=430,
            height=30,
            corner_radius=3,
            border_width=1  
        )
        product_name_entry.pack(pady=(10, 5), padx=(30, 10), anchor='w')

        # Label for category selection
        category_lbl = ctk.CTkLabel(
            container,
            text="Category",
            text_color="#1E1E1E",
            font=("Inter", 18, "bold")
        )
        category_lbl.pack(pady=(10, 5), padx=(30, 10), anchor='w')

        # Category combobox, populated from the database
        category_combobox = ctk.CTkComboBox(
            container,
            values=self.categories,  
            width=200,  
            fg_color="#F5F5F5",
            text_color="black",
            font=("Inter", 18)
        )
        category_combobox.pack(pady=(10, 20), padx=(30, 10), anchor='w')

        # Label for price
        price_lbl = ctk.CTkLabel(
            container,
            text="Price",
            text_color="#1E1E1E",
            font=("Inter", 18, "bold")
        )
        price_lbl.pack(pady=(10, 5), padx=(30, 10), anchor='w')

        # Price entry field
        price_entry = ctk.CTkEntry(
            container,
            text_color="#372724",
            placeholder_text="Enter product price",
            fg_color="#F5F5F5",
            font=("Inter", 18),
            width=200,  
            height=30,
            corner_radius=3,
            border_width=1
        )
        price_entry.pack(pady=(10, 5), padx=(30, 10), anchor='w')

        # Instruction label for ingredients checkboxes
        ingredients_instr_lbl = ctk.CTkLabel(
            container,
            text="Select ingredients for the new product from the list below:",
            text_color="black",
            font=("Inter", 11, "italic", "bold")
        )
        ingredients_instr_lbl.pack(pady=(10, 5), padx=(30, 10), anchor='w')

        # Ingredient checkboxes
        self.create_ingredient_checkboxes(container, ingredient_names)

        # Button Container
        button_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
        button_container.pack(fill="x", padx=(120, 0), pady=(10, 10), anchor="s") 


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
        cancel_btn.pack(side="left", padx=(0, 10), pady=10)

        # Save Button
        save_btn = ctk.CTkButton(
            button_container,
            text="Save",
            font=("Inter", 20, "bold"),
            width=100,
            fg_color="#5482C7",
            text_color="#F5F5F5",
            command=lambda: self.add_new_product_to_menu(product_name_entry.get(), category_combobox.get(), price_entry.get())
        )
        save_btn.pack(side="left", padx=(20, 20), pady=10)

    def create_ingredient_checkboxes(self, container, ingredient_names):
        self.checkbuttons = []  
        for idx, ingredient in enumerate(ingredient_names):
            var = ctk.StringVar(value=ingredient)  
            checkbutton = ctk.CTkCheckBox(
                container,
                text=ingredient,
                text_color="black",
                variable=var,
                onvalue=ingredient, 
                offvalue="off", 
                command=lambda var=var: self.on_ingredient_check(var)
            )
            checkbutton.pack(anchor="w", padx=(30, 10), pady=(5, 5))
            checkbutton.select()
            self.checkbuttons.append((checkbutton, var))  

    def on_ingredient_check(self, var):
        if var.get() != "off":
            if var.get() not in self.selected_ingredients:
                self.selected_ingredients.append(var.get()) 
        else:
            if var.get() in self.selected_ingredients:
                self.selected_ingredients.remove(var.get())  

    def add_new_product_to_menu(self, product_name, price, category):
        try:
            cursor = db.cursor()

            insert_unit_query = """
            INSERT INTO tbl_product_unit (unit_name)
            VALUES (%s)
            """
            cursor.execute(insert_unit_query, (product_name,))
            
            unit_id = cursor.lastrowid

            insert_query = """
            INSERT INTO tbl_products (product_name, product_price, product_category, product_image, unit_id, product_status)
            VALUES (%s, %s, %s, NULL, %s, 'Available')
            """
            cursor.execute(insert_query, (product_name, category, price, unit_id))
            

            db.commit()
            cursor.close()
            print("Product added successfully!")
            self.modal.destroy()  # Close the modal after saving
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_product_categories(self):
        categories = []
        try:
            cursor = db.cursor()  
            cursor.execute("SELECT category_name FROM tbl_product_category")
            categories = [row[0] for row in cursor.fetchall()]
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return categories
