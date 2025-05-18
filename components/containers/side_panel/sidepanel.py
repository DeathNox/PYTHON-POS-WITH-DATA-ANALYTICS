from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as CTk
from components.containers.side_panel.navigation import switch_to_orders, switch_to_home, switch_to_sales_con, \
    switch_to_prod_view, switch_to_inventory_con, log_out, switch_to_performance_con

from components.containers.global_variable.global_var import account_type

is_expanded = False
side_panel = None  

# Global button and icon variables
menu_btn, orders_btn, view_products_btn, sales_btn, inventory_btn, signout_btn = [None] * 6
ctk_menu_icon = ctk_orders_icon = ctk_product_icon = ctk_sales_btn_icon = ctk_inventory_btn_icon = ctk_signout_icon = None

def create_side_panel(window):  # Renamed function
    global side_panel, menu_btn, orders_btn, view_products_btn, sales_btn, inventory_btn, signout_btn  
    global ctk_menu_icon, ctk_orders_icon, ctk_product_icon, ctk_sales_btn_icon, ctk_inventory_btn_icon, ctk_signout_icon  

    side_panel = tk.Frame(window, bg="#E4CFBB", width=220)  # Increased from 185 to 220
    side_panel.pack_propagate(False)
    side_panel.pack(side="left", fill="y", padx=8, pady=8)

    # Add logo
    company_logo = Image.open("./imgs/sidepanel_icons/dummylogo.png")
    resized_logo = company_logo.resize((100, 100))
    company_logo = ImageTk.PhotoImage(resized_logo)
    logo_label = tk.Label(side_panel, image=company_logo, bg="#E4CFBB", cursor="hand2")
    logo_label.bind("<Button-1>", lambda event: toggle_side_panel(window, event)) 
    logo_label.image = company_logo
    logo_label.pack(pady=10)

    # Label to toggle side panel width
    label = tk.Label(side_panel, bg="#E4CFBB")
    label.pack(pady=10)

    return side_panel


def sidepanel_options(side_panel, window, content_frame, user_id, account_type):
    global menu_btn, orders_btn, view_products_btn, sales_btn, inventory_btn, signout_btn 
    global ctk_menu_icon, ctk_orders_icon, ctk_product_icon, ctk_sales_btn_icon, ctk_inventory_btn_icon, ctk_signout_icon  
  
        
    

    # START -  Pang navigate to other interfaces.

    def switch_to_orders_frame():
        switch_to_orders(window, content_frame, user_id=user_id)

    def switch_to_home_frame():
        switch_to_home(window, content_frame, user_id=user_id)

    def switch_to_view_prod_frame():
        switch_to_prod_view(window, content_frame, user_id=user_id, user_role=account_type)

    def log_out_frame():
        log_out(window, content_frame, side_panel)

    # END -  Pang navigate to other interfaces.

    # START - home btn styling
    menu_btn_icon = Image.open("./imgs/sidepanel_icons/menu_icon_light.png")
    resized_icon = menu_btn_icon.resize((30, 40))
    ctk_menu_icon = CTk.CTkImage(dark_image=resized_icon, size=(25, 30))

    menu_btn = CTk.CTkButton(side_panel, text="Home", image=ctk_menu_icon,
                             font=("Inter", 18, "bold"),
                             compound="left", fg_color="#372724",
                             text_color="#EBE0D6", width=1000,
                             command=switch_to_home_frame)

    menu_btn.pack(pady=10, padx=10)
    # END - home btn styling

    # START - orders_history btn styling
    orders_btn_icon = Image.open("./imgs/sidepanel_icons/orders_icon_light.png")
    resized_icon = orders_btn_icon.resize((30, 40))
    ctk_orders_icon = CTk.CTkImage(dark_image=resized_icon, size=(20, 30))

    orders_btn = CTk.CTkButton(side_panel, text=" Orders", image=ctk_orders_icon, 
                               font=("Inter", 18, "bold"),
                               compound="left",
                               fg_color="#372724",
                               text_color="#EBE0D6", width=1000,
                               command=switch_to_orders_frame)

    orders_btn.pack(pady=10, padx=10)
    # END- orders_history styling

    # START - Products styling btn
    products_btn_icon = Image.open("./imgs/sidepanel_icons/products_icon.png")
    resized_icon = products_btn_icon.resize((30, 40))
    ctk_product_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))

    view_products_btn = CTk.CTkButton(side_panel, text="Products", image=ctk_product_icon,
                                      font=("Inter", 18, "bold"),
                                      compound="left",
                                      fg_color="#372724",
                                      text_color="#EBE0D6", width=1000,
                                      command=switch_to_view_prod_frame)

    view_products_btn.pack(pady=10, padx=10)
    # END - products styling btn

    # == START Sales styling btn === 
    if account_type != "Employee":
        sales_btn_icon = Image.open("./imgs/sidepanel_icons/sales_icon.png")
        resized_icon = sales_btn_icon.resize((30, 40))
        ctk_sales_btn_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))

        sales_btn = CTk.CTkButton(side_panel, text="Sales", image=ctk_sales_btn_icon,
                                  font=("Inter", 18, "bold"),
                                  compound="left", fg_color="#372724",
                                  text_color="#EBE0D6", width=1000,
                                  command=lambda: switch_to_sales_con(window, content_frame, user_id, account_type))

        sales_btn.pack(pady=10, padx=10)
        
    if account_type != "Employee":
        performance_btn_icon = Image.open("./imgs/sidepanel_icons/performance_1.png")
        resized_icon = performance_btn_icon.resize((30, 40))
        ctk_performance_btn_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))

        performance_btn = CTk.CTkButton(side_panel, text="Performance", image=ctk_performance_btn_icon,
                                  font=("Inter", 18, "bold"),
                                  compound="left", fg_color="#372724",
                                  text_color="#EBE0D6", width=1200,
                                  command=lambda: switch_to_performance_con(window, content_frame, user_id, account_type))

        performance_btn.pack(pady=10, padx=10)
    # == END Sales styling btn ===

    # == START Inventory styling btn ==
    # == END Inventory styling btn

    # START - signout btn styling
    signout_btn_icon = Image.open("./imgs/sidepanel_icons/sign_out_icon_light.png")
    resized_icon = signout_btn_icon.resize((30, 40))

    ctk_signout_icon = CTk.CTkImage(dark_image=resized_icon, size=(25, 30))

    signout_btn = CTk.CTkButton(side_panel, text="Sign Out", image=ctk_signout_icon,
                                font=("Inter", 18, "bold"),
                                compound="left",
                                fg_color="#372724",
                                text_color="#EBE0D6", width=1000,
                                command=go_to_log_out_handler)

    signout_btn.pack(side="bottom", pady=10, padx=10)
    # END - signout btn styling

