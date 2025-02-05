import tkinter as tk
import customtkinter as ctk
from db_setup.db_connect import db, mycursor
from PIL import Image
from components.frames.header import HeaderFrame
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

def orders_container(window, user_id):
  

    
    container = ctk.CTkFrame(window, fg_color="#EBE0D6", width=1275, height=900, corner_radius=2)
    container.pack_propagate(False)
    container.pack(side="left", fill="both", expand=True, padx=10, pady=50)

    header_frame = HeaderFrame(container, user_id=user_id)

 
    orders_container_lbl = ctk.CTkLabel(
        header_frame,
        text="Orders List",
        font=("Inter", 32, "bold"),
        text_color="#EBE0D6",
        compound="left"
    )
    orders_container_lbl.pack(anchor="nw", pady=20, padx=25)

    
    metrics_frame = ctk.CTkFrame(container, fg_color="#EBE0D6", height=600, width=200,
                                 corner_radius=15)
    metrics_frame.pack(fill="x", pady=5)

     # Initialize metric labels
    global total_income_label, completed_orders_label, orders_in_progress_label
    total_orders_value = get_total_orders()
    orders_in_progress_value = get_orders_in_progress()
    completed_orders_value = get_completed_orders()

    create_metric_card(metrics_frame, "             Total Orders              ", total_orders_value, 0)
    orders_in_progress_label = create_metric_card(metrics_frame, "             Orders in Progress              ", orders_in_progress_value, 1)
    total_income_label = create_metric_card(metrics_frame, "                Sales Today              ", f"PHP {get_total_income_today()}", 3)
    completed_orders_label = create_metric_card(metrics_frame, "              Completed Orders              ", completed_orders_value, 2)

   
    card_frame = ctk.CTkFrame(container, fg_color="#372724", corner_radius=10)
    card_frame.pack(padx=20, pady=50, fill="both", expand=True)

  
    header_frame = ctk.CTkFrame(card_frame, fg_color="#372724")
    header_frame.pack(fill="x")

    headers = ["Order #", "Date", "Item Name", "Quantity", "Total", "Status", "Action"]
    col_widths = [150, 200, 200, 150, 200, 200, 200]

    for idx, header in enumerate(headers):
        label = ctk.CTkLabel(
            header_frame,
            text=header,
            font=("Inter", 20, "bold"),
            text_color="white",
            width=col_widths[idx]
        )
        label.grid(row=0, column=2 * idx, padx=5, pady=15)

        if idx < len(headers) - 1:
            ctk.CTkFrame(header_frame, fg_color="white", width=1, height=40).grid(row=0, column=2 * idx + 1, pady=10)

    
    orders_scrollable_frame = ctk.CTkScrollableFrame(card_frame, fg_color="#F4F4F4", height=500)
    orders_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # fetch data from the database
    fetch_orders(orders_scrollable_frame, col_widths)

    return container

def create_metric_card(frame, title, value, col):
    cards_width = 305
    cards_height = 150


    card = ctk.CTkFrame(frame, fg_color="#60514E", corner_radius=10, width=cards_width, height=cards_height)  
    card.grid(row=0, column=col, padx=(35, 15), pady=(20, 0))

    
    label_title_frame = ctk.CTkFrame(card, fg_color="#60514E", width=cards_width)
    label_title_frame.pack(fill="both", expand=False, pady=(8, 0))  
    
    
   # Title label
    label_title = ctk.CTkLabel(label_title_frame, text=title, font=("Inter", 18, "bold", "italic"), fg_color="#60514E", text_color="white", width=cards_width-10)
    label_title.pack(pady=(0, 0), padx=(0,10), anchor="w")  

     # Value label
    label_value = ctk.CTkLabel(card, text=value, font=("Inter", 36, "bold"), fg_color="#60514E", text_color="white",  width=cards_width-30)
    label_value.pack(pady=(20, 30), padx=(15, 0), anchor="w")  
    
    
    return label_value

def get_total_orders():
  
    sql = "SELECT COUNT(*) FROM tbl_purchase_order"
    mycursor.execute(sql)
    total_orders = mycursor.fetchone()[0]
    return total_orders

def get_orders_in_progress():
  
    sql = "SELECT COUNT(*) FROM tbl_purchase_order WHERE order_status = 'In Progress'"
    mycursor.execute(sql)
    in_progress_orders = mycursor.fetchone()[0]
    return in_progress_orders

