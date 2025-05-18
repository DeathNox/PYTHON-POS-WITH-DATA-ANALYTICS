import customtkinter as ctk
from components.containers.global_variable import global_var  # Import global_var


def switch_to_home(window, content_frame, user_id):
    from components.containers.home_con import home_container
    from components.containers.home_con import reset_receipt_container
    reset_receipt_container()
    
    # from ..containers.home_con import setup_receipt_container
    for widget in content_frame.winfo_children():
        widget.destroy()

    
    
    home_frame = home_container(content_frame, user_id=user_id)
    
    home_frame.pack(side="left", fill="both", expand=True)
    # setup_receipt_container(window)  

# components/actions/navigation.py

def switch_to_orders(window, content_frame, user_id):
    
    from components.containers.orders_con import orders_container
    
    for widget in content_frame.winfo_children():
        widget.destroy()
    

    orders_frame = orders_container(content_frame, user_id=user_id)
    

    orders_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

def switch_to_archive(window, content_frame, user_id):
    
    from components.containers.orders_con import orders_container_archive
    
    for widget in content_frame.winfo_children():
        widget.destroy()
    

    orders_frame = orders_container_archive(content_frame, user_id=user_id)
    

    orders_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    
    
def switch_to_prodconfig(window, content_frame, user_id):
    from components.containers.prod_config_con import prod_config_container

    for widget in content_frame.winfo_children():
        widget.destroy()
    
    prod_frame = prod_config_container(content_frame, user_id=user_id)
    prod_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        
        
        


def switch_to_prod_view(window, content_frame, user_id, user_role):
    from components.containers.products_con import display_products

    # Access account_type from global_var
    account_type = global_var.account_type

    # Determine user_role based on account_type (example logic)

    for widget in content_frame.winfo_children():
        widget.destroy()

    display_prod_frame = display_products(content_frame, user_id=user_id, user_role=user_role)

    display_prod_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)


def switch_to_sales_con(window, content_frame, user_id, account_type):
    if account_type != "Employee":  
        from components.containers.sales_con import sales_container
        for widget in content_frame.winfo_children():
            widget.destroy()
            
        sales_frame = sales_container(content_frame, user_id)  # Remove account_type
        sales_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

def switch_to_performance_con(window, content_frame, user_id, account_type):
    if account_type != "Employee":  
        from components.containers.sales_con import performance_container
        for widget in content_frame.winfo_children():
            widget.destroy()
            
        sales_frame = performance_container(content_frame, user_id)  # Remove account_type
        sales_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)


    

def switch_to_inventory_con(window, content_frame, user_id):
    
    from components.containers.inventory_con import InventoryDisplay
    
    for widget in content_frame.winfo_children():
            widget.destroy()
    
    display_inventory_frame = InventoryDisplay(content_frame, user_id)
    
    display_inventory_frame.pack(side="left", fill="both", expand=True,
                            padx=10, pady=10)

    
    
def log_out(window, content_frame, side_panel):
    from components.containers.forms.login_form import login_form_container
    
    for widget in content_frame.winfo_children():
        widget.destroy()
        
    content_frame.pack_forget()
    
    side_panel.pack_forget() 
    login_form_container(window)




