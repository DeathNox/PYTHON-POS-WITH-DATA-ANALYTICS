import bcrypt
from db_setup.db_connect import db
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox


def Reset_Password_Container(window, username):
    
    # Create the main container frame
    main_container = ctk.CTkFrame(window, fg_color="#372724")
    main_container.pack(side="left", fill="both", expand=True)

    logo_image = Image.open('./imgs/mockups/mock3.png') 
    resized_image = logo_image.resize((700, 990)) 
    logo_image = ImageTk.PhotoImage(resized_image)

    logo_label = ctk.CTkLabel(main_container, image=logo_image, text="")
    logo_label.image = logo_image 
    logo_label.pack(pady=20)

    title_label = ctk.CTkLabel(
        main_container,
        text="Coffee Shop",
        fg_color="#EBE0D6",
        text_color="#382724",
        font=("Inter", 36, "bold")
    )
    title_label.pack(pady=10)

    right_container = ctk.CTkFrame(window, fg_color="#EBE0D6")
    right_container.pack(side="right", fill="both", expand=True)

    # Title and subtitle for the login form
    login_title = ctk.CTkLabel(
        right_container,
        text="Forgot your Password?",
        text_color="#382724",
        font=("Inter", 64, "bold")
    )
    login_title.pack(pady=(50, 5), anchor="nw", padx=23)

    subtitle_label = ctk.CTkLabel(
        right_container,
        text="Enter a new password below to reset your account password.",
        text_color="#372724",
        font=("Inter", 20)
    )
    subtitle_label.pack(pady=(0, 5), anchor="nw", padx=23)

    form_frame = ctk.CTkFrame(right_container, fg_color="#372724")
    form_frame.pack(padx=20, pady=20, fill="x")

    error_frame = ctk.CTkFrame(form_frame, fg_color="#F1EBEB")
    error_frame.pack(padx = 28, pady=(45, 45), fill="x")
    error_frame.pack_forget()
    
    error_label = ctk.CTkLabel(error_frame, text="", text_color="#A70C0C", font=("Inter", 20))
    error_label.pack(pady=(10, 10), anchor="w", padx=28)

    close_button = ctk.CTkButton(
        error_frame, 
        text="  X  ", 
        command=lambda: error_frame.place_forget(),
        fg_color="#A70C0C", 
        text_color="white", 
        font=("Inter", 12),
        width=12,
        height=20,
        corner_radius=2
    )
    close_button.place(relx=1.001, y=0, anchor="ne") 

    # Password label and entry
    new_password_label = ctk.CTkLabel(
        form_frame,
        text="New Password",
        text_color="#EBE0D6",
        font=("Inter", 28, "bold")
    )
    new_password_label.pack(pady=(20, 25), padx = 28, anchor="w")

    password_entry = ctk.CTkEntry(
        form_frame,
        text_color="#372724",
        fg_color="#EBE0D6",
        font=("Inter", 24),
        height=50,
        corner_radius=10,
        show='•'
    )
    password_entry.pack(pady=(0, 10), padx = 28, fill="x")

    # Password label and entry for confirmation
    confirm_password_label = ctk.CTkLabel(
        form_frame,
        text="Confirm password",
        text_color="#EBE0D6",
        font=("Inter", 28, "bold")
    )
    confirm_password_label.pack(pady=(20, 25), padx = 28, anchor="w")

    confirm_password_entry = ctk.CTkEntry(
        form_frame,
        text_color="#372724",
        fg_color="#EBE0D6",
        font=("Inter", 24),
        height=50,
        corner_radius=10,
        show='•'
    )
    confirm_password_entry.pack(pady=(0, 10), padx = 28, fill="x")

    # Show password functionality
    def show_password():
        if password_entry.cget('show') == '':
            password_entry.configure(show='•')  
            show_password_btn.configure(text='Show Password') 
        else:
            password_entry.configure(show='')  
            show_password_btn.configure(text='Hide Password')  
    
    show_password_btn = ctk.CTkCheckBox(form_frame, text="Show Password", command=show_password, font=("Inter", 20))
    show_password_btn.pack(pady=(15, 60), padx = (33,0), anchor="w")

    def reset_password(username, password_entry, confirm_password_entry, error_label, error_frame, window):
      new_password = password_entry.get()
      confirm_password = confirm_password_entry.get()

      # Validate passwords
      if new_password != confirm_password:
            error_label.configure(text="Passwords do not match. Please try again.")
            error_frame.pack(pady=(10, 10), fill="x")
      elif len(new_password) < 8:  # Check for password length
            error_label.configure(text="Password must be at least 8 characters.")
            error_frame.pack(pady=(10, 10), fill="x")
      else:
            # Update password in the database
            try:
                  update_password(username, new_password)  # Pass the username here
                  messagebox.showinfo("Success", "Your password has been reset successfully.")
                  redirect_to_login(window)
            
            except Exception as e:
                  messagebox.showerror("Error", f"An error occurred: {e}")


    reset_button = ctk.CTkButton(
    right_container,
    text="Reset Password", 
    fg_color="#6F5E5C",
    text_color="#EBE0D6",
    font=("Inter", 32, "bold"),
    cursor="hand2", 
    height=60,
    command=lambda: reset_password(username, password_entry, confirm_password_entry, error_label, error_frame, window)  #
)

    reset_button.pack(pady=(10, 15), padx=20, fill="x")

    return main_container


def update_password(username, new_password):
 
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    cursor = db.cursor()  
    try:
      
        query = "UPDATE tbl_users SET password = %s WHERE username = %s"
        cursor.execute(query, (hashed_password, username))
        db.commit()  
    except Exception as e:
        db.rollback()  
        raise e
    finally:
        cursor.close()  



def redirect_to_login(window):
      from ...login_form import login_form_container
      for widget in window.winfo_children():
        widget.pack_forget()
        
      login_form_container(window)