import customtkinter as ctk
from components.actions.db.fetch_inventory_categories import fetch_inventory_by_category

def display_inventory(inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category):
    # Clear existing items in the scrollable frame
    for widget in ingredient_display_scrollable_frame.winfo_children():
        widget.destroy()

    # Fetch ingredients by category from the database
    ingredients = fetch_inventory_by_category(category)

    # Populate the scrollable frame with ingredients
    for idx, ingredient in enumerate(ingredients):
        ingredient_name = ingredient[0]  # Access the first element (name) of the tuple
        initial_status = ingredient[2]    # Access the third element (status) of the tuple

        # Create a label for the ingredient name
        ingredient_label = ctk.CTkLabel(
            ingredient_display_scrollable_frame,
            text=ingredient_name,
            font=("Inter", 24, "bold"),
            text_color="black",
            width=450  # Set width to match header
        )
        ingredient_label.grid(row=idx, column=0, padx=(5, 5), pady=5, sticky="ew")  # Align center

        # Create the status dropdown
        status_dropdown = create_status_dropdown(ingredient_name, initial_status)
        status_dropdown.grid(row=idx, column=1, padx=(5, 5), pady=5, sticky="ew")  # Align center

        # Optionally, you can add an action button for editing or deleting ingredients
        action_button = ctk.CTkButton(
            ingredient_display_scrollable_frame,
            text="Edit",
            width=450  # Set width to match header
        )
        action_button.grid(row=idx, column=2, padx=(5, 5), pady=5, sticky="ew")  # Align center

    # Set the column weights to ensure proper alignment and responsiveness
    ingredient_display_scrollable_frame.grid_columnconfigure(0, weight=1, minsize=450)  # Ingredient Name
    ingredient_display_scrollable_frame.grid_columnconfigure(1, weight=1, minsize=450)  # Availability (Status)
    ingredient_display_scrollable_frame.grid_columnconfigure(2, weight=1, minsize=450)  # Action (Edit Button)

    # Set row weight to ensure proper height allocation
    for idx in range(len(ingredients)):
        ingredient_display_scrollable_frame.grid_rowconfigure(idx, weight=1)  # Allow rows to expand equally
