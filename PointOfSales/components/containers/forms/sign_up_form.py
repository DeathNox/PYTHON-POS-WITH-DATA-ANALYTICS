
import customtkinter as ctk
import tkinter as  tk 
from PIL import Image, ImageTk



def sign_up_form_container(window):
      
      
      
      main_container = ctk.CTkFrame(window, fg_color="#372724")
      main_container.pack(side="left", fill="both", expand=True)

      logo_image = Image.open("./imgs/mockups/Mockup 2.png")
      resized_image = logo_image.resize((800, 990))
      
      logo_image = ImageTk.PhotoImage(resized_image)
      
      logo_label = ctk.CTkLabel(main_container, image=logo_image, text="")
      logo_label.image = logo_image 
      logo_label.pack(pady=20)
      
      

      right_container = ctk.CTkFrame(window, fg_color="#EBE0D6")
      right_container.pack(side="right", fill="both", expand=True)
      
      
      signup_title = ctk.CTkLabel(
            right_container,
            text="Create an account",
            text_color="#382724",
            font=("Inter", 36, "bold")
            
      )
      
      signup_title.pack(pady=(50, 5), anchor = "nw", padx=24)
      
      
      subtitle_label = ctk.CTkLabel (
            
            right_container,
            text="Get started and pour success into every sale!  Create your account now.",
            text_color="#372724",
            font=("Inter", 20)
      )
      
      subtitle_label.pack(pady=(0, 5), anchor="nw", padx=(25, 25 ))
      
      form_frame = ctk.CTkFrame(right_container, fg_color="#372724")
      form_frame.pack(padx=20, pady=20, fill="x")
      
      firstname_label = ctk.CTkLabel(
            form_frame,
            text="First name",
            fg_color="transparent",
            text_color="#EBE0D6",
            font=("Inter", 22, "bold")
      )
      firstname_label.grid(row=0, column=0, pady=(25, 10), padx=(28, 10), sticky="w")  # Align to the left

      firstname_entry = ctk.CTkEntry(
            form_frame,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
             height=45,
            corner_radius=5,
            width=300  #
      )
      firstname_entry.grid(row=1, column=0, pady=(0, 15), padx=(28, 28), sticky="ew")  

    
      lastname_label = ctk.CTkLabel(
            form_frame,
            text="Last name",
            fg_color="transparent",
            text_color="#EBE0D6",
            font=("Inter", 22, "bold")
      )
      lastname_label.grid(row=0, column=1, pady=(25, 10), padx=(10, 28), sticky="w")  

      lastname_entry = ctk.CTkEntry(
            form_frame,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
           height=45,
             corner_radius=5,
            width=300 
    )
      lastname_entry.grid(row=1, column=1, pady=(0, 15), padx=(10, 28), sticky="ew") 
      
      
       
      email_address_label = ctk.CTkLabel(
            form_frame,
            text="Email address",
            text_color="#EBE0D6",
            font=("Inter", 22, "bold")
      )
      email_address_label.grid(row=2, column=0, pady=(0, 10), padx=(28, 10), sticky="w", columnspan=2)  

      email_address_entry = ctk.CTkEntry(
            form_frame,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
             height=45,
            corner_radius=5,
            width=600  
      )
      email_address_entry.grid(row=3, column=0, pady=(0, 15), padx=(25, 25), sticky="ew", columnspan=2) 

      username_label = ctk.CTkLabel(
            form_frame,
            text="Username",
            text_color="#EBE0D6",
            font=("Inter", 22, "bold")
      )
      
      
      username_label.grid(row = 4, column = 0, pady=(0, 10), padx=(28, 10), sticky="w", columnspan=2 )
      
      username_entry = ctk.CTkEntry (
            form_frame,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
             height=45,
             corner_radius=5,
            width=600 
            
      )
      
      username_entry.grid(row=5, column=0, pady=(0, 15), padx=(25, 25), sticky="ew", columnspan=2)
      
      
      password_label = ctk.CTkLabel(
            
            form_frame,
            text="Password",
            text_color = "#EBE0D6",
            font=("Inter", 22, "bold")
      )
      
      password_label.grid(row=6, column = 0, pady=(0, 10), padx=(28, 10), sticky="w", columnspan=2 )
      
      password_entry = ctk.CTkEntry(
            form_frame,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
            height=45,
             corner_radius=5,
            width=300 ,
            show='•'
      )
      
      password_entry.grid(row = 7, column=0, pady=(0, 15), padx=(25, 25), sticky="ew", columnspan=2)


      def show_password():
    
        if password_entry.cget('show') == '':
            password_entry.configure(show='•')  
            show_password_btn.configure(text='Show Password')  
            
        else:
            password_entry.configure(show='')  
            

      show_password_btn = ctk.CTkCheckBox(form_frame, text_color="#EBE0D6", text="Show Password", command=show_password, font=("Inter", 22))
      show_password_btn.grid(row=8, column = 1, pady=(0, 0), padx=(100, 10), columnspan=2)

      phone_number_label = ctk.CTkLabel(
            
            form_frame,
            text = "Phone number",
            text_color = "#EBE0D6",
            font=("Inter", 22, "bold")
            
      )
      
      # Phone Number Entry
      phone_number_label.grid(row = 9, column = 0, pady=(0, 0), padx=(28, 10), sticky="w", columnspan=2)

      phone_number_entry = ctk.CTkEntry (
            
            form_frame,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
            height=45,
             corner_radius=5,
            width=500

      )
      
      phone_number_entry.grid(row = 10, column=0, pady=(0, 15), padx=(25, 25))
      
      # Role Choice 
      role_choice_label = ctk.CTkLabel (
            form_frame,
            text="Role", 
            text_color="#EBE0D6",
            font=("Inter", 22, "bold")
      )
      
      role_choice_label.grid(row = 9, column=1, pady=(25, 10), padx=(15, 10), sticky="w")
      
      
      role_options = ['Employee', 'Admin']
      
      role_choice_optMenu = ctk.CTkOptionMenu(
            form_frame,
            values=role_options,
            text_color="#372724",
            fg_color="#EBE0D6",
            font=("Inter", 22),
            height=45,
            corner_radius=5,
            width=350

      )
      
      role_choice_optMenu.grid(row=10, column=1, pady=(0, 15), padx=(5, 15))
      
      
      
      # Create account button / Sign up
      create_account_btn = ctk.CTkButton (
            right_container,
            text = "Sign Up",
            fg_color="#6F5E5C",
            text_color="#EBE0D6",
            font=("Inter", 26, "bold"),
            cursor="hand2", 
            height=60,
            command=lambda: handle_signup(
            username_entry, 
            password_entry, 
            firstname_entry, 
            lastname_entry, 
            phone_number_entry, 
            role_choice_optMenu, 
            email_address_entry,
            form_frame, 
            window
    )
            
      )
      
      create_account_btn.pack(pady=(10, 15), padx=20, fill="x")
      
      

      form_frame.grid_columnconfigure(0, weight=1)
      form_frame.grid_columnconfigure(1, weight=1)
      
      
  
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






