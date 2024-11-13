import random
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

# Sample data for ingredients
ingredient_data = {
    'toppings': ['./imgs/menu_items/coldbrews/salted_caramel.png', './imgs/menu_items/coldbrews/salted_caramel.png'],  
    'base_liquids': ['./imgs/menu_items/coldbrews/matcha.png', './imgs/menu_items/coldbrews/matcha.png'],
    'coffee_base': ['./imgs/menu_items/coldbrews/machiato.png', './imgs/menu_items/coldbrews/iced_coffee.png'],
    'additives': ['./imgs/menu_items/coldbrews/salted_caramel.png', './imgs/menu_items/coldbrews/matcha.png']
}

class MixAndMatchApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Mix and Match Ingredients")
        self.root.geometry("600x600")

        self.selected_ingredients = []
        self.current_category = None
        self.current_index = 0

        # Frame for ingredient categories
        self.category_frame = ctk.CTkFrame(self.root)
        self.category_frame.pack(pady=10)

        # Create buttons for each ingredient category
        for category, images in ingredient_data.items():
            cat_frame = ctk.CTkFrame(self.category_frame)
            cat_frame.pack(side="top", fill="x", padx=10, pady=5)

            label = ctk.CTkLabel(cat_frame, text=category.capitalize())
            label.pack(pady=5)

            category_button = ctk.CTkButton(cat_frame, text=f"Select {category.capitalize()}", command=lambda c=category: self.show_images(c))
            category_button.pack(pady=5)

        # Display selected ingredients
        self.selected_frame = ctk.CTkFrame(self.root)
        self.selected_frame.pack(pady=10)

        self.selected_label = ctk.CTkLabel(self.selected_frame, text="Selected Ingredients: None")
        self.selected_label.pack(pady=10)

        # Image display area
        self.image_label = ctk.CTkLabel(self.root, text="")
        self.image_label.pack(pady=20)

        # Navigation buttons
        self.prev_button = ctk.CTkButton(self.root, text="Previous", command=self.show_prev_image)
        self.prev_button.pack(side="left", padx=20)

        self.next_button = ctk.CTkButton(self.root, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right", padx=20)

        # Finalize button
        self.finalize_button = ctk.CTkButton(self.root, text="Finalize Combination", command=self.finalize_combination)
        self.finalize_button.pack(pady=20)

        self.root.mainloop()

    def show_images(self, category):
        self.current_category = category
        self.current_index = 0
        self.update_image()

    def update_image(self):
        if self.current_category:
            images = ingredient_data[self.current_category]
            img_path = images[self.current_index]
            img = Image.open(img_path).resize((200, 200), Image.LANCZOS)  
            img_tk = ImageTk.PhotoImage(img)

            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk  

    def show_prev_image(self):
        if self.current_category:
            images = ingredient_data[self.current_category]
            self.current_index = (self.current_index - 1) % len(images)
            self.update_image() 

    def show_next_image(self):
        if self.current_category:
            images = ingredient_data[self.current_category]
            self.current_index = (self.current_index + 1) % len(images)
            self.update_image()

    def finalize_combination(self):
        if self.selected_ingredients:
            combination_name = " & ".join([i.split('.')[0] for i in self.selected_ingredients])
            messagebox.showinfo("Finalized Combination", f"You have created: {combination_name}")
        else:
            messagebox.showwarning("No Ingredients Selected", "Please select ingredients to finalize a combination.")

# Run the application
if __name__ == "__main__":
    app = MixAndMatchApp()
