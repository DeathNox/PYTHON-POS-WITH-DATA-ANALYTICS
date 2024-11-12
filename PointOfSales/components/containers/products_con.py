
import customtkinter as ctk
from db_setup.db_connect import db, mycursor
from io import BytesIO
from PIL import Image, ImageTk
from components.actions.db.fetch_products import get_all_products
from components.frames.header import HeaderFrame
from components.actions.modal_generate_product import Modal_Generate_New_Product_Display

STATUS_OPTIONS = ["Available", "Not Available"]

def update_product_status(product_name, new_status):
    
    try:
        mycursor = db.cursor()
        sql = "UPDATE tbl_products SET product_status = %s WHERE product_name = %s"
        mycursor.execute(sql, (new_status, product_name))
        db.commit()  
    except Exception as e:
        print(f"Error updating product status: {e}")
    finally:
        mycursor.close()
        
        
def get_product_details(product_name):
    """Fetch product details from the database by product name."""
    try:
        mycursor = db.cursor()
        sql = "SELECT product_name, product_category, product_price, product_status, product_image FROM tbl_products WHERE product_name = %s"
        mycursor.execute(sql, (product_name,))
        return mycursor.fetchone()  
    except Exception as e:
        print(f"Error fetching product details: {e}")
    finally:
        mycursor.close()

