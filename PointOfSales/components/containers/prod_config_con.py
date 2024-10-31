from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox 
import tkinter as tk
import os
from tkinter import filedialog
import mysql.connector
from db_setup.db_connect import mycursor, db
from components.frames.header import HeaderFrame

# TODO: sidepanel > add prod btn > redirect to this page - DONE
# TODO: (???) the client can add their other products. - DONE





def prod_config_container(window):

        global product_price_entry, prodName_entry, image_label, product_description_entry
    
        container = ctk.CTkFrame(window, fg_color="#EBE0D6", width=1275, height=900, corner_radius=2)
        container.pack_propagate(False)
        container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        
        header_frame = HeaderFrame(container)
        
     
        
       
         # Return Label
        return_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/misc/return.png") 
        resized_icon = return_btn_icon.resize((30, 30)) 
        return_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))  

        return_label = ctk.CTkLabel(header_frame, text="", 
                                    fg_color="transparent", text_color="#EBE0D6", cursor="hand2", compound="left")
        return_label.configure(image=return_btn_icon)
        return_label.pack(side="left", padx=(20, 10), pady=15)

  
        return_label.bind("<Button-1>", lambda e: return_to_main(window))
      
        
  
        
        
        add_prod_lbl = ctk.CTkLabel(header_frame, text="Add Product",
                                font=("Inter", 32, "bold"), fg_color="transparent", text_color="#EBE0D6", compound="left")
        add_prod_lbl.pack(anchor="nw", pady=20, padx=25)
  
        card_frame = ctk.CTkFrame(container, fg_color="#E3D8CD", corner_radius=20, width=350, height=600)
        card_frame.pack(padx=20, pady=20, side="left", anchor="n", fill="y", expand=False)

            
     
        
        
        # Product Name Start
        
        
        prodName_lbl = ctk.CTkLabel(
            card_frame,
            text="Product Name",
            font=("Inter", 24, "bold"),
            fg_color="transparent",
            text_color="black",
            compound="left"
        )
        prodName_lbl.grid(row=0, column=0, padx=25, pady=15, sticky="w") 


        #product name form
        
        prodName_entry = ctk.CTkEntry(
            card_frame,
            placeholder_text="Enter product name",
            text_color="black",
            fg_color="white",
            width=430,
            font=("Inter", 22), corner_radius=5, border_color="white"
        )
        
     
        prodName_entry.grid(row=1, column=0, padx=25, pady=15, sticky="w")  


        #Product Name End


      
      


        # Product Image Start
        
        

        
        prodImage_lbl = ctk.CTkLabel(
            
            card_frame,
            text="Product Image",
            font=("Inter", 24, "bold"),
            fg_color="transparent",
            text_color="black",
            compound="left"
            
        )
        
        prodImage_lbl.grid(row=2, column=0, padx = 20, pady = 10, sticky="w")
        

        def on_enter(event):
            prodImage_btn_upload.configure(text_color="#EBE0D6", fg_color="#6F5E5C")
            
        def on_leave(event):
            prodImage_btn_upload.configure(text_color="#372724", fg_color="#E4CFBB")
        
        
        frame_image_section = ctk.CTkFrame(card_frame, fg_color="#E3D8CD")  
        frame_image_section.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        prodImage_btn_upload = ctk.CTkButton(
                frame_image_section,
                text="Upload Image", 
                font=("Inter", 16),
                text_color="#372724",
                border_color="black",
                fg_color="#E4CFBB", 
                height=200, 
                width=200,  
                hover_color="#6F5E5C",
                command=lambda: prodImage_upload(image_label)  
            ) # TODO: add command="upload_image"
        prodImage_btn_upload.grid(row = 0, column = 0, padx = 20, pady = 10, sticky="w")
        
        
        image_label = ctk.CTkLabel(frame_image_section, text="", height=200, width=200, fg_color="#E4CFBB")
        image_label.grid(row=0, column=1, padx=5, pady=0)


     
            
        prodImage_btn_upload.bind("<Enter>", on_enter)
        prodImage_btn_upload.bind("<Leave>", on_leave)
      
        
        
        #Product Image End
        
        
       # ! product description start
        product_des_frame = ctk.CTkFrame(card_frame, fg_color="white", corner_radius=10)
        product_des_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Adjusting the size of the entry to fill the frame
        product_description_entry = ctk.CTkEntry(
            product_des_frame, 
            placeholder_text="Describe your product",
            font=("Inter", 18), 
            fg_color="transparent",
            text_color="#372724"
        )

        # Make the entry fill the entire width of the frame
        product_description_entry.pack(fill="both", expand=True, padx=10, pady=10)

    
        # ! product description end





       
        
        
        
        price_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        price_frame.grid(row=5, column=0, columnspan=2, padx=(10, 5), pady=(20, 5), sticky="w")
        
        
            # Label for product price
            
        product_price_lbl = ctk.CTkLabel(
        price_frame,
        text="Price (PHP):",
        font=("Inter", 24, "bold"),
        fg_color="transparent",
        text_color="#372724",
        compound="left"
    )
        product_price_lbl.grid(row=0, column=0, padx=(10, 5), pady=(0, 0), sticky="w")

        # Validation command
        vcmd = (price_frame.register(validate_price_entry), "%P")

        # Entry field for product price inside the same frame
        product_price_entry = ctk.CTkEntry(
            price_frame,
            fg_color="white",
            text_color="black",
            width=200,
            font=("Inter", 22),
            corner_radius=4,
            validate="key",
            validatecommand=vcmd,  
            placeholder_text="Enter Price"
        )
        product_price_entry.grid(row=0, column=1, padx=(5, 10), pady=(0, 0), sticky="w")
                
        """
        # ! TENTATIVE
        
          # TODO: available sizes buttons (M, L or via Oz)
          
    
        size_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        size_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

      
        size_lbl = ctk.CTkLabel(size_frame, text="SIZES:", text_color="#372724", font=("Inter", 24, "bold"))
        size_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="w")

       
       
        # ??? tentative: baka prefer ng client is by Oz ex: 18oz and so on.
        
        medium_size_btn = ctk.CTkButton(size_frame, fg_color="#E4CFBB", text="M", text_color="#372724", font=("Inter", 24, "bold"),
                                        width=100, height=40, command=lambda: toggle_size(medium_size_btn))
        medium_size_btn.grid(row=0, column=1, padx=5, pady=5)

        large_size_btn = ctk.CTkButton(size_frame, text="L", fg_color="#E4CFBB", text_color="#372724", font=("Inter", 24, "bold"),
                                    width=100, height=40, command=lambda: toggle_size(large_size_btn))
        large_size_btn.grid(row=0, column=2, padx=5, pady=5)



        # toggle button sizes
        def toggle_size(button):
            if button.cget("fg_color") == "#E4CFBB":  # If not clicked
                button.configure(fg_color="#372724", text_color="#EBE0D6")  # set it as clicked
            else:
                button.configure(fg_color="#E4CFBB", text_color="black")  # unclick
        """
        
         # product category start
           
    # DALE - UPDATE   
        #product categories
     
        query_productUnit = "SELECT category_name FROM tbl_product_category"
        mycursor.execute(query_productUnit)
        records_productUnit = mycursor.fetchall()

        global productCategories
        productCategories = []  

        for row in records_productUnit:
            category_name = row[0]  
            print(category_name)  
            productCategories.append(category_name)  #
        
        
        
        
        global category_frame
        category_frame = ctk.CTkFrame(container, fg_color="#E3D8CD", corner_radius=10)
        category_frame.pack(padx=20, pady=30, fill="x", expand=False)
        
        create_category_buttons()
    

       
    
        new_category_frame = ctk.CTkFrame(container, fg_color="#EBE0D6")
        new_category_frame.pack(padx=20, pady=10, fill="x", expand=False)
        
        new_category_btn = ctk.CTkButton(new_category_frame, text="Create New Category", font=("Inter", 18, "bold"), 
                                        fg_color="#372724", height=50, width=800, command=add_category)
        new_category_btn.pack(padx=10, pady=5, expand=True) 
 
        
       # product category end


        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(padx=10, pady=20, fill="x", side="bottom")

            # Save Product Button
        save_product_btn = ctk.CTkButton(button_frame, text="Save Product", font=("Inter", 24, "bold"), fg_color="#6F5E5C", height=70, width=200, command=save_product)
        save_product_btn.pack(side="bottom", padx=10)

    
        
        
        return container
      
      