def update_side_panel_text(show_text):
    global menu_btn, orders_btn, view_products_btn, sales_btn, inventory_btn, signout_btn 
    global ctk_menu_icon, ctk_orders_icon, ctk_product_icon, ctk_sales_btn_icon, ctk_inventory_btn_icon, ctk_signout_icon  

    if show_text:
        # Show text and hide image  
        menu_btn.configure(text="Home", image="")
        orders_btn.configure(text="Orders", image="")
        view_products_btn.configure(text="Products", image="")
        inventory_btn.configure(text="Inventory", image="")
        sales_btn.configure(text="Sales", image="")
        signout_btn.configure(text="Sign Out", image="")
    else:
        # Show only icons and hide text
        menu_btn.configure(text="", image=ctk_menu_icon)
        orders_btn.configure(text="", image=ctk_orders_icon)
        view_products_btn.configure(text="", image=ctk_product_icon)
        inventory_btn.configure(text="", image=ctk_inventory_btn_icon)
        sales_btn.configure(text="", image=ctk_sales_btn_icon)
        signout_btn.configure(text="", image=ctk_signout_icon)
        

def toggle_side_panel(window, event=None):
    global is_expanded  

    current_width = side_panel.winfo_width()

  
    large_width = 175
    small_width = 65

 
  
    is_expanded = not is_expanded

 
    if is_expanded:
        # Expand side panel
        animate_side_panel(side_panel, current_width, large_width)
    else:
        # Collapse side panel
        animate_side_panel(side_panel, current_width, small_width)

def animate_side_panel(panel, start_width, end_width):
    def change_width(current_width, target_width):
        if current_width != target_width:
      
            width_diff = target_width - current_width
            step = 7 if width_diff > 0 else -7
            new_width = current_width + step

            if (step > 0 and new_width > target_width) or (step < 0 and new_width < target_width):
                new_width = target_width

            panel.config(width=new_width)
            panel.after(10, change_width, new_width, target_width)  

    # Start the animation process
    change_width(start_width, end_width)
    
def go_to_log_out_handler():
      try:
            log_out_handler()
      except Exception as e:
            print(f"Error @ redirect_to_sign_in: {e}")
            
def log_out_handler():
    try:
        from components.containers.forms.login_form import login_form_container

        # Check if side_panel exists and is valid
        if side_panel is None or not side_panel.winfo_exists():
            print("Error: side_panel does not exist or has already been destroyed.")
            return

        # Destroy the current window's children
        root = side_panel.winfo_toplevel()  # Get the existing Tk instance
        for widget in root.winfo_children():
            widget.destroy()

        # Load the login form in the existing Tk instance
        sign_in_frame = login_form_container(root)
        sign_in_frame.pack()

    except Exception as e:
        print(f"Error in log_out: {e}")