def display_products(window):
      
     
      
      container = ctk.CTkFrame(window, fg_color="#EBE0D6", width=1275, height=900, corner_radius=2)
      container.pack_propagate(False)
      container.pack(side="right", fill="both", expand=True, padx=10, pady=10)


      
      header_frame = HeaderFrame(container) 
      


      prod_lbl = ctk.CTkLabel(
            header_frame,
            text="View Products",
            font=("Inter", 32, "bold"),
            fg_color="transparent",
            text_color="#EBE0D6",
            compound="left"
      )
      prod_lbl.pack(anchor="nw", pady=20, padx=25)

   # Add Products Button
      add_btn_icon = Image.open("./imgs/misc/add_product_icon.png")
      resized_icon = add_btn_icon.resize((30, 30))
      add_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

      add_products_redirect = ctk.CTkButton(
      container,
      text="ADD NEW PRODUCT",
      image=add_btn_icon,
      font=("Inter", 16, "bold"),
      fg_color="#5482C7",
      text_color="white",
      width=70,
      height=40,
      corner_radius=15,
      cursor="hand2",
      command=lambda: redirect_to_add_product(window)
      )

    
      add_products_redirect.grid(row=0, column=0, padx=(20, 10), pady=(150, 5), sticky="e") 


         # Generate Product Btn
      generate_product_icon = Image.open("./imgs/icons/chat-gpt.png")
      resized_icon = generate_product_icon.resize((30, 30))
      generate_product_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

      generate_product = ctk.CTkButton(
      container,
      text="",
      image=generate_product_icon,
      fg_color="#5482C7",
      width=70,
      height=40,
      corner_radius=15,
      cursor="hand2",
      command=Modal_Generate_New_Product_Display
      )

    
      generate_product.grid(row=0, column=6, padx=(50, 10), pady=(150, 5), sticky="w") 

      table_frame = ctk.CTkFrame(container, fg_color="#372724", corner_radius=10)
      table_frame.pack(padx=20, pady=(150, 10), fill="both", expand=True)

      table_header_frame = ctk.CTkFrame(table_frame, fg_color="#372724", corner_radius=5)
      table_header_frame.pack(fill="x")

      table_headers = ["Product Name", "Category", "Unit Price", "Status", "Action"]
      col_widths = [300, 270, 270, 270, 270]

      for idx, header in enumerate(table_headers):
            label = ctk.CTkLabel(
                  table_header_frame,
                  text=header,
                  font=("Inter", 20, "bold"),
                  text_color="white",
                  width=col_widths[idx]
            )
            label.grid(row=0, column=idx, padx=5, pady=15)

            if idx < len(table_headers) - 1:
                  ctk.CTkFrame(table_header_frame, fg_color="white", width=1, height=40).grid(row=0, column=idx + 1, pady=10)
                  
                  

      product_display_scrollable_frame = ctk.CTkScrollableFrame(table_frame, fg_color="#F4F4F4", height=500)
      product_display_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

      products_display = get_all_products()
      status_options = ["Available", "Not Available"]



      def create_status_dropdown(product_name, initial_status):
            
          

            dropdown_color = "#6FCF6D" if initial_status == "Available" else "#FF4D4D"

          
            status_dropdown = ctk.CTkOptionMenu(
                  product_display_scrollable_frame,
                  values=status_options,
                  command=lambda new_status: (
                  update_product_status(product_name, new_status),
                  update_dropdown_color(status_dropdown) 
                  ),
                  text_color="white",
                  font=("Inter", 16, "bold"),
                  width=col_widths[3],
                  fg_color=dropdown_color,
                  button_color=dropdown_color
            )
            status_dropdown.set(initial_status) 
            return status_dropdown

      def update_dropdown_color(status_dropdown):
            
 
            
            selected_status = status_dropdown.get()
            dropdown_color = "#6FCF6D" if selected_status == "Available" else "#FF4D4D"
            status_dropdown.configure(fg_color=dropdown_color, button_color=dropdown_color)

      for row_idx, product in enumerate(products_display):
            product_name, product_category, product_price, product_status = product
            product_price = f"₱ {product_price:,.2f}"
        

            for col_idx, value in enumerate([product_name, product_category, product_price]):
                  label = ctk.CTkLabel(
                  product_display_scrollable_frame,
                  text=value,
                  font=("Inter", 20, "bold"),
                  text_color="#30211E",
                  width=col_widths[col_idx]
                  )
                  label.grid(row=row_idx, column=col_idx, padx=5, pady=5)

            
            status_dropdown = create_status_dropdown(product_name, product_status)
            status_dropdown.grid(row=row_idx, column=len(table_headers) - 1, padx=(5, 20), pady=10, sticky="ew")

            update_dropdown_color(status_dropdown)
            
            

            action_view_button = ctk.CTkButton(
                  product_display_scrollable_frame, 
                  text="VIEW",
                  font=("Inter", 16, "bold"),
                  fg_color="#5482C7",
                  text_color="white",
                  width=60,  
                  height=40,
                  cursor="hand2",
                  command=lambda name=product_name: view_product_action(name, window)
                  )
            action_view_button.grid(row=row_idx, column=10, padx=(5, 5), pady=10)
            
            action_edit_button = ctk.CTkButton(
                  product_display_scrollable_frame, 
                  text="EDIT",
                  font=("Inter", 16, "bold"),
                  fg_color="#E8BA19",
                  text_color="white",
                  width=60,  
                  height=40,
                  cursor="hand2",
                  command=lambda name=product_name: edit_product_action(name, window)

                  )
            action_edit_button.grid(row=row_idx, column=11, padx=(5, 5), pady=10)
            
            
            delete_btn_icon = Image.open("./imgs/misc/delete_icon.png")
            resized_icon = delete_btn_icon.resize((30, 30))
            
            delete_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))
            
            action_delete_button = ctk.CTkButton(
                  product_display_scrollable_frame, 
                  text="",
                  image=delete_btn_icon,
                  fg_color="#D73030",
                  text_color="white",
                  width=50,  
                  height=40,
                  cursor="hand2",
                  command=lambda name=product_name: delete_product_action(name, window)
                  )
            action_delete_button.grid(row=row_idx, column=12, padx=(5, 10), pady=10)

      return container



def redirect_to_add_product(window):
      
  from components.containers.prod_config_con import prod_config_container
  for widget in window.winfo_children():
        widget.destroy()  
    

  prod_config_container(window)
  
  

