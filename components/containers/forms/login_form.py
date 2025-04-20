import customtkinter as ctk
from PIL import Image, ImageTk




def login_form_container(window):
    
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
    forgot_password_label.bind("<Button 1>", lambda event: redirect_to_forgot_password(window, event))
    
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

# Add a global variable to track failed attempts
failed_attempts = 0
MAX_ATTEMPTS = 3  # Define the maximum number of allowed attempts

def handle_login(username, password, window, error_frame, error_label):
    global failed_attempts  # Use the global variable to track attempts
    from components.containers.forms.validations.verify_credentials import verify_user_credentials
    
    success, message, user_id, account_type, logged_in_user = verify_user_credentials(username, password)

    if success:
        print("Login successful!")
        print(f"User ID: {user_id}, Employee Name: {logged_in_user}, Account Type: {account_type}")  # You now have the user_id and account_type
        redirect_to_home(window, user_id, account_type)  # Pass account_type here
        error_frame.pack_forget() 
        error_label.configure(text="")  
        failed_attempts = 0  # Reset the counter on successful login
    else:
        failed_attempts += 1  # Increment the counter on failed login
        remaining_attempts = MAX_ATTEMPTS - failed_attempts  # Calculate remaining attempts
        error_label.configure(text="") 
        
        if message == "password_incorrect":
            error_label.configure(text=f"Sorry, that password isn't right. You have {remaining_attempts} attempt(s) left.")
        elif message == "username_not_found":
            error_label.configure(text=f"Sorry, we couldn't find an account with that username. You have {remaining_attempts} attempt(s) left.")

        error_frame.place(x=100, y=10)

        # Check if the failed attempts have reached the maximum
        if failed_attempts >= MAX_ATTEMPTS:
            print("Too many failed attempts. Closing the application.")
            window.quit()  # Close the application
        
        
content_frame = None


# After logging in, this will trigger:
def redirect_to_home(window, user_id, account_type):
    global content_frame  
    
    # Hides all existing widgets
    for widget in window.winfo_children():
        widget.pack_forget()
    
    from components.containers.home_con import home_container
    from components.containers.side_panel.sidepanel import create_side_panel, sidepanel_options
    
    side_panel_frame = create_side_panel(window)  # Call the renamed function
    side_panel_frame.pack(side="left", fill="y", padx=8, pady=8)  

    content_frame = home_container(window, user_id)  
    content_frame.pack(side="left", fill="both", expand=True) 
    
    sidepanel_options(side_panel_frame, window, content_frame, user_id=user_id, account_type=account_type)

   
    print(f"Logged in user ID: {user_id}")  



def redirect_to_signup(window):
    
    from .sign_up_form import sign_up_form_container
    for widget in window.winfo_children():
        widget.pack_forget()
        
    sign_up_form_container(window)

def redirect_to_forgot_password(window, event=None):
    
    from .validations.forgot_password import Forgot_Password_Container
    
    for widget in window.winfo_children():
        widget.pack_forget()
        
    Forgot_Password_Container(window)



# ! Functionality ng Form - End
