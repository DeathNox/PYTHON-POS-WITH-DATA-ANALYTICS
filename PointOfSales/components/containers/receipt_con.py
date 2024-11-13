import customtkinter as ctk
from decimal import Decimal
from datetime import datetime
from db_setup.db_connect import db, mycursor
from PIL import Image, ImageTk

from components.actions.receipt_payment_method.modal_cash_payment import insert_amount_receive

from components.actions.receipt_payment_method.modal_cash_payment import show_cash_payment_modal

class ReceiptContainer:
    
    def is_valid(self):
        """Check if the receipt container and its frame are valid and not destroyed."""
        return self.frame.winfo_exists()
    
    def get_subtotal(self):
        """Return the current subtotal value."""
        return self.subtotal
    
    def __init__(self, window):
        self.window = window
        
        self.frame = ctk.CTkFrame(window, fg_color="#372724", width=300, height=895, corner_radius=5)
        self.frame.pack_propagate(False)
        self.frame.pack(side="left", fill="y", padx=8, pady=8)
        
        self.lbl = ctk.CTkLabel(self.frame, fg_color="#372724",
                                   text="RECEIPT", font=("Inter", 24, "bold"))
        self.lbl.pack(side="top", pady=(20, 0))
        
    
      
        self.notification_label = ctk.CTkLabel(self.frame, 
                                         text="", 
                                         text_color="white", 
                                         font=("Inter", 16, "bold"),  
                                         fg_color="#372724",
                                         corner_radius=5) 
        self.notification_label.pack(side="top", pady=10) 




        self.receipt_list = ctk.CTkScrollableFrame(self.frame, fg_color="#E4CFBB")
        self.receipt_list.pack(fill="both", expand=True)  

    
        self.items = {}  
        self.subtotal = Decimal('0.00')
        # self.tax_rate = Decimal('0.12')  # user defined
        
        """
        DISCOUNTS:
        PWD - .5%
        student - .20%
        
        """
        
        self.total = Decimal('0.00')
        
        
        
       # ? Payment Method Container / Frame - Start

        self.payment_frame = ctk.CTkFrame(self.frame, fg_color="#EBE0D6", height=90)
        self.payment_frame.pack(fill="x", padx=5, pady=(10, 10))

        # Payment Frame Label (Top Left)
        self.payment_frame_lbl = ctk.CTkLabel(
            self.payment_frame,
            text="Payment Method",
            font=("Inter", 18, "bold"),
            fg_color="transparent",
            text_color="#1E1E1E",  
            compound="left"
        )
        self.payment_frame_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=(3, 5), sticky="w")

      
        self.payment_frame.grid_columnconfigure((0, 1), weight=1)

        # Cash Payment Button
        cash_payment_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/receipt_icons/cash_payment.png")
        resized_icon = cash_payment_btn_icon.resize((30, 30))
        cash_payment_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

        
        self.cash_payment_btn = ctk.CTkButton(
            self.payment_frame,
            text="",
            font=("Inter", 20, "bold"),
            image=cash_payment_btn_icon,
            fg_color="#372724",
            width=100,
            height=35,
            corner_radius=5,
            command=lambda: show_cash_payment_modal(self.get_subtotal(), self.handle_payment)
        )
        
        
        self.cash_payment_btn.grid(row=1, column=0, padx=(25, 10), pady=(5, 15), sticky="e")  
        

        # E-Wallet Payment Button
        e_wallet_payment_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/receipt_icons/e-wallet_payment.png")
        resized_icon = e_wallet_payment_btn_icon.resize((30, 30))
        e_wallet_payment_btn_icon = ctk.CTkImage(dark_image=resized_icon, size=(30, 30))

        self.ewallet_payment_btn = ctk.CTkButton(
            self.payment_frame,
            text="",
            font=("Inter", 20, "bold"),
            image=e_wallet_payment_btn_icon,
            fg_color="#372724",
            width=100,
            height=35,
            corner_radius=5,
        )
        self.ewallet_payment_btn.grid(row=1, column=1, padx=(10, 25), pady=(5, 15), sticky="w")  

        # ? Payment Method Container / Frame - End


        
      
        self.summary_frame = ctk.CTkFrame(self.frame, fg_color="#EBE0D6")
        self.summary_frame.pack(side="bottom", fill="x", padx=5, pady=10)

        formatted_header = f"{'*' * 30}\nORDER RECEIPT\n{'*' * 30}"
        header_label = ctk.CTkLabel(self.receipt_list, text=formatted_header, text_color="black", font=("Inter", 16, "bold"))
        header_label.pack(pady=10)
        
        # Separator lines 
        separator_top = "--------------------------------------"
        separator_label_top = ctk.CTkLabel(self.summary_frame, text=separator_top, text_color="black", font=("Inter", 12, "bold"))
        separator_label_top.pack(anchor="center")
        
        # Labels for subtotal, tax, and total
        self.subtotal_label = ctk.CTkLabel(self.summary_frame, text="SUBTOTAL: PHP 0.00", text_color="black", font=("Inter", 16, "bold"))
        self.subtotal_label.pack(anchor="w", padx=20, pady=10)
        
        # self.tax_label = ctk.CTkLabel(self.summary_frame, text="TAX: PHP 0.00", text_color="black", font=("Inter", 16, "bold"))
        # self.tax_label.pack(anchor="w", padx=20, pady=10)
        
        self.total_label = ctk.CTkLabel(self.summary_frame, text="TOTAL: PHP 0.00", text_color="black", font=("Inter", 16, "bold"))
        self.total_label.pack(anchor="w", padx=20, pady=10)
        
           # Separator lines 
        separator_bottom = "--------------------------------------"
        separator_label_bottom = ctk.CTkLabel(self.summary_frame, text=separator_bottom, text_color="black", font=("Inter", 12, "bold"))
        separator_label_bottom.pack(anchor="center")
        
        
        # Process Order button
        self.process_button = ctk.CTkButton(self.summary_frame, text="PROCESS ORDER", font=("Inter", 20, "bold"), width=20, command=self.process_order, fg_color="#372724")
        self.process_button.pack(pady=20)



       # DALE
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

    def add_item(self, item_name, item_price, quantity):
        """Add or update an item in the receipt container."""
    
        total_price = Decimal(item_price) * quantity

        if item_name in self.items:
            # Update existing item
            existing_item = self.items[item_name]
            existing_item['quantity'] += quantity
            existing_item['total_price'] += total_price  # Update total price
            self.update_item_display(existing_item)
        else:
            # Create a new item frame
            item_frame = ctk.CTkFrame(self.receipt_list, fg_color="#EBE0D6", height=40)
            item_frame.pack(fill="x", pady=2)

            # Create a new item dictionary
            item = {
                'name': item_name,
                'price': Decimal(item_price),  # Ensure price is Decimal
                'quantity': quantity,
                'total_price': total_price,
                'frame': item_frame,  # Store the reference to the frame
            }
          
            # Item Name frame
            item_name_frame_width = 105  # Fixed width for item names
            item_name_frame = ctk.CTkFrame(item_frame, fg_color="#EBE0D6", width=item_name_frame_width)
            item_name_frame.grid(row=0, column=0, padx=(10, 0), sticky="w")

            # Item label
            item_label = ctk.CTkLabel(item_name_frame, text=item_name, text_color="black", font=("Inter", 14, "bold"), width=item_name_frame_width)
            item_label.pack(side="left", anchor="w")  

            # Price frame
            item_price_frame = ctk.CTkFrame(item_frame, fg_color="#EBE0D6", width=100)  
            item_price_frame.grid(row=0, column=1, padx=(10, 10), sticky="e")

            # Price label
            price_label = ctk.CTkLabel(item_price_frame, text=f"PHP {total_price:.2f}", text_color="black", font=("Inter", 14, "bold"))
            price_label.grid(row=0, column=0, padx=(2, 0), sticky="e")  # Align to the right

            # Quantity label
            quantity_label = ctk.CTkLabel(item_frame, text=f"x{quantity}", text_color="black", font=("Inter", 12, "bold"))
            quantity_label.grid(row=0, column=2, padx=(10, 0), sticky="e")

            # Button frame for remove button
            button_frame = ctk.CTkFrame(item_frame, fg_color="#EBE0D6")
            button_frame.grid(row=0, column=3, padx=(15, 5))
            
            # Button to remove the item
            remove_button = ctk.CTkButton(
                button_frame, text=" X ", 
                command=lambda: self.remove_item(item_name, item_frame), 
                fg_color="#D32F2F",
                font=("Inter", 12),
                width=15,
                height=20,
                corner_radius=2
            )
            remove_button.pack(side="right")  

            # Add the new item to the items dictionary
            self.items[item_name] = item

        # Update subtotal and totals
        self.subtotal += total_price
        self.update_totals()

        
 

    
    def remove_item(self, item_name, item_frame, decrement=1):
       
        if item_name in self.items:
            item = self.items[item_name]

            if item['quantity'] > decrement:
                # decrease the quantity
                item['quantity'] -= decrement
                item['total_price'] = item['price'] * item['quantity']
                
                
                self.subtotal -= item['price'] * decrement
                self.update_item_display(item)
            else:
                # remove the item completely pag zero na
                self.subtotal -= item['total_price']
                if item_frame.winfo_exists():
                    item_frame.destroy()
                del self.items[item_name]

            # Update totals
            self.update_totals()


    def update_item_display(self, item):
        """Update the display of an existing item."""
        for widget in item['frame'].winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                if widget.cget("text").startswith("PHP"):
                    widget.configure(text=f"PHP {item['total_price']:.2f}")
                elif widget.cget("text").startswith("x"):
                    widget.configure(text=f"x{item['quantity']}")

    def update_totals(self):
        """Update the subtotal, tax, and total labels."""
        if not self.is_valid():
            print("ReceiptContainer is not valid, skipping total update.")
            return  # Skip updating if the container is not valid

        # tax = self.subtotal * self.tax_rate
        self.total = self.subtotal 
        
        # Update labels if they exist
        if self.subtotal_label.winfo_exists():
            self.subtotal_label.configure(text=f"SUBTOTAL: PHP {self.subtotal:.2f}")
        if self.total_label.winfo_exists():
            self.total_label.configure(text=f"TOTAL: PHP {self.total:.2f}")


    def clear_receipt(self):
        """Clear all items from the receipt container."""
        for item in self.items.values():
            item['frame'].destroy()
        self.items.clear()
        self.subtotal = Decimal('0.00')
        self.update_totals()
        
        
 
    def show_notification(self, message):
        """Display a notification message at the top right corner of the receipt."""
        self.notification_label.configure(text=message, text_color="white")  # Set text color to white
        if "Oops! Your receipt is empty" in message:
            self.notification_label.configure(fg_color="#ED4337")  # Soft red for no items
        else:
            self.notification_label.configure(fg_color="#198754")
        
        # Hide after 5 seconds
        self.notification_label.after(5000, lambda: self.notification_label.configure(text="", fg_color="#372724"))  # Reset color and text
        
    
    
    def process_order(self):
        from .home_con import hide_receipt_container
        if not self.items:
            self.notification_label.configure(fg_color="#ED4337")
            self.show_notification("Oops! Your receipt is empty")
            from .home_con import reset_receipt_container
            self.window.after(2000, reset_receipt_container)
            self.window.after(2000, self.clear_receipt)
            self.window.after(2000, hide_receipt_container)
            return

        show_cash_payment_modal(self.get_subtotal(), self.handle_payment)



    def get_product_id(self, product_name):
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

    def handle_payment(self, amount_received, change_amount, payment_method):
        from .home_con import hide_receipt_container

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

                mycursor.execute(sql, values)
                db.commit()

                insert_amount_receive(amount_received, change_amount, payment_method)

            self.show_notification("Order placed successfully!")
            from .home_con import reset_receipt_container
            self.window.after(2000, reset_receipt_container)
            self.window.after(2000, self.clear_receipt)
            self.window.after(2000, hide_receipt_container)

        except Exception as e:
            print(f"Error processing order: {e}")
            self.show_notification("Error processing order: {e}")
