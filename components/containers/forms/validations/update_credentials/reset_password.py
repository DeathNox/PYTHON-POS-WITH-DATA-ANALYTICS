import bcrypt
from db_setup.db_connect import db
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox

def validate_email_for_reset(window, username, email, error_frame, error_label):

    cursor = db.cursor()
    try:
        query = "SELECT email_address FROM tbl_users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result and result[0] == email:
            
            redirect_to_forgot_password_form(window, username)
            messagebox.showinfo("Validation Success", "Your email address has been successfully verified.")

         
        else:
            
            error_label.configure(text="Invalid username or email address. Please try again.")
            error_frame.pack(side="top",padx=28, pady=(0, 45))
            return False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return False
    finally:
        cursor.close()




def update_password(username, new_password):

    # Update user password in the database with a hashed version.
  
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    cursor = db.cursor()  
    try:
        query = "UPDATE tbl_users SET hashed_password = %s WHERE username = %s"
        cursor.execute(query, (hashed_password, username))
        db.commit() 
    finally:
        cursor.close()  


def redirect_to_forgot_password_form(window, username):
      from .reset_password_form import Reset_Password_Container
      for widget in window.winfo_children():
        widget.pack_forget()
        
      Reset_Password_Container(window, username)