import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

from components.frames.header import HeaderFrame
from components.actions.generate_new_product import generate_hypothetical_products, generate_product_name, suggest_new_products, load_data, create_ingredient_matrix, train_random_forest

class Modal_Generate_New_Product_Display:
      
    def __init__(self):
        self.products_df, self.ingredients_df = load_data()  
        self.ingredient_matrix = create_ingredient_matrix(self.ingredients_df, self.products_df)  
        self.modal_generate_new_item()
            
    
    def modal_generate_new_item(self):
          
        from main import CenterWindowToDisplay
            
        
        self.modal = ctk.CTkToplevel()
        self.modal.title("Generate New Product")
        self.modal.geometry(CenterWindowToDisplay(self.modal, 550, 480, self.modal._get_window_scaling()))
        self.modal.resizable(False, False)
        self.modal.configure(fg_color="#30211E")
        
        container = ctk.CTkFrame(self.modal, fg_color="#EBE0D6")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        # Header frame
        header_frame = HeaderFrame(container)
        header_frame.pack(fill="x", pady=(0, 5))

        # Title of the Interface
        title_label = ctk.CTkLabel(
            header_frame,
            text="Suggested New Products",
            text_color="#EBE0D6",
            font=("Inter", 26, "bold"),
            bg_color="transparent", compound="left"
        )
        title_label.pack(anchor="nw", pady=20, padx=25)

        # Description of the Interface
        modal_description = ctk.CTkLabel(
            container,
            text="Generate new menu items automatically based on your inventory.",
            text_color="#1E1E1E",
            font=("Inter", 15, "bold"),
            bg_color="transparent", compound="left"
        )
        modal_description.pack(anchor="nw", padx=(20, 5), pady=(5, 10))

        # Generate product button
        generate_product_btn = ctk.CTkButton(
            container,
            text="Generate Combinations",
            fg_color="#5482C7",
            font=("Inter", 18, "bold"),
            width=70,
            height=40,
            corner_radius=10,
            cursor="hand2",
            command=self.on_generate_combinations
        )
        generate_product_btn.pack(pady=(10, 0), padx=(30, 30))

        # Suggestions Display Section
        self.suggestions_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
        self.suggestions_container.pack(fill="both", expand=True, pady=20)

        # Button container 
        button_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
        button_container.pack(side="bottom", fill="x", pady=(20, 10), padx=30)

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
            text_color="#F5F5F5"
        )
        save_btn.pack(side="right", padx=(10, 20), pady=10)

    def on_generate_combinations(self):
        
    # generate hypothetical products
        self.products_df, self.ingredients_df = load_data()  
        
        #  ingredient matrix
        self.ingredient_matrix = create_ingredient_matrix(self.ingredients_df, self.products_df)
        
        # Train the Random Forest model
        model = train_random_forest(self.ingredient_matrix)  
        
        # Generate new product combinations
        new_product_suggestions = generate_hypothetical_products(self.ingredients_df)  
        
        
        valid_suggestions = suggest_new_products(self.products_df, model, self.ingredient_matrix, new_combinations=new_product_suggestions)
        
       
        limited_suggestions = valid_suggestions[:3]

        for widget in self.suggestions_container.winfo_children():
            widget.destroy()


        if limited_suggestions:
            
            for combination in limited_suggestions:
                product_name = generate_product_name(combination)  
                
                
                
                suggestion_frame = ctk.CTkFrame(self.suggestions_container, fg_color="#EBE0D6", width=520)
                suggestion_frame.pack(fill="x", pady=5, padx=20)

                # Left container 
                left_container = ctk.CTkFrame(suggestion_frame, fg_color="#EBE0D6")
                left_container.grid(row=0, column=0, sticky="w") 

                # Display product name
                product_label = ctk.CTkLabel(
                    left_container,
                    text=product_name,
                    font=("Inter", 13, "italic"),
                    bg_color="transparent",
                    text_color="#1E1E1E"
                )
                product_label.pack(padx=10, pady=5)

               # Right container
                right_container = ctk.CTkFrame(suggestion_frame, fg_color="#EBE0D6")
                right_container.grid(row=0, column=1, sticky="e")  

                # Add button with icon
                add_btn_icon = Image.open("./imgs/misc/add_product_icon.png")
                resized_icon = add_btn_icon.resize((15, 15))  
                add_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(15, 15))

                add_button = ctk.CTkButton(
                    right_container,
                    image=add_btn_icon,
                    text="",
                    command=lambda name=product_name: self.add_to_menu(name),
                    fg_color="#4CAF50",
                    font=("Inter", 12, "bold"),
                    width=30,  
                    height=30
                )
                add_button.pack(side="left", padx=(10, 5), pady=5)  

              
                custom_btn_icon = Image.open("./imgs/icons/custom_icon.png")
                resized_icon = custom_btn_icon.resize((15, 15))  
                custom_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(15, 15))

                custom_button = ctk.CTkButton(
                    right_container,
                    image=custom_btn_icon,
                    text="",
                    fg_color="#4CAF50",
                    font=("Inter", 12, "bold"),
                    width=30,  
                    height=30
                )
                custom_button.pack(side="left", padx=(5, 10), pady=5) 


                suggestion_frame.grid_columnconfigure(0, weight=1) 
                suggestion_frame.grid_columnconfigure(1, weight=0)  


        else:
            no_suggestions_label = ctk.CTkLabel(
                self.suggestions_container,
                text="No valid new product combinations found.",
                font=("Inter", 14, "italic"),
                fg_color="transparent"
            )
            no_suggestions_label.pack()

          



# ? ADDS THE GENERATED PRODUCT SA MENU
# TODO: should pop up a modal to confirm the addition of the generated menu.
    def add_to_menu(self, product_name):
        print(f"Product '{product_name}' added to the menu!")  




#? ALLOWS THE USER TO CUSTOMIZE THE GENERATED PRODUCT MENU 
# TODO: should pop up a modal 

    def customize_generated_product(self, product_name):
        ...
        
        