def view_product_action(product_name, window):
    """Open a modal to view product details, including image."""
    from main import CenterWindowToDisplay
    from PIL import Image
    from io import BytesIO

    # Create the modal window
    modal = ctk.CTkToplevel(window)
    modal.title(f"View Product: {product_name}")
    modal.geometry(CenterWindowToDisplay(modal, 600, 450, modal._get_window_scaling()))
    modal.resizable(False, False)
    modal.configure(fg_color="#EBE0D6") 

    # Fetch product details
    product_details = get_product_details(product_name)

    
    if product_details:
       
        details_frame = ctk.CTkFrame(modal, fg_color="#FFFFFF", corner_radius=10)
        details_frame.pack(padx=20, pady=20, fill="both", expand=True)

      
        labels = ["Product Name", "Category", "Price", "Status"]
        for idx, label in enumerate(labels):
            label_text = f"{label}:"
            value_text = product_details[idx]

            # Create labels for the detail name and value
            name_label = ctk.CTkLabel(
                details_frame, 
                text=label_text, 
                font=("Inter", 16, "bold"), 
                text_color="#30211E"
            )
            name_label.grid(row=idx, column=0, sticky="w", padx=(10, 5), pady=(5, 0))

            value_label = ctk.CTkLabel(
                details_frame, 
                text=value_text, 
                font=("Inter", 16), 
                text_color="#30211E"
            )
            value_label.grid(row=idx, column=1, sticky="w", padx=(0, 10), pady=(5, 0))

        # Display the product image if available
        image_data = product_details[4]  
        if image_data:
            image = Image.open(BytesIO(image_data))
            image.thumbnail((150, 150)) 
            photo = ctk.CTkImage(image, size=(150, 150))

            image_label = ctk.CTkLabel(details_frame, image=photo, text="")
            image_label.grid(row=len(labels), column=0, columnspan=2, pady=(10, 0))

        # Create the close button
        close_button = ctk.CTkButton(
            modal, 
            text="Close", 
            command=modal.destroy, 
            font=("Inter", 16, "bold"), 
            width=100, 
            fg_color="#D73030", 
            text_color="white"
        )
        close_button.pack(pady=(10, 20))

    else:

        error_label = ctk.CTkLabel(
            modal, 
            text="Product details not found.", 
            font=("Inter", 16), 
            anchor="w", 
            text_color="#D73030"
        )
        error_label.pack(padx=10, pady=10)

      
        close_button = ctk.CTkButton(
            modal, 
            text="Close", 
            command=modal.destroy, 
            font=("Inter", 16, "bold"), 
            width=100, 
            fg_color="#D73030", 
            text_color="white"
        )
        close_button.pack(pady=(10, 20))

        
        
        
def edit_product_action(product_name, window):
    from main import CenterWindowToDisplay
    from ..actions.db.fetch_product_categories import get_product_categories
    from ..actions.db.save_changes import save_product_changes
    from ..actions.change_image import change_product_image
    
    
    modal = ctk.CTkToplevel(window)
    modal.title(f"Editing Product: {product_name}")
    modal.geometry(CenterWindowToDisplay(modal, 580, 400, modal._get_window_scaling()))
    modal.resizable(False, False)

    product_details = get_product_details(product_name)
    product_price = product_details[2]
    product_category = product_details[1]
    image_data = product_details[4] 

    # categories from the database 
    categories = get_product_categories()
    category_names = [category[1] for category in categories] 

    # Main container 
    main_container = ctk.CTkFrame(modal, fg_color="#EBE0D6")
    main_container.grid(row=0, column=0, padx=(10,10), pady=(10, 50), sticky="nsew")

 
    main_container.grid_rowconfigure(0, weight=1)
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=1)

    # Left container
    left_container = ctk.CTkFrame(main_container, fg_color="#EBE0D6")
    left_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    product_name_lbl = ctk.CTkLabel(
        left_container,
        text="Product Name:",
        text_color="#30211E",
        font=("Inter", 20, "bold")
    )
    product_name_lbl.grid(row=0, column=0, pady=(25, 10), padx=(28, 10), sticky="w")

    product_name_entry = ctk.CTkEntry(
        left_container,
        placeholder_text=f"{product_name}",
        text_color="#372724",
        fg_color="#F5F5F5",
        font=("Inter", 18),
        height=35,
        width=300,
        corner_radius=5
    )
    product_name_entry.grid(row=1, column=0, pady=(0, 15), padx=(28, 28), sticky="ew")

    product_price_lbl = ctk.CTkLabel(
        left_container,
        text="Price: ",
        text_color="#30211E",
        font=("Inter", 20, "bold")
    )
    product_price_lbl.grid(row=2, column=0, pady=(0, 15), padx=(28, 28), sticky="w")

    product_price_entry = ctk.CTkEntry(
        left_container,
        placeholder_text=f"PHP {product_price:.2f}",
        text_color="#372724",
        fg_color="#F5F5F5",
        font=("Inter", 18),
        height=35,
        width=300,
        corner_radius=5
    )
    product_price_entry.grid(row=3, column=0, pady=(0, 15), padx=(28, 10), sticky="w")

    category_lbl = ctk.CTkLabel(
        left_container,
        text="Category: ",
        text_color="#30211E",
        font=("Inter", 20, "bold")
    )
    category_lbl.grid(row=4, column=0, pady=(0, 15), padx=(28, 28), sticky="w")

    category_dropdown = ctk.CTkOptionMenu(
        left_container,
        values=category_names, 
        width=300,
        height=35,
        corner_radius=5,
        fg_color="#6F5E5C",
        text_color="white",
        font=("Inter", 16, "bold")
    )
    category_dropdown.set(product_category)
    category_dropdown.grid(row=5, column=0, pady=(0, 15), padx=(28, 10), sticky="w")

    right_container = ctk.CTkFrame(main_container, fg_color="#EBE0D6")
    right_container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    if image_data:
        product_image = Image.open(BytesIO(image_data))
        product_image.thumbnail((150, 150))  
        product_image_ctk = ImageTk.PhotoImage(product_image)
    else:
        product_image_ctk = None  

    image_label = ctk.CTkLabel(right_container, fg_color="#F5F5F5", image=product_image_ctk, text="")
    image_label.grid(row=0, column=0, padx=10, pady=10)

    change_image_button = ctk.CTkButton(
        right_container,
        text="Change Image",
        command=lambda: change_product_image(product_name, right_container),
        font=("Inter", 16)
    )
    change_image_button.grid(row=1, column=0, padx=10, pady=(10, 10))

    # Button container 
    button_container = ctk.CTkFrame(main_container, fg_color="#EBE0D6")
    button_container.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="ew")

    cancel_btn = ctk.CTkButton(
        button_container,
        text="Cancel",
        command=modal.destroy,
        font=("Inter", 16, "bold"),
        width=100,
        fg_color="#F5F5F5",
        text_color="black"
    )
    cancel_btn.grid(row=0, column=0, padx=(10, 10), pady=10)

    save_changes_btn = ctk.CTkButton(
        button_container,
        text="Save Changes",
        font=("Inter", 16, "bold"),
        width=100,
        fg_color="#5482C7",
        text_color="#F5F5F5",
        command=lambda: save_product_changes(
            product_name,
            product_name_entry.get(),
            float(product_price_entry.get().replace('PHP ', '').replace(',', '')),
            category_dropdown.get(),
            modal
        )
    )
    save_changes_btn.grid(row=0, column=1, padx=(0, 10), pady=10)


    button_container.grid_columnconfigure(0, weight=1)
    button_container.grid_columnconfigure(1, weight=1)



