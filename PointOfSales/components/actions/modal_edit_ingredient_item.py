from db_setup.db_connect import db, mycursor
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

def edit_ingredient_item(ingredient_name, display_inventory, inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category):
    try:
        # Modal Display for Edit
        from main import CenterWindowToDisplay
        
        modal = ctk.CTkToplevel()
        modal.title("Edit Ingredient")
        modal.geometry(CenterWindowToDisplay(modal, 520, 480, modal._get_window_scaling()))
        modal.resizable(False, False)
        modal.configure(fg_color="#30211E")
        
        container = ctk.CTkFrame(modal, fg_color="#EBE0D6")
        container.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="nsew")
        
        modal.grid_rowconfigure(0, weight=1)
        modal.grid_columnconfigure(0, weight=1)
        
        # Modal label
        modal_lbl = ctk.CTkLabel(
            container,
            text="Edit Ingredient",
            text_color="#1E1E1E",
            font=("Inter", 26, "bold")
        )
        modal_lbl.grid(row=0, column=0, pady=(20, 10), padx=(30, 10), sticky='w')

        # Input fields for ingredient name and status
        ingredient_name_label = ctk.CTkLabel(container, text="Ingredient Name",
            text_color="#1E1E1E",
            font=("Inter", 20, "bold"))
        
        
        ingredient_name_label.grid(row=1, column=0, padx=(30, 10), pady=(10, 5), sticky="w")
        
        
        ingredient_name_entry = ctk.CTkEntry(container,
                                    text_color="#372724",
                                    fg_color="#F5F5F5",
                                    font=("Inter", 18),
                                    width=430,
                                    height=30,
                                    corner_radius=3,
                                    border_width=1  
                                             )
        ingredient_name_entry.insert(0, ingredient_name)  
        
        ingredient_name_entry.grid(row=2, column=0, padx=(30, 10), pady=(5, 10), sticky="w")

        status_label = ctk.CTkLabel(container, text="Status:", font=("Inter", 20))
        status_label.grid(row=3, column=0, padx=(30, 10), pady=(10, 5), sticky="w")
        
        
        
        # Button container
        button_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
        button_container.grid(row=5, column=0, columnspan=2, padx=(30, 0), pady=(50, 10), sticky="ew")
        
        button_container.grid_columnconfigure(0, weight=1)
        
        # Cancel Button
        cancel_btn = ctk.CTkButton(
            button_container,
            text="Cancel",
            command=modal.destroy,
            font=("Inter", 20, "bold"),
            width=100,
            fg_color="#F5F5F5",
            text_color="#2C2C2C"
        )
        cancel_btn.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="e")
        
        # Save Button
        def save_changes():
            new_name = ingredient_name_entry.get()
      
            
            try:
                # SQL update query
                sql_update = "UPDATE tbl_product_ingredients SET ingredient_name = %s WHERE ingredient_name = %s"
                values = (new_name, ingredient_name)
                mycursor.execute(sql_update, values)
                db.commit()
                
                messagebox.showinfo("Success", f"{ingredient_name} updated successfully.")
                
                # Close modal and refresh inventory display
                modal.destroy()
                display_inventory(inventory_display, ingredient_display_scrollable_frame, create_status_dropdown, category)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update ingredient: {e}")

        save_btn = ctk.CTkButton(
            button_container,
            text="Save Changes",
            font=("Inter", 20, "bold"),
            width=100,
            fg_color="#5482C7",
            text_color="#F5F5F5",
            command=save_changes
        )
        save_btn.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="e")

    except Exception as e:
        messagebox.showerror("Error", f"Unable to edit {ingredient_name}: {e}")