def get_completed_orders():
  
    sql = "SELECT COUNT(*) FROM tbl_purchase_order WHERE order_status = 'Completed'"
    mycursor.execute(sql)
    completed_orders = mycursor.fetchone()[0]
    return completed_orders

def get_total_income():
    sql = "SELECT SUM(sub_total) FROM tbl_purchase_order WHERE order_status = 'Completed'"
    mycursor.execute(sql)
    total_income = mycursor.fetchone()[0] or 0
    # print(f"Total Income Calculated: {total_income}")  # Debugging line
    return total_income

def get_total_income_today():
    sql = "SELECT SUM(sub_total) FROM tbl_sales WHERE DATE(order_date) = CURDATE()"
    mycursor.execute(sql)
    total_income = mycursor.fetchone()[0] or 0
    # print(f"Total Income Calculated: {total_income}")  # Debugging line
    return total_income

# DALE - GET TOTAL INCOME
def get_profit():
    sql = "SELECT SUM(sub_total) FROM tbl_purchase_order WHERE order_status = 'Completed'"
    mycursor.execute(sql)
    total_income = mycursor.fetchone()[0] or 0
    total_income_20_percent = total_income * Decimal(0.2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Calculate 20% of total income
    # print(f"20% of Total Income: {total_income_20_percent}")  # Debugging line
    return total_income_20_percent


def fetch_orders(frame, col_widths):
    try:
        sql = "SELECT purchase_order_id, order_date, item_name, quantity, sub_total, order_status FROM tbl_purchase_order ORDER BY purchase_order_id DESC"
        mycursor.execute(sql)
        orders = mycursor.fetchall()

        if not orders:
            print("No orders found.")
            return

        status_options = ["Pending", "In Progress", "Completed"]
        for row_idx, order in enumerate(orders, start=1):
            order_id, order_date, item_name, quantity, sub_total, order_status = order

            row_bg_color = "#F2F1ED"  

           
            ctk.CTkLabel(
                frame,
                text=str(order_id),
                text_color="black",
                font=("Inter", 18),
                width=col_widths[0],
                fg_color=row_bg_color
            ).grid(row=row_idx, column=0, padx=5, pady=(10, 0))

            ctk.CTkLabel(
                frame,
                text=order_date.strftime("%Y-%m-%d %H:%M:%S"),
                text_color="black",
                font=("Inter", 18),
                width=col_widths[1],
                fg_color=row_bg_color
            ).grid(row=row_idx, column=2, padx=0, pady=(10, 0))

            ctk.CTkLabel(
                frame,
                text=item_name,
                text_color="black",
                font=("Inter", 18),
                width=col_widths[2],
                fg_color=row_bg_color
            ).grid(row=row_idx, column=4, padx=10, pady=(10, 0))

            ctk.CTkLabel(
                frame,
                text=str(quantity),
                text_color="black",
                font=("Inter", 18),
                width=col_widths[3],
                fg_color=row_bg_color
            ).grid(row=row_idx, column=6, padx=5, pady=(10, 0))

            ctk.CTkLabel(
                frame,
                text=f"PHP {sub_total:.2f}",
                text_color="black",
                font=("Inter", 18),
                width=col_widths[4],
                fg_color=row_bg_color
            ).grid(row=row_idx, column=8, padx=5, pady=(10, 0))


            status_dropdown = ctk.CTkOptionMenu(
                frame,
                values=status_options,
                command=lambda status, oid=order_id, old_status=order_status: update_order_status(oid, status, old_status, frame, col_widths),
                text_color="white",
                font=("Inter", 16, "bold"),
                width=col_widths[5],
                fg_color="#6F5E5C"
            )
            status_dropdown.set(order_status)
            
            # Disable the dropdown if the status is "Completed"
            if order_status == "Completed":
                status_dropdown.configure(state="disabled")
            
            status_dropdown.grid(row=row_idx, column=10, padx=(5,20), pady=10, sticky="ew")
            
              # Cancel Button
            cancel_btn_icon = Image.open("./imgs/icons/cancel_icon.png")
            resized_icon = cancel_btn_icon.resize((30, 30))  
            cancel_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

            action_cancel_button = ctk.CTkButton(
            frame,
            text="", 
            image=cancel_icon,
            command=lambda oid=order_id, frame=frame, col_widths=col_widths: cancel_order(oid, frame, col_widths),
            font=("Inter", 16, "bold"),
            fg_color="#FF5733",
            text_color="white",
            width=40,  
            height=40  
                )

            action_cancel_button.grid(row=row_idx, column=16, padx=5, pady=10)
            

            # View Button
            view_btn_icon = Image.open("./imgs/icons/view_icon.png")
            resized_icon = view_btn_icon.resize((30, 30))  
            view_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

            action_view_button = ctk.CTkButton(
                frame, 
                text="",  
                image=view_icon,
                command=lambda oid=order_id: view_order_details(oid),
                font=("Inter", 16, "bold"),
                fg_color="#007BFF",
                text_color="white",
                width=40,  
                height=40  
            )
            action_view_button.grid(row=row_idx, column=12, padx=(20, 10), pady=10)

            # Print Button
            print_btn_icon = Image.open("./imgs/icons/print_icon.png")
            resized_icon = print_btn_icon.resize((30, 30))  # Same size for uniformity
            print_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

            action_print_button = ctk.CTkButton(
                frame,
                text="", 
                image=print_icon,
                command=lambda oid=order_id: print_order(oid),
                font=("Inter", 16, "bold"),
                fg_color="#388E3C",
                text_color="white",
                width=40,  
                height=40  
            )
            action_print_button.grid(row=row_idx, column=14, padx=5, pady=10)
            
            
            
            
            
            
            

                # Add a horizontal line below each row
            ctk.CTkFrame(frame, fg_color="black", height=1).grid(row=row_idx + 1, column=0, columnspan=15, sticky="ew", pady=(0, 10))


    except Exception as e:
        print(f"Error fetching orders: {e}")
        


def cancel_order(order_id, frame, col_widths):
    try:
        sql = "DELETE FROM tbl_payments WHERE purchase_order_id = %s"
        mycursor.execute(sql, (order_id,))
        db.commit()

        sql = "DELETE FROM tbl_purchase_order WHERE purchase_order_id = %s"
        mycursor.execute(sql, (order_id,))
        db.commit()

        print(f"Order {order_id} and related payments have been canceled.")
        
        # Refresh the display: clear the frame and reload orders
        for widget in frame.winfo_children():
            widget.grid_forget()  

        fetch_orders(frame, col_widths)  
        
    except Exception as e:
        print(f"Error canceling order: {e}")
        
        

def view_order_details(order_id):
    """
    Function to handle the action when the "View" button is clicked.
    Opens a modal displaying order details as a receipt.
    """
  
    receipt_modal = ctk.CTkToplevel()
    receipt_modal.title("Order Details")
    receipt_modal.geometry("400x600")  
    receipt_modal.resizable(False, False)
    receipt_modal.grab_set()  


    receipt_frame = ctk.CTkFrame(receipt_modal, fg_color="white", corner_radius=10)
    receipt_frame.pack(fill="both", expand=True, padx=20, pady=20)

   
    try:
        sql = "SELECT purchase_order_id, order_date, item_name, quantity, sub_total, order_status FROM tbl_purchase_order WHERE purchase_order_id = %s"
        mycursor.execute(sql, (order_id,))
        order_details = mycursor.fetchone()

        if order_details:
            order_id, order_date, item_name, quantity, sub_total, order_status = order_details
            
            # Header section (Centered)
            header_label_1 = ctk.CTkLabel(
                receipt_frame, 
                text="=====================================", 
                font=("Inter", 18), 
                text_color="black"
            )
            header_label_1.pack(pady=2)
            
            header_label_2 = ctk.CTkLabel(
                receipt_frame, 
                text="RECEIPT", 
                font=("Inter", 20, "bold"),  
                text_color="black"
            )
            header_label_2.pack(pady=2)

            # Line separator
            order_label = ctk.CTkLabel(
                receipt_frame, 
                text=f"ORDER #: {order_id}", 
                font=("Inter", 18), 
                text_color="black"
            )
            order_label.pack(pady=2)
            
            separator_label = ctk.CTkLabel(
                receipt_frame, 
                text="=====================================", 
                font=("Inter", 18), 
                text_color="black"
            )
            separator_label.pack(pady=2)

            # Order Details
            date_label = ctk.CTkLabel(
                receipt_frame, 
                text=order_date.strftime('%Y-%m-%d %H:%M:%S'), 
                font=("Inter", 18),  
                text_color="black"
            )
            date_label.pack(pady=2)

            item_label = ctk.CTkLabel(
                receipt_frame, 
                text=f" {quantity}x  {item_name} ......... PHP {sub_total:.2f}", 
                font=("Inter", 20),  
                text_color="black"
            )
            item_label.pack(anchor="w", padx=10)

            # price_label = ctk.CTkLabel(
            #     receipt_frame, 
            #     text=f"PHP {sub_total:.2f}", 
            #     font=("Inter", 20),  
            #     text_color="black"
            # )
            # price_label.pack(anchor="e", padx=10)

            # Separator for total amount
            total_separator = ctk.CTkLabel(
                receipt_frame, 
                text="\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", 
                font=("Inter", 18), 
                text_color="black"
            )
            total_separator.pack(pady=5)

            # Total amount
            total_label = ctk.CTkLabel(
                receipt_frame, 
                text="TOTAL AMOUNT", 
                font=("Inter", 20, "bold"),  
                text_color="black"
            )
            total_label.pack(anchor="w", padx=10)

            total_value_label = ctk.CTkLabel(
                receipt_frame, 
                text=f"PHP {sub_total:.2f}", 
                font=("Inter", 20), 
                text_color="black"
            )
            total_value_label.pack(anchor="e", padx=10)

            # Final separator
            final_separator = ctk.CTkLabel(
                receipt_frame, 
                text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", 
                font=("Inter", 18), 
                text_color="black"
            )
            final_separator.pack(pady=5)

            # Footer with separator lines
            footer_label_1 = ctk.CTkLabel(
                receipt_frame, 
                text="\n=====================================\n", 
                font=("Inter", 18), 
                text_color="black"
            )
            footer_label_1.pack(pady=2)

            footer_label_2 = ctk.CTkLabel(
                receipt_frame, 
                text="THANK YOU", 
                font=("Inter", 20, "bold"), 
                text_color="black"
            )
            footer_label_2.pack(pady=2)

            footer_label_3 = ctk.CTkLabel(
                receipt_frame, 
                text="\n=====================================", 
                font=("Inter", 18), 
                text_color="black"
            )
            footer_label_3.pack(pady=2)
            
              # Close button
            close_button = ctk.CTkButton(receipt_modal, text="Close", command=receipt_modal.destroy, font=("Inter", 16, "bold"), width=100, fg_color="#D73030", text_color="white")
            close_button.pack(pady=(10, 20))

        else:
            
            error_label = ctk.CTkLabel(receipt_frame, text="Order details not found.", font=("Inter", 14, "bold"), text_color="red")
            error_label.pack(pady=20)

    except Exception as e:
        print(f"Error fetching order details: {e}")



def print_order(order_id):
    """
    Function to handle the action when the "Print" button is clicked.
    Generates a PDF file of the order details and saves it.
    """


    
    import tempfile
    import webbrowser
    from fpdf import FPDF
    # pip install fpdf


    try:
        # Fetch order details
        sql = "SELECT purchase_order_id, order_date, item_name, quantity,  unit_price, sub_total, order_status FROM tbl_purchase_order WHERE purchase_order_id = %s"
        mycursor.execute(sql, (order_id,))
        order_details = mycursor.fetchone()

        if not order_details:
            print("Order details not found.")
            return


        order_id, order_date, item_name,  quantity, unit_price, sub_total, order_status = order_details

        # temporary PDF file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf_path = temp_file.name

  
        receipt_width_mm = 80
        receipt_height_mm = 120 

        # Generate PDF content using FPDF with custom page size
        pdf = FPDF(orientation='P', unit='mm', format=(receipt_width_mm, receipt_height_mm))
        pdf.add_page()
        
        

        # Header section (Centered)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 5, txt="=====================================", ln=True, align='C')
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(60, 5, txt="RECEIPT", ln=True, align='C')

        # Line separator
        pdf.set_font('Arial', '', 9)
        pdf.cell(60, 6, txt=f"ORDER #: {order_id}", ln=True, align='C')
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 5, txt="=====================================", ln=True, align='C')
       
        # Order Details
        pdf.set_font('Arial', '', 8)
        pdf.ln(3)  # Line break
       
        pdf.cell(60, 5, txt=f"{order_date.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        
        
        pdf.set_font('Arial', '', 10)
        # Set up the row for item details
        pdf.cell(120, 10, txt=f"{quantity}x     {item_name}", ln=False) 
        pdf.cell(0, 10, txt=f"PHP {unit_price:.2f}", ln=True, align="R")  
        pdf.ln(5) 

        
        pdf.set_font('Arial', '', 10)
        pdf.cell(60, 5, txt="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", ln=True, align='C')

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(100, 6, txt="TOTAL AMOUNT", align='L')  # Left-aligned cell with some width

        pdf.cell(0, 6, txt=f"PHP {sub_total:.2f}", ln=True, align='R')  # Right-aligned cell with the rest of the width

        pdf.set_font('Arial', '', 10)
        pdf.cell(60, 5, txt="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ", ln=True, align='C')

        # Footer with separator lines
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(60, 5, txt="=====================================", ln=True, align='C')
        pdf.cell(60, 6, txt="THANK YOU", ln=True, align='C')
        pdf.cell(60, 5, txt="=====================================", ln=True, align='C')
        
  
        pdf.output(temp_pdf_path)

   
        webbrowser.open(temp_pdf_path)

        print(f"Order {order_id} displayed and sent to printer.")

    except Exception as e:
        print(f"Error printing order: {e}")
    
    
def set_status_color(status):
    if status == "Pending":
        return "#6F5E5C"
    elif status == "In Progress":
        return "#6F5E5C"
    elif status == "Completed":
        return "#6F5E5C"
    else:
        return "black"
    
    
    
def get_order_details(order_id):
    """
    Fetches product details associated with the given order ID.
    """
    sql = """
        SELECT product_id, item_name, product_category, quantity, unit_price, sub_total
        FROM tbl_purchase_order
        WHERE purchase_order_id = %s
    """
    mycursor.execute(sql, (order_id,))
    result = mycursor.fetchone()
    if result:
        return {
            "product_id": result[0],
            "item_name": result[1],
            "category": result[2],
            "quantity": result[3],
            "unit_price": result[4],
            "sub_total": result[5]
        }
    else:
        raise ValueError(f"No details found for Order ID {order_id}")

def update_order_status(order_id, new_status, old_status, frame, col_widths):
    """
    Updates the order status in the database and refreshes the metrics if the status is changed.
    """
    try:
        # Update the order status in the database
        sql = "UPDATE tbl_purchase_order SET order_status = %s WHERE purchase_order_id = %s"
        mycursor.execute(sql, (new_status, order_id))
        db.commit()
        print(f"Order {order_id} updated to {new_status}")

        # Retrieve the order subtotal and details for updating metrics
        order_subtotal = get_order_subtotal(order_id)
        print(f"Order Subtotal for Order ID {order_id}: {order_subtotal}")
        
        order_details = get_order_details(order_id)

        # Update metrics
        update_metrics_on_status_change(
            old_status, 
            new_status, 
            order_subtotal, 
            order_details["product_id"], 
            order_details["item_name"], 
            order_details["category"], 
            order_details["quantity"], 
            order_details["unit_price"], 
            order_details["sub_total"]
        )

        # Refresh the orders to update the dropdown list
        for widget in frame.winfo_children():
            widget.grid_forget()  
        fetch_orders(frame, col_widths)

    except Exception as e:
        print(f"Error updating order status: {e}")


def update_metrics_on_status_change(old_status, new_status, order_subtotal, product_id, item_name, category, quantity, unit_price, sub_total):
    orders_in_progress_value = get_orders_in_progress()
    completed_orders_value = get_completed_orders()

    orders_in_progress_label.configure(text=f"{orders_in_progress_value}")
    completed_orders_label.configure(text=f"{completed_orders_value}")

    # adjust total income based on status change
    current_income = get_total_income_today()  
    print(f"Current Total Income: {current_income}")

    # Adjust total income and insert into tbl_sales if status changes to 'Completed'
    if old_status == "Completed" and new_status in ["Pending", "In Progress"]:
        new_income = current_income - order_subtotal
        total_income_label.configure(text=f"PHP {new_income:,.2f}")
        print(f"Income adjusted by subtracting {order_subtotal}: New Income: {new_income}")

    elif old_status in ["Pending", "In Progress"] and new_status == "Completed":
        # Insert sales record into tbl_sales
        insert_into_sales(product_id, item_name, category, quantity, unit_price, sub_total)
        
        # Update total income after marking as completed
        new_income = get_total_income_today()
        total_income_label.configure(text=f"PHP {new_income:,.2f}")
        print(f"Updated Total Income after marking as completed: {new_income}")

    # debugging print statements
    print(f"Updated Income after status change from '{old_status}' to '{new_status}': {total_income_label.cget('text')}")



def get_order_subtotal(order_id):
    """
    Fetches the subtotal of a specific order by purchase order id
    """
    sql = "SELECT sub_total FROM tbl_purchase_order WHERE purchase_order_id = %s"
    mycursor.execute(sql, (order_id,))
    subtotal = mycursor.fetchone()[0] or 0  
    print(f"Fetched Subtotal for Order ID {order_id}: {subtotal}")
    return subtotal


# DALE - Nilakay ko to kase ang nahirapan ako mag import ng functions from class container xd
def get_product_category(self, product_name):
        """Get the product category from the database based on the product name."""
        try:
            sql = "SELECT product_category FROM tbl_products WHERE product_name = %s"
            mycursor.execute(sql, (product_name,))
            result = mycursor.fetchone()
            
            if result:
                return result[0]  # Return the product category
            else:
                raise ValueError(f"The product category for '{product_name}' is not found.")
        
        except Exception as e:
            print(f"Error fetching product category: {e}")
            return None   
        
def process_order(self):
        from .home_con import hide_receipt_container
        """Handle the process order button click and save the order to the database."""
        if not self.items:  # Check if there are no items in the receipt
            
            self.notification_label.configure(fg_color="#ED4337")
            self.show_notification("Oops! Your receipt is empty")
            
            from .home_con import reset_receipt_container
            
            
            self.window.after(2000, reset_receipt_container)
            
            
            self.window.after(2000, self.clear_receipt)
            
            self.window.after(2000, hide_receipt_container)
            
            
            return  
        
        
        try:
            for item in self.items.values():
                product_id = self.get_product_id(item['name']) 
                item_name = item['name']
                quantity = item['quantity']
                unit_price = item['price']
                sub_total = item['total_price']
                order_status = "Pending"

                category = self.get_product_category(item_name) or 'Unknown Category' 


                sql = """
                    INSERT INTO tbl_purchase_order (product_id, quantity, unit_price, sub_total, order_date, order_status, item_name, product_category) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (product_id, quantity, unit_price, sub_total, datetime.now(), order_status, item_name, category)


                # Execute the query and commit the transaction
                mycursor.execute(sql, values)
                # DALE - Wrap the tbl_sales query into this function

                db.commit()
            
            # Show the notification
            self.show_notification("Order placed successfully!")  # Display notification
            
            from .home_con import reset_receipt_container
            
            
            self.window.after(2000, reset_receipt_container)
            
            
            self.window.after(2000, self.clear_receipt)
            
            self.window.after(2000, hide_receipt_container)
            
            
            
            

        except Exception as e:
            print(f"Error processing order: {e}")
            self.show_notification("Error processing order.")  # Display error notification

    # DALE - query for tbl_sales
def insert_into_sales(product_id, item_name, category, quantity, unit_price, sub_total):
    """Insert a sales record into tbl_sales."""
    try:
        # Fetch the last inserted purchase_order_id
        mycursor.execute("SELECT purchase_order_id FROM tbl_purchase_order ORDER BY purchase_order_id DESC LIMIT 1")
        last_purchase_order_id = mycursor.fetchone()[0]

        # Insert the sales record, omitting the invoice_id as it's auto-incremented
        sql2 = "INSERT INTO tbl_sales (sales_id, product_id, product_name, product_category, quantity, unit_price, sub_total) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values2 = (last_purchase_order_id, product_id, item_name, category, quantity, unit_price, sub_total)
        mycursor.execute(sql2, values2)
        db.commit()
    except Exception as e:
        print(f"Error inserting into sales: {e}")
        db.rollback()


def get_product_id(product_name):
        """Get the product_id from the database given the product name."""
        try:
            sql = "SELECT product_id FROM tbl_products WHERE product_name = %s"
            mycursor.execute(sql, (product_name,))
            result = mycursor.fetchone()
            if result:
                return result[0]
            else:
                raise ValueError(f"Product ID for {product_name} not found.")
        except Exception as e:
            print(f"Error fetching product ID: {e}")
            return None