def delete_product_action(product_name, window):
    """Delete product from the database."""
    from main import CenterWindowToDisplay

    # Confirmation dialog
    modal = ctk.CTkToplevel(window)
    modal.title("Confirm Delete")
    modal.geometry(CenterWindowToDisplay(modal, 600, 150, modal._get_window_scaling()))
    modal.resizable(False, False)
    modal.configure(fg_color="#EBE0D6")
    

    confirmation_label = ctk.CTkLabel(modal, text=f"Remove '{product_name}' from your products?", font=("Inter", 18, "bold"), text_color="black")
    confirmation_label.pack(pady=20)


    def confirm_delete():
        try:
            mycursor = db.cursor()

            #  delete from the tbl_products 
            sql_delete_product = "DELETE FROM tbl_products WHERE product_name = %s"
            mycursor.execute(sql_delete_product, (product_name,))

            #  delete from tbl_product_unit
            sql_delete_unit = "DELETE FROM tbl_product_unit WHERE unit_name = %s"
            mycursor.execute(sql_delete_unit, (product_name,))

            db.commit()

            
            for widget in window.winfo_children():
                widget.destroy()
            display_products(window)
            modal.destroy()
        except Exception as e:
            print(f"Error deleting product: {e}")
        finally:
            mycursor.close()
            
            
            
            

    # Delete button
    confirm_button = ctk.CTkButton(
        modal, 
        text="Remove", 
        command=confirm_delete, 
        font=("Inter", 16, "bold"), 
        fg_color="#D73030",  
        text_color="white",
        width=120
    )
    confirm_button.pack(side="right", padx=(20, 10), pady=20)

    # Cancel button 
    cancel_button = ctk.CTkButton(
        modal, 
        text="Cancel", 
        command=modal.destroy, 
        font=("Inter", 16, "bold"), 
        fg_color="#F5F5F5",  
        text_color="black",
        width=120
    )
    cancel_button.pack(side="left", padx=(10, 20), pady=20)