selected_category = None
selected_category_btn = None

def select_category(category, category_btn):
    global selected_category, selected_category_btn
    selected_category = category
    
    # Reset selected button's color
    if selected_category_btn is not None:
        selected_category_btn.configure(fg_color="#6F5E5C", text_color="#EBE0D6")  
    
    #  new selected button
    selected_category_btn = category_btn 
    selected_category_btn.configure(fg_color="#372724", text_color="#EBE0D6") 
    
    print(f"Selected category: {selected_category}")  # For debugging

    
    
def create_category_buttons():
    num_columns = 3 
    for widget in category_frame.winfo_children():
        widget.destroy()  
    
    for idx, category in enumerate(productCategories):
        row = idx // num_columns
        col = idx % num_columns
        
        category_btn = ctk.CTkButton(
            category_frame, 
            text=category, 
            font=("Inter", 18, "bold"), 
            fg_color="#6F5E5C", 
            height=80, 
            width=200
        )
        
        # Fixing late binding by using default parameters in lambda
        category_btn.configure(command=lambda c=category, btn=category_btn: select_category(c, btn))
        
        category_btn.grid(row=row, column=col, padx=10, pady=10, sticky="w")



def add_category():
    
    dialog = ctk.CTkInputDialog(title="Add a new Category", text="Category Name: ")
    new_category = dialog.get_input()

    if new_category and new_category.strip():
        new_category = new_category.strip().capitalize()  

      
        if new_category in productCategories:
            messagebox.showinfo("Duplicate Category", "This category already exists in the list.")
            return

      
        mycursor.execute("SELECT category_name FROM tbl_product_category WHERE LOWER(category_name) = %s", (new_category.lower(),))
        existing_category = mycursor.fetchone()

        if existing_category:
            messagebox.showinfo("Duplicate Category", "This category already exists.")
            return

      
        try:
        
            category_query = "INSERT INTO tbl_product_category (category_name) VALUES (%s)"
            mycursor.execute(category_query, (new_category,))
            db.commit()

           
            productCategories.append(new_category)
            create_category_buttons()
            print(f"Category '{new_category}' added successfully.")
            
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    elif new_category is None:
       
        pass
    else:
        messagebox.show_warning("Invalid Input", "Category name cannot be empty.")

        

