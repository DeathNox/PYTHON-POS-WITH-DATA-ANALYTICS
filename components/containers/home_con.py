import customtkinter as ctk
import tkinter as tk
from PIL import Image as PILImage
from io import BytesIO
from db_setup.db_connect import *
from PIL import Image, ImageTk
import io
from components.frames.header import HeaderFrame


receipt_container = None

if hasattr(PILImage, 'Resampling'):
    resampling_filter = PILImage.Resampling.LANCZOS
else:
    resampling_filter = PILImage.LANCZOS

# Resets the receipt
def reset_receipt_container():
    global receipt_container
    if receipt_container:
        receipt_container.frame.destroy()  
        receipt_container = None  
        print("ReceiptContainer reset.")


# Pang setup ng receipt -> then show 
def setup_receipt_container(window):
    from components.containers.receipt_con import ReceiptContainer
    
    global receipt_container
    
    if receipt_container is None:
        print("Initializing ReceiptContainer")
        receipt_container = ReceiptContainer(window)
        print("ReceiptContainer initialized, but not packed.")
        
        
        

# Shows receipt 
def show_receipt_container():
    global receipt_container
    if receipt_container and not receipt_container.frame.winfo_ismapped(): 
        receipt_container.frame.pack(side="right", fill="y", padx=8, pady=8) 
        print("Showing ReceiptContainer")
    else:
        print("ReceiptContainer is already shown or not initialized.")




# Hides receipt when switching to different interfaces
def hide_receipt_container():
    global receipt_container
    if receipt_container and receipt_container.frame.winfo_ismapped():
        receipt_container.frame.pack_forget()  
        print("Hiding ReceiptContainer frame")



# Allows to display the products from the database
def fetch_products():
    sql = "SELECT product_name, product_category, product_price, product_image FROM tbl_products WHERE product_status = 'Available'"
    mycursor.execute(sql)
    return mycursor.fetchall()



# If the user clicks an item to order, this function handles the process of putting it sa receipt.
def on_card_click(product_name, product_price, quantity_entry, window):
    global receipt_container
    try:
        quantity_text = quantity_entry.get().strip()
        if not quantity_text:
            raise ValueError("Quantity cannot be empty.")
        
        quantity = int(quantity_text)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        
        # Setup the receipt container if it's None
        if receipt_container is None:
            print("Setting up the ReceiptContainer because it's None.")
            setup_receipt_container(window)  
        
        if receipt_container:
            receipt_container.add_item(product_name, product_price, quantity)
            show_receipt_container()  # Show the receipt container when an item is added
            
        else:
            print("Receipt container is not set up.")
    except ValueError as e:
        print(f"Invalid quantity: {e}")

# DALE - UPDATE
# Resize the image
def resize_image(image_data, width, height):
    try:
        # Load image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Resize the image
        img = img.resize((width, height), Image.LANCZOS)  
        
        # Convert to PhotoImage for CTkLabel
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None


        
        
        
        
        
def home_container(window, user_id):
    # Create the main container
    main_container = ctk.CTkFrame(window, fg_color="#EBE0D6", width=975, height=895, corner_radius=10)
    main_container.pack(side="left", fill="both", expand=True, padx=10, pady=20)

    # Header
    header_frame = HeaderFrame(main_container, user_id=user_id)

    # Title of the Interface 
    title_label = ctk.CTkLabel(
        header_frame,
        text="Point Of Sales System",
        text_color="#EBE0D6",
        font=("Inter", 32, "bold"),
        bg_color="transparent", compound="left"
    )
    title_label.pack(anchor="nw", pady=20, padx=25)

    # Vertical Scroll bar
    scrollable_frame = ctk.CTkScrollableFrame(main_container, fg_color="#EBE0D6", width=950, height=800)
    scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

    products = fetch_products()
    num_columns = 4

    for i in range(num_columns):
        scrollable_frame.grid_columnconfigure(i, weight=1)

    for idx, (name, category, price, image_data) in enumerate(products):
        row = idx // num_columns
        column = idx % num_columns

        # Product Container (Card Like)
        product_card = ctk.CTkFrame(scrollable_frame, fg_color="#F4F1F0", corner_radius=10, width=300, height=400)
        product_card.grid(row=row, column=column, padx=15, pady=15, sticky="n")  # Changed sticky to "n" to prevent vertical expansion

        # Image Frame
        image_frame = ctk.CTkFrame(product_card, fg_color="#E9C7A7", corner_radius=10, width=280, height=280)
        image_frame.pack(pady=(10, 5), padx=10, fill="both", expand=True)

        photo = resize_image(image_data, 280, 280)
        
        if photo:
            lbl_image = ctk.CTkLabel(image_frame, image=photo, text="")
            lbl_image.image = photo
            lbl_image.pack(fill="both", expand=True)
        else:
            lbl_image = ctk.CTkLabel(image_frame, text="Image Not Available", fg_color="#E4CFBB")
            lbl_image.pack(fill="both", expand=True)

        # Product Info Frame Container
        desc_frame = ctk.CTkFrame(product_card, fg_color="#F4F1F0")
        desc_frame.pack(anchor="center", pady=10, padx=20, fill="x")

        # Name Frame for proper alignment
        name_frame = ctk.CTkFrame(desc_frame, fg_color="#F4F1F0")
        name_frame.pack(side="left", padx=0, fill="x", expand=True)

        # Product Name
        item_label = ctk.CTkLabel(name_frame, text=f"{name}", font=("Inter", 18, "bold"), text_color="black")
        item_label.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Price Frame for proper alignment
        price_frame = ctk.CTkFrame(desc_frame, fg_color="#F4F1F0")
        price_frame.pack(side="right", padx=5, fill="x")

        # Product Price
        price_label = ctk.CTkLabel(price_frame, text=f"{price:.2f}", font=("Inter", 16, "bold"), text_color="black")
        price_label.pack(side="right", padx=2)

        # Product Quantity
        quantity_frame = ctk.CTkFrame(product_card, fg_color="#F4F1F0")
        quantity_frame.pack(pady=(5, 10), padx=5, fill="x")

        quantity_label = ctk.CTkLabel(quantity_frame, text="QUANTITY", text_color="black", font=("Inter", 18, "bold"))
        quantity_label.pack(side="top", padx=5)

        quantity_spinbox = tk.Spinbox(quantity_frame, from_=1, to=100, width=5, font=("Inter", 18), justify="center")
        quantity_spinbox.pack(side="bottom", padx=5)

        button_frame = ctk.CTkFrame(product_card, fg_color="#F4F1F0")
        button_frame.pack(pady=(10, 10), padx=5, fill="x")

        add_button = ctk.CTkButton(button_frame, text="ORDER", font=("Inter", 24, "bold"), fg_color="#372724",
                                    command=lambda name=name, price=price, quantity_entry=quantity_spinbox: on_card_click(name, price, quantity_entry, window))
        add_button.pack(pady=5, padx=5)

    # Configure the last row to expand if needed
    scrollable_frame.grid_rowconfigure((len(products) // num_columns), weight=1)

    return main_container
