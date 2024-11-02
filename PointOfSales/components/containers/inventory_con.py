import customtkinter as ctk
from db_setup.db_connect import db
from components.actions.db.fetch_inventory_categories import fetch_inventory_by_category
from components.actions.display_inventory import display_inventory
from PIL import Image, ImageTk


class InventoryDisplay(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#EBE0D6", **kwargs)

        from components.frames.container import ContainerFrame
        from components.frames.header import HeaderFrame
        
        # Modal Import
        from components.actions.modal_add_ingredient import Modal_Add_Ingredient_Display

        container = ContainerFrame(self)
        container.pack(fill="both", expand=True, pady=(5, 5), padx=(5, 5))

        header_frame = HeaderFrame(container)
        header_frame.pack(fill="x", side="top")

        inventory_lbl = ctk.CTkLabel(
            header_frame,
            text="View Inventory",
            font=("Inter", 32, "bold"),
            fg_color="transparent",
            text_color="#EBE0D6",
            compound="left"
        )
        inventory_lbl.pack(anchor="nw", pady=20, padx=25)

        
         # Category label
        category_lbl = ctk.CTkLabel(container, text="Categories", fg_color="#EBE0D6", font=("Inter", 36, "bold"), text_color="#30211E")
        category_lbl.pack(anchor="nw", pady=(20, 0), padx=25)
        
        # Category Sort - Start
        category_frame = ctk.CTkFrame(container, fg_color="#EBE0D6")
        category_frame.pack(fill="x", pady=10)

       

        # Configuring grid columns for buttons
        category_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Button padding values
        button_padding_x = 10  
        button_padding_y = 10  

        # Coffee Base Button
        
        
        coffee_btn = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/icons/categories/light_/coffee_base.png")
        
        resized_icon = coffee_btn.resize((30, 40))
        ctk_coffee_icon = ctk.CTkImage(dark_image=resized_icon, size=(25, 30))
        
        
        coffee_base_button = ctk.CTkButton(
            category_frame,
            image=ctk_coffee_icon,
            text="Coffee Base",
            command=lambda: display_inventory(
                self, 
                self.ingredient_display_scrollable_frame, 
                self.create_status_dropdown, 
                "Coffee Base"
            ),
            corner_radius=10,
            font=("Inter", 25, "bold"),
            fg_color="#372724",
            width=150,
            height=55,
            text_color="#F1EBEB"
        )
        coffee_base_button.grid(row=0, column=0, padx=button_padding_x, pady=button_padding_y)

        # Base Liquids Button
        
          
        base_liquid_btn = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/icons/categories/light_/base_liquids.png")
        
        resized_icon = base_liquid_btn.resize((30, 40))
        ctk_base_liquid_icon = ctk.CTkImage(dark_image=resized_icon, size=(25, 30))
        
        
        
        
        base_liquids_button = ctk.CTkButton(
            category_frame,
            image=ctk_base_liquid_icon,
            text="Base Liquids",
            text_color="#F1EBEB",
            corner_radius=10,
            font=("Inter", 25, "bold"),
            fg_color="#372724",
            width=150,
            height=55,
            command=lambda: display_inventory(
                self, 
                self.ingredient_display_scrollable_frame, 
                self.create_status_dropdown, 
                "Base Liquids"
            )
        )
        base_liquids_button.grid(row=0, column=1, padx=button_padding_x, pady=button_padding_y)

        # additives Button
        
        additives_btn = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/icons/categories/light_/additives.png")
        
        resized_icon = additives_btn.resize((30, 40))
        ctk_additives_btn = ctk.CTkImage(dark_image=resized_icon, size=(25, 30))
        
        
        
        additives_button = ctk.CTkButton(
            category_frame,
            image=ctk_additives_btn,
            text="Additives",
            text_color="#F1EBEB",
            corner_radius=10,
            font=("Inter", 25, "bold"),
            fg_color="#372724",
            width=150,
            height=55,
            command=lambda: display_inventory(
                self, 
                self.ingredient_display_scrollable_frame, 
                self.create_status_dropdown, 
                "Additives"
            )
        )
        additives_button.grid(row=0, column=2, padx=button_padding_x, pady=button_padding_y)

        # Toppings Button
        
        toppings_btn = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/icons/categories/light_/toppings.png")
        resized_icon = toppings_btn.resize((30, 40))
        ctk_toppings_btn= ctk.CTkImage(dark_image=resized_icon, size=(25, 30))
        
        
        toppings_button = ctk.CTkButton(
            category_frame,
            image=ctk_toppings_btn,
            text="Toppings",
            text_color="#F1EBEB",
            corner_radius=10,
            font=("Inter", 25, "bold"),
            fg_color="#372724",
            width=150,
            height=55,
            command=lambda: display_inventory(
                self, 
                self.ingredient_display_scrollable_frame, 
                self.create_status_dropdown, 
                "Toppings"
            )
        )
        toppings_button.grid(row=0, column=3, padx=button_padding_x, pady=button_padding_y)

        # Category Sort - End


        # Add New Inventory
       
       
        modal_add_ingredient = Modal_Add_Ingredient_Display(refresh_callback=self.display_all_ingredients)

        
        add_new_inventory_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/misc/add_inventory.png")
        resized_icon = add_new_inventory_btn_icon.resize((30, 40))
        ctk_add_new_inventory_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))
        
        
       
        
        add_new_inventory_btn = ctk.CTkButton(
            container,
            image= ctk_add_new_inventory_btn_icon,
            text="ADD NEW INGREDIENT",
            font=("Inter", 16, 'bold'),
             fg_color="#5482C7",
            text_color="white",
            corner_radius=15,
            cursor="hand2",
            command=lambda: modal_add_ingredient.modal_add_inventory())

    
        add_new_inventory_btn.pack(anchor="nw", pady=(20, 0), padx=25)


        # scrollable frame for inventory
        table_frame = ctk.CTkFrame(container, fg_color="#372724", corner_radius=10)
        table_frame.pack(padx=20, pady=(30, 10), fill="both", expand=True)

        table_header_frame = ctk.CTkFrame(table_frame, fg_color="#372724", corner_radius=5)
        table_header_frame.pack(fill="x")

        table_headers = ["Ingredient Name", "Availability", "Action"]
        col_widths = [450, 450, 450]

        for idx, header in enumerate(table_headers):
            label = ctk.CTkLabel(
                table_header_frame,
                text=header,
                font=("Inter", 20, "bold"),
                text_color="white",
                width=col_widths[idx],
                corner_radius=10
            )
            label.grid(row=0, column=idx, padx=5, pady=15)
            if idx < len(table_headers) - 1:
                ctk.CTkFrame(table_header_frame, fg_color="white", width=1, height=40).grid(row=0, column=idx + 1, pady=10)

        self.ingredient_display_scrollable_frame = ctk.CTkScrollableFrame(table_frame, fg_color="#F4F4F4", height=500)
        self.ingredient_display_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.inventory_status_options = ["In Stock", "Out of Stock", "Low Stock"]
        
        self.display_all_ingredients()  # Call method to display all ingredients

    def display_all_ingredients(self):
        # Call display_inventory with an empty string or a keyword to represent all categories
        display_inventory(
            self, 
            self.ingredient_display_scrollable_frame, 
            self.create_status_dropdown, 
            "All"  # or use "" if you modify your fetching method accordingly
        )

        
        
        

    def create_status_dropdown(self, product_name, initial_status):
        from components.actions.db.update_ingredient_status import update_ingredient_status

     
        dropdown_color = self.get_color_by_status(initial_status)

        status_dropdown = ctk.CTkOptionMenu(
            self.ingredient_display_scrollable_frame,
            values=self.inventory_status_options,
            command=lambda new_status: (
                update_ingredient_status(product_name, new_status),
                self.update_dropdown_color(status_dropdown, new_status)  
            ),
            text_color="white",
            font=("Inter", 20, "bold"),
            fg_color=dropdown_color, 
            button_color=dropdown_color  
        )

        status_dropdown.set(initial_status) 
        return status_dropdown

    def update_dropdown_color(self, status_dropdown, selected_status):
        dropdown_color = self.get_color_by_status(selected_status)
        status_dropdown.configure(fg_color=dropdown_color, button_color=dropdown_color)

    def get_color_by_status(self, status):
        """Get the color corresponding to the ingredient status."""
        return (
            "#6FCF6D" if status == "In Stock" 
            else "#5482C7" if status == "Low Stock" 
            else "#FF4D4D"  
        )