def validate_price_entry(new_value):
    # Allow only digits and a single decimal point
    if new_value == "":  # Allow deletion (empty string)
        return True
    try:
        float(new_value)  
        return True
    except ValueError:
        return False  



image_path = None
def prodImage_upload(image_label):
    global image_path

    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])

    if image_path:
        img = Image.open(image_path)
        img = img.resize((500, 500), Image.Resampling.LANCZOS)
        img_ctk = ctk.CTkImage(light_image=img, size=(200, 200))

        image_label.configure(image=img_ctk)
        image_label.image = img_ctk 
        image_label.configure(text="")

    else:
        # No image display
        image_label.configure(image="", text="No Image Selected", text_color="black",
                              font=("Inter", 16))


image_path = None

def save_product():
    global selected_category  
    global image_path
    
    product_name = prodName_entry.get()
    product_price = product_price_entry.get()
    product_description = product_description_entry.get()

    is_new_image = image_path is not None and image_path !=""
    product_image = image_path if image_path and image_path !="" else None

    # Validation checks
    if not product_name or not product_price or not selected_category:
        print("Error: Please enter all required fields.")
        return

    try:
        product_price = float(product_price)
    except ValueError:
        print("Error: Invalid price entered.")
        return

  # Check if image_path is valid before proceeding
    if product_image is None:
        print("Error: No image selected.")
        return

    img_save_path = None  
    insert_product_image =  None
    
    if is_new_image and product_image:
        image_directory = os.path.join(os.path.expanduser("~"), "Documents", "PointOfSales", "imgs")
        
        if not os.path.exists(image_directory):
            os.makedirs(image_directory) 

        try:
            img = Image.open(product_image)
            
            img_save_path = os.path.join(image_directory, f"{product_name}.png")  # Use os.path.join for proper path handling
            img.save(img_save_path)  # Save the image to the specified path

            with open(img_save_path, "rb") as File:
                insert_product_image = File.read()
        except Exception as e:
            print(f"Error saving image: {e}")
            return
    else:
        print("No image is selected")
        
    try:
        #   DALE - UPDATE
        #   For tbl_product_unit
        product_name = prodName_entry.get()

        product_nameForTable = "INSERT INTO tbl_product_unit (unit_name) VALUES (%s)"

        productColumns = (product_name,)

        mycursor.execute(product_nameForTable, productColumns)
        db.commit()


       

        category_query = "INSERT IGNORE INTO tbl_product_category (category_name) VALUES (%s)"
        mycursor.execute(category_query, (selected_category,))
        db.commit()

        mycursor.fetchall()  

        mycursor.execute("SELECT category_id FROM tbl_product_category WHERE category_name = %s", (selected_category,))
        category_id = mycursor.fetchone()[0]
        
        mycursor.fetchall()  
        
        # DALE - UPDATE   
        # Adding of unit name, product category, and unit_id
        unit_name =  product_name
        mycursor.execute("SELECT unit_id FROM tbl_product_unit WHERE unit_name = %s", (unit_name,))    
        
            

        try:
            unit_id = mycursor.fetchone()[0]
        except TypeError:
            unit_id = None  

        # Dale - Inserting of image
     
        product_status = "Available"
        product_query = """
        INSERT INTO tbl_products (product_name, product_price, product_category, product_image, unit_id, product_status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        product_values = (product_name, product_price, selected_category, insert_product_image, unit_id, product_status) 

        mycursor.execute(product_query, product_values)
        db.commit()

        print("Success: Product saved successfully.")

        # DALE - Resetting of image paths
        if img_save_path and os.path.exists(img_save_path):
            os.remove(img_save_path)  # Remove the image file from the system
        print(f"Image {img_save_path} deleted successfully.")

        # Reset img paths to avoid reusing old images
        image_path = None
        img_save_path = None
        insert_product_image = None

        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    
    messagebox.showinfo("Success", "Product saved successfully!")
    clear_fields()



def clear_fields():
    prodName_entry.delete(0, tk.END)
    product_price_entry.delete(0, tk.END)
    product_description_entry.delete(0, tk.END)
    image_label.configure(image="", text="No Image Selected")
    global image_path
    image_path = None


def return_to_main(window):

    from components.containers.products_con import display_products

    for widget in window.winfo_children():
        widget.pack_forget()  
        
    display_products(window)  