def redirect_to_login(window):
      from .login_form import login_form_container
      for widget in window.winfo_children():
        widget.pack_forget()
        
      login_form_container(window)
  
    
    
    
    
def handle_signup(username_entry, password_entry, firstname_entry, lastname_entry, phone_number_entry, role_choice_optMenu, email_address_entry, form_frame, window):
      
    from components.actions.create_account import create_user_account



    username = username_entry.get().strip()
    password = password_entry.get().strip()
    firstname = firstname_entry.get().strip()
    lastname = lastname_entry.get().strip()
    email_address = email_address_entry.get().strip()
    phone_number = phone_number_entry.get().strip()
    role_choice = role_choice_optMenu.get()


    def show_error_message(message, form_frame):
        error_frame = ctk.CTkFrame(form_frame, fg_color="#F8D7DA")  
        error_frame.grid(padx=28, pady=(10, 10), sticky="nsew")  
        error_label = ctk.CTkLabel(error_frame, text=message, text_color="#721C24", font=("Inter", 20, "bold"))
        error_label.grid(pady=(10, 10), padx=(10, 80))

        form_frame.after(3000, lambda: error_frame.grid_forget())  
        
        
    
    if not username or not password or not firstname or not lastname or not email_address or not phone_number or not role_choice:
        show_error_message("All fields are required. Please fill out the form.", form_frame)
        return
 
    success = create_user_account(username, password, firstname, lastname, phone_number, role_choice, email_address,)
    
    
    def show_success_message(message, form_frame):
      success_frame = ctk.CTkFrame(form_frame, fg_color="#D6EFD6")  
      success_frame.grid(padx=28, pady=(45, 45), sticky="nsew")  
      success_label = ctk.CTkLabel(success_frame, text=message, text_color="#4B8A4B", font=("Inter", 20))
      success_label.grid(pady=(10, 10), padx=10)  

      
      form_frame.after(1200, lambda: (success_frame.grid_forget(), redirect_to_login(window)))

    if success:  
        show_success_message("Account created successfully!", form_frame)
        
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        firstname_entry.delete(0, 'end')
        lastname_entry.delete(0, 'end')
        email_address_entry.delete(0, 'end')
        phone_number_entry.delete(0, 'end')
        role_choice_optMenu.set('') 
        
        

    
    
