import customtkinter as ctk



def switch_to_home(window, content_frame):
    from components.containers.home_con import home_container
    from ..containers.home_con import reset_receipt_container
    reset_receipt_container()
    
    # from ..containers.home_con import setup_receipt_container
    for widget in content_frame.winfo_children():
        widget.destroy()

    
    
    home_frame = home_container(content_frame)
    
    home_frame.pack(side="left", fill="both", expand=True)
    # setup_receipt_container(window)  

# components/actions/navigation.py

def switch_to_orders(window, content_frame):
    
    from components.containers.orders_con import orders_container
    
    for widget in content_frame.winfo_children():
        widget.destroy()
    

    orders_frame = orders_container(content_frame)
    

    orders_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    
    
def switch_to_prodconfig(window, content_frame):
    
        from components.containers.prod_config_con import prod_config_container
        # from ..containers.home_con import hide_receipt_container
        # hide_receipt_container()
    
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        
        prod_frame = prod_config_container(content_frame)
        

        prod_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        
        


def switch_to_prod_view(window, content_frame):
    from components.containers.products_con import display_products
    

    for widget in content_frame.winfo_children():
        widget.destroy()
        
    
    display_prod_frame = display_products(content_frame)
    
    display_prod_frame.pack(side="left", fill="both", expand=True,
                            padx=10, pady=10)

        
def switch_to_sales_con(window, content_frame):
    
    from components.containers.sales_con import sales_container
    # from ..containers.home_con import hide_receipt_container
    # hide_receipt_container()
    
    for widget in content_frame.winfo_children():
            widget.destroy()
            
    sales_frame = sales_container(content_frame)
    sales_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    

def switch_to_inventory_con(window, content_frame):
    
    from components.containers.inventory_con import InventoryDisplay
    
    for widget in content_frame.winfo_children():
            widget.destroy()
    
    display_inventory_frame = InventoryDisplay(content_frame)
    
    display_inventory_frame.pack(side="left", fill="both", expand=True,
                            padx=10, pady=10)

    
    
def log_out(window, content_frame, side_panel):
    from ..containers.forms.login_form import login_form_container
    
    for widget in content_frame.winfo_children():
        widget.destroy()
        
    content_frame.pack_forget()
    
    side_panel.pack_forget() 
    login_form_container(window)

 


