import customtkinter as ctk
from PIL import Image, ImageTk

from .update_credentials.reset_password import validate_email_for_reset



def Forgot_Password_Container(window):
    
    # Create the main container frame
    main_container = ctk.CTkFrame(window, fg_color="#372724")
    main_container.pack(side="left", fill="both", expand=True)


    logo_image = Image.open('./imgs/mockups/mock3.png') 
    resized_image = logo_image.resize((700, 990)) 
    
    
    logo_image= ImageTk.PhotoImage(resized_image)
    
    

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
        text="No worries! Just enter your email address and username below, and we'll verify it.",
        text_color="#372724",
        font=("Inter", 20)
    )
    subtitle_label.pack(pady=(0, 5), anchor="nw", padx=23)
    
    
    
    

    form_frame = ctk.CTkFrame(right_container, fg_color="#372724")
    form_frame.pack(padx=20, pady=20, fill="x")


   
    
    error_frame = ctk.CTkFrame(form_frame, fg_color="#F1EBEB")
    error_frame.pack(side="top", padx = 28, pady=(45, 45), fill="x")
    error_frame.pack_forget()
    
    error_label = ctk.CTkLabel(error_frame, text="", text_color="#A70C0C", font=("Inter", 20))
    error_label.pack(pady=(10, 10), anchor="w", padx=28)

    close_button = ctk.CTkButton(
    error_frame, 
    text="  X  ", 
    command=lambda: close_error_frame(error_frame),
    fg_color="#A70C0C", 
    text_color="white", 
    font=("Inter", 12),
    width=12,
    height=20,
    corner_radius=2
)
    close_button.place(relx=1.001, y=0, anchor="ne") 



     # email label and entry
    email_label = ctk.CTkLabel(
        form_frame,
        text="Email address",
        fg_color="transparent",
        text_color="#EBE0D6",
        font=("Inter", 28, "bold")
    )
    email_label.pack(pady=(20, 25), padx = 28, anchor="w")

    email_entry = ctk.CTkEntry(
        form_frame,
       
        text_color="#372724",
        fg_color="#EBE0D6",
        font=("Inter", 24, "bold"),
        height=50,
        corner_radius=10
    )
    email_entry.pack(pady=(0, 15), padx = 28, fill="x")

     # email label and entry
    username_label = ctk.CTkLabel(
        form_frame,
        text="Username",
        fg_color="transparent",
        text_color="#EBE0D6",
        font=("Inter", 28, "bold")
    )
    username_label.pack(pady=(20, 25), padx = 28, anchor="w")

    username_entry = ctk.CTkEntry(
        form_frame,
       
        text_color="#372724",
        fg_color="#EBE0D6",
        font=("Inter", 24, "bold"),
        height=50,
        corner_radius=10
    )
    username_entry.pack(pady=(20, 75), padx = 28, fill="x")

    verify_button = ctk.CTkButton(
    right_container,
    text="Verify", 
    fg_color="#6F5E5C",
    text_color="#EBE0D6",
    font=("Inter", 32, "bold"),
    cursor="hand2", 
    height=60,
    command=lambda: handle_verification(username_entry.get(), email_entry.get(), error_frame, error_label, window)
)


    verify_button.pack(pady=(10, 15), padx=20, fill="x")

    login_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    login_frame.pack(pady=(10, 0), padx=20, anchor="nw")  #

      # Login label
    login_label_btn = ctk.CTkLabel(
      login_frame,
      text="Already have an account?",
      text_color="#372724",
      font=("Inter", 24),
      fg_color="transparent"
      )

    login_label_btn.grid(row=0, column=0, padx=(0, 5)) 

      # Login button
    login_btn = ctk.CTkButton(
      login_frame,
      text="Sign in.",
      text_color="#372724",
      font=("Inter", 24, "bold"),
      fg_color="transparent",
      cursor="hand2",
      width=20, 
      command=lambda: redirect_to_login(window)
      )

    login_btn.grid(row=0, column=1, padx=(0, 0))  

    return main_container




def redirect_to_login(window):
      from ..login_form import login_form_container
      for widget in window.winfo_children():
        widget.pack_forget()
        
      login_form_container(window)


def handle_verification(username, email, error_frame, error_label, window):
    from .update_credentials.reset_password_form import Reset_Password_Container
    
  
    if validate_email_for_reset(window, username, email, error_frame, error_label):
       
        for widget in window.winfo_children():
            widget.pack_forget()
        Reset_Password_Container(window, username)  
    else:
       
        error_label.configure(text="Invalid username or email address. Please try again.")
        error_frame.pack(side="top",padx=28, pady=(0, 45))




def close_error_frame(error_frame):
    error_frame.pack_forget()