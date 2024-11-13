import customtkinter as ctk
from components.actions.db.fetch_inventory_categories import fetch_inventory_by_category
from components.actions.db.delete_ingredient_item import delete_inventory_item
from components.actions.inventory.modal_edit_ingredient_item import IngredientManager

from PIL import Image, ImageTk

def display_inventory(inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category):
    for widget in ingredient_display_scrollable_frame.winfo_children():
        widget.destroy()

    # Fetch ingredients 
    ingredients = fetch_inventory_by_category(category)

    for idx, ingredient in enumerate(ingredients):
        ingredient_name = ingredient[0]
        initial_status = ingredient[2]

      
        ingredient_label = ctk.CTkLabel(
            ingredient_display_scrollable_frame,
            text=ingredient_name,
            font=("Inter", 24, "bold"),
            text_color="black",
            width=450
        )
        ingredient_label.grid(row=idx, column=0, padx=(5, 5), pady=5, sticky="w")  

        # Create the status dropdown
        status_dropdown = create_status_dropdown(ingredient_name, initial_status)
        status_dropdown.grid(row=idx, column=1, padx=(5, 5), pady=5, sticky="w")  

        # Edit Button
        edit_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/misc/edit_icon.png")
        resized_icon = edit_btn_icon.resize((30, 30))
        edit_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))
        
        
        edit_item = IngredientManager()

        action_edit_button = ctk.CTkButton(
            ingredient_display_scrollable_frame,
            image=edit_btn_icon,
            text="",
            font=("Inter", 16, "bold"),
            fg_color="#E8BA19",
            text_color="white",
            width=50,  
            height=40,
            cursor="hand2",
             command=lambda name=ingredient_name: edit_item.edit_ingredient_item(name, display_inventory, inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category)
        )
        action_edit_button.grid(row=idx, column=2, padx=(5, 5), pady=5, sticky="ew") 

        # Delete Button
        delete_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/misc/delete_icon.png")
        resized_icon = delete_btn_icon.resize((30, 30))
        delete_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

        action_delete_button = ctk.CTkButton(
            ingredient_display_scrollable_frame,
            text="",
            image=delete_btn_icon,
            fg_color="#D73030",
            text_color="white",
            width=50,
            height=40,
            cursor="hand2",
             command=lambda name=ingredient_name: delete_inventory_item(name, display_inventory, inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category)
        )
        action_delete_button.grid(row=idx, column=3, padx=(5, 5), pady=5, sticky="ew")  

    # Configure columns
    ingredient_display_scrollable_frame.grid_columnconfigure(0, weight=1)  
    ingredient_display_scrollable_frame.grid_columnconfigure(1, weight=1)  
    ingredient_display_scrollable_frame.grid_columnconfigure(2, weight=1)  
    ingredient_display_scrollable_frame.grid_columnconfigure(3, weight=1) 

    for idx in range(len(ingredients)):
        ingredient_display_scrollable_frame.grid_rowconfigure(idx, weight=0) 
        
