from tkinter import filedialog
from PIL import ImageTk, Image
from io import BytesIO
import customtkinter as ctk 
from db_setup.db_connect import db

def change_product_image(product_name, container):
    """Allow the user to select a new product image and update it in the database."""
    # Open a file dialog to select a new image
    image_path = filedialog.askopenfilename(
        title="Select Product Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if image_path:
        try:
            # Open the new image
            with open(image_path, "rb") as file:
                image_data = file.read()

            # Update the image in the database
            mycursor = db.cursor()
            sql = "UPDATE tbl_products SET product_image = %s WHERE product_name = %s"
            mycursor.execute(sql, (image_data, product_name))
            db.commit()
            mycursor.close()

            # Update the image on the GUI
            new_image = Image.open(image_path)
            new_image.thumbnail((150, 150))  # Resize the image
            new_image_ctk = ImageTk.PhotoImage(new_image)

            # Update the image display
            for widget in container.winfo_children():
                widget.destroy()  # Clear previous image
            new_image_label = ctk.CTkLabel(container, image=new_image_ctk, text="")
            new_image_label.grid(row=0, column=0, padx=10, pady=10)

        except Exception as e:
            print(f"Error updating product image: {e}")