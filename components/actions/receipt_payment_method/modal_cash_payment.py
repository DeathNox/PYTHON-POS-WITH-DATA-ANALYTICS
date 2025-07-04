import customtkinter as ctk
import tkinter as tk
from db_setup.db_connect import db, mycursor


def insert_amount_receive(amount_receive, change_amount, payment_method):
    # Combined query that inserts amount, change, payment method, and the latest purchase_order_id
    query = """
    INSERT INTO tbl_payments (amount_received, change_amount, payment_method, purchase_order_id, sub_total)
    VALUES (%s, %s, %s, (SELECT purchase_order_id FROM tbl_purchase_order ORDER BY purchase_order_id DESC LIMIT 1), (SELECT sub_total FROM tbl_purchase_order ORDER BY purchase_order_id DESC LIMIT 1));
    """
    
    try:
        # Execute the combined query
        mycursor.execute(query, (amount_receive, change_amount, payment_method))
        
        # Commit the transaction
        db.commit()
        
        print("Amount received, change, payment method, and latest purchase_order_id inserted successfully.")
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        print(f"Failed to insert data: {e}")




def show_cash_payment_modal(orders_total, on_payment_confirmed):
    from main import CenterWindowToDisplay

    # Modal window
    modal = ctk.CTkToplevel()
    modal.title("Cash Payment")
    modal.geometry(CenterWindowToDisplay(modal, 450, 480, modal._get_window_scaling()))
    modal.resizable(False, False)
    modal.configure(fg_color="#30211E")

    modal.grid_rowconfigure(0, weight=1)
    modal.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(modal, fg_color="#EBE0D6")
    container.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="nsew")
    container.grid_columnconfigure(0, weight=1)

    # Modal label
    modal_lbl = ctk.CTkLabel(
        container,
        text="Cash Payment",
        text_color="#1E1E1E",
        font=("Inter", 26, "bold")
    )
    modal_lbl.grid(row=0, column=0, pady=(20, 10), padx=(30, 10), sticky='w')

    orders_total = float(orders_total)

    # Total amount entry frame 
    total_amount_entry_frame = ctk.CTkFrame(
        container,
        fg_color="#F4F4F4",
        corner_radius=5,
        width=300,
        height=40
    )
    total_amount_entry_frame.grid(row=1, column=0, padx=(30, 30), pady=(10, 5), sticky="ew")
    total_amount_entry_frame.grid_columnconfigure(0, weight=1)

    # "Total" label
    total_label = ctk.CTkLabel(
        total_amount_entry_frame,
        text="Total",
        font=("Inter", 16, "bold"),
        text_color="#2C2C2C"
    )
    total_label.grid(row=0, column=0, padx=(10, 10), pady=(5, 0), sticky="w")

    # Total amount label
    total_amount_label = ctk.CTkLabel(
        total_amount_entry_frame,
        text=f"PHP {orders_total:.2f}",
        font=("Inter", 32, "bold"),
        fg_color="#F4F4F4",
        text_color="#1E1E1E"
    )
    total_amount_label.grid(row=1, column=0, padx=(90, 10), pady=(5, 10), sticky="w")

    # Frame and labels for "Amount Received"
    amount_received_frame = ctk.CTkFrame(
        container,
        fg_color="#F4F4F4",
        corner_radius=5,
        width=300,
        height=60
    )
    amount_received_frame.grid(row=2, column=0, padx=(30, 30), pady=(10, 5), sticky="ew")
    amount_received_frame.grid_columnconfigure((0, 1, 2), weight=1)  
    

    # "Amount Received" label
    amount_received_lbl = ctk.CTkLabel(
        amount_received_frame,
        text="Amount Received",
        font=("Inter", 16, "bold"),
        text_color="#2C2C2C"
    )
    amount_received_lbl.grid(row=0, column=0, padx=(10, 5), pady=(5, 0), sticky="w")

    # "PHP" label
    php_lbl = ctk.CTkLabel(
        amount_received_frame,
        text="PHP",
        font=("Inter", 32, "bold"),
        text_color="#1E1E1E"
    )
    php_lbl.grid(row=1, column=0, padx=(30, 5), pady=(5, 10), sticky="w")

    # Define a validation function
    def validate_numeric_input(value):
        if value == "" or value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit()):
            return True
        return False

    # Register the validation function
    validate_command = modal.register(validate_numeric_input)

    # Entry for the amount received
    amount_received_entry = ctk.CTkEntry(
        amount_received_frame,
        font=("Inter", 32, "bold"),
        fg_color="#E9E6E6",
        text_color="#1E1E1E",
        width=120,
        border_width=1,
        validate="key",
        validatecommand=(validate_command, "%P")  # %P passes the current value of the entry
    )
    amount_received_entry.grid(row=1, column=1, padx=(5, 10), pady=(5, 10), sticky="w")

    # Optional
    # amount_received_entry.insert(0, "0.00") 

    def on_submit():
        try:
            amount_receive = float(amount_received_entry.get())
            payment_method = "Cash"
            change_amount = calculated_change

            # Check if amount_received is enough
            if amount_receive < orders_total:
                print("Insufficient amount received. Please enter enough to cover the total.")
                return  # Exit the function without calling on_payment_confirmed

            # Call the function if payment is sufficient
            on_payment_confirmed(amount_receive, change_amount, payment_method)
            modal.destroy()

        except ValueError:
            print("Invalid input. Please enter a numeric amount.")




    # Frame and labels for change amount
    change_amount_frame = ctk.CTkFrame(
        container,
        fg_color="#F4F4F4",
        corner_radius=5,
        width=300,
        height=60
    )
    change_amount_frame.grid(row=3, column=0, padx=(30, 30), pady=(10, 5), sticky="ew")
    change_amount_frame.grid_columnconfigure((0, 1, 2), weight=1)  
    
    
    
    # "Change" label
    change_label = ctk.CTkLabel(
        change_amount_frame,
        text="Change",
        font=("Inter", 16, "bold"),
        text_color="#2C2C2C"
    )
    change_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky="w")

    # "PHP" label
    currency_label = ctk.CTkLabel(
        change_amount_frame,
        text="PHP",
        font=("Inter", 24, "bold"),
        text_color="#1E1E1E"
    )
    currency_label.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky="w")

    # Change amount label
    change_amount_lbl = ctk.CTkLabel(
        change_amount_frame,
        text="0.00",  
        font=("Inter", 26, "bold"),
        text_color="#1E1E1E"
    )
    change_amount_lbl.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky="e")

    
    
    
     # Button container
    button_container = ctk.CTkFrame(container, fg_color="#EBE0D6")
    button_container.grid(row=5, column=0, columnspan=2, padx=(30, 0), pady=(50, 10), sticky="ew")
        
    button_container.grid_columnconfigure(0, weight=1)
    
    
    def calculate_change(event):
        global calculated_change  # Access the global variable
        
        try:
            amount_received = float(amount_received_entry.get())
            
            # Calculate change
            calculated_change = amount_received - orders_total
            change_text = f"{calculated_change:.2f}" if calculated_change >= 0 else "Insufficient"
            change_amount_lbl.configure(text=change_text)
            
        except ValueError:
            change_amount_lbl.configure(text="Invalid Input")
            calculated_change = 0.0  


    # Cancel Button
    cancel_btn = ctk.CTkButton(
            button_container,
            text="Cancel",
            command=modal.destroy,
            font=("Inter", 20, "bold"),
            width=100,
            fg_color="#F5F5F5",
            text_color="#2C2C2C"
        )
    cancel_btn.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="e")

    confirm_payment_btn = ctk.CTkButton(
            button_container,
            text="Confirm Payment",
            font=("Inter", 20, "bold"),
            width=100,
            fg_color="#2B9B43",
            text_color="#F5F5F5",
            command=on_submit
        )
    confirm_payment_btn.grid(row=0, column=1, padx=(20, 20), pady=10, sticky="e")

    # Bind Enter key 
    amount_received_entry.bind("<KeyRelease>", calculate_change)