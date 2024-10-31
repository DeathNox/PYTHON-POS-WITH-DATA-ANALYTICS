import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk




def login_form_container(window):
    
    # Create the main container frame
    main_container = ctk.CTkFrame(window, fg_color="#372724")
    main_container.pack(side="left", fill="both", expand=True)


    logo_image = Image.open('C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/mockups/mock3.png') 
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
        text="Login",
        text_color="#382724",
        font=("Inter", 64, "bold")
    )
    login_title.pack(pady=(50, 5), anchor="nw", padx=23)

    subtitle_label = ctk.CTkLabel(
        right_container,
        text="Glad to have you here! Let's brew up some great service today",
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


   

     # Username label and entry
    username_label = ctk.CTkLabel(
        form_frame,
        text="Username",
        fg_color="transparent",
        text_color="#EBE0D6",
        font=("Inter", 28, "bold")
    )
    username_label.pack(pady=(65, 25), padx = 28, anchor="w")

    username_entry = ctk.CTkEntry(
        form_frame,
       
        text_color="#372724",
        fg_color="#EBE0D6",
        font=("Inter", 24, "bold"),
        height=50,
        corner_radius=10
    )
    username_entry.pack(pady=(0, 15), padx = 28, fill="x")

    # Password label and entry
    password_label = ctk.CTkLabel(
        form_frame,
        text="Password",
        text_color="#EBE0D6",
        font=("Inter", 28, "bold")
    )
    password_label.pack(pady=(50, 25), padx = 28, anchor="w")

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

    
    # show passworkdkd
    
    def show_password():
    
        if password_entry.cget('show') == '':
            password_entry.configure(show='•')  # Hide the password
            show_password_btn.configure(text='Show Password')  # Change button text
            
        else:
            password_entry.configure(show='')  # Show the password
            show_password_btn.configure() 
    
    show_password_btn = ctk.CTkCheckBox(form_frame, text="Show Password", command=show_password, font=("Inter", 20))
    show_password_btn.pack(pady=(15), padx = (33,0), anchor="w")


    forgot_password_label = ctk.CTkLabel(
        form_frame,
        text="Forgot password?", 
        text_color="#EBE0D6",
        font=("Inter", 20, "underline"),
        cursor="hand2"  
    )
    forgot_password_label.pack(pady=(15, 40), anchor="e", padx=(0, 28))  

    
    login_button = ctk.CTkButton(
        right_container,
        text="Login", 
        fg_color="#6F5E5C",
        text_color="#EBE0D6",
        font=("Inter", 32, "bold"),
        cursor="hand2", 
        height=60,
         command=lambda: handle_login(username_entry.get(), password_entry.get(), window,  error_frame, error_label)
    )
    login_button.pack(pady=(10, 15), padx=20, fill="x")

    sign_up_frame = ctk.CTkFrame(right_container, fg_color="transparent")
    sign_up_frame.pack(pady=(20, 0), padx=20, anchor="nw") 

    # Sign-up label
    signup_label = ctk.CTkLabel(
        sign_up_frame,
        text="Don't have an account?",
        text_color="#372724",
        font=("Inter", 24),
        fg_color="transparent"
    )
    signup_label.grid(row=0, column=0, padx=(0, 5))  

    # Sign-up button
    sign_up_label_btn = ctk.CTkButton(
        sign_up_frame, 
        text="Sign up.",
        text_color="#372724",
        font=("Inter", 24, "bold"),
        fg_color="transparent",
        cursor="hand2",
        width=20,
        command=lambda: redirect_to_signup(window)
    )
    sign_up_label_btn.grid(row=0, column=1, padx=(5, 0)) 

    return main_container



# ! Functionality ng Form - Start


# Function to verify the credentials of the user kung stored ba sa database.
def handle_login(username, password, window, error_frame, error_label):
    
    from components.actions.verify_credentials import verify_user_credentials
    
    success, message = verify_user_credentials(username, password)

    if success:
        print("Login successful!")
        redirect_to_home(window)
        error_frame.pack_forget() 
        error_label.configure(text="")  
    else:
        error_label.configure(text="") 
        if message == "password_incorrect":
            error_label.configure(text="Sorry, that password isn't right. Please try again.")
        elif message == "username_not_found":
            error_label.configure(text="Sorry, we couldn't find an account with that username.")

        error_frame.place(x=100, y=10)  
        
        
content_frame = None


# After logging in, this will trigger:
def redirect_to_home(window):
    global content_frame  
    
    # Hides all existing widgets
    for widget in window.winfo_children():
        widget.pack_forget()
    
    from components.containers.home_con import home_container
    from components.containers.sidepanel import side_panel, sidepanel_options
    
    # Create and pack the side panel
    side_panel_frame = side_panel(window)  
    side_panel_frame.pack(side="left", fill="y", padx=8, pady=8)  

    # Create and pack the content frame
    content_frame = home_container(window)  # Assign to the global variable
    content_frame.pack(side="left", fill="both", expand=True) 
    
    # Call sidepanel_options with the new content_frame
    sidepanel_options(side_panel_frame, window, content_frame)



def redirect_to_signup(window):
    
    from .sign_up_form import sign_up_form_container
    for widget in window.winfo_children():
        widget.pack_forget()
        
    sign_up_form_container(window)



# ! Functionality ng Form - End
