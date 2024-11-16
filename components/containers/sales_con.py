import customtkinter as ctk
from ..actions.db.fetch_top_sellers import get_top_selling_items, get_top_selling_item_details
from ..actions.db.fetch_sales import get_avg_order
from components.actions.data_analytics.data_visualization import open_product_modal_pieChart, display_line_chart
from .orders_con import get_total_income, get_profit
from ..actions.db.fetch_product_categories import get_product_categories


# Function to create a metric card
def create_metric_card(frame, title, value, row, col):
    cards_width = 305
    cards_height = 150


    card = ctk.CTkFrame(frame, fg_color="#60514E", corner_radius=10, width=cards_width, height=cards_height)  
    card.grid(row=row, column=col, padx=(30, 0), pady=10)

    label_title_frame = ctk.CTkFrame(card, fg_color="#60514E", width=cards_width)
    label_title_frame.pack(fill="both", expand=False, pady=(8, 0))  

    # Title label
    label_title = ctk.CTkLabel(label_title_frame, text=title, font=("Inter", 18, "bold", "italic"), fg_color="#60514E", text_color="white", width=cards_width-10)
    label_title.pack(pady=(0, 0), padx=(0,10), anchor="w")  

    # Value label
    label_value = ctk.CTkLabel(card, text=value, font=("Inter", 36, "bold"), fg_color="#60514E", text_color="white",  width=cards_width-30)
    label_value.pack(pady=(20, 30), padx=(15, 0), anchor="w")  

    return label_value

def sales_container(window, user_id):
    # Main container frame for sales overview
    container = ctk.CTkFrame(window, fg_color="#EBE0D6", width=1275, height=900, corner_radius=2)
    container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Configure the grid layout for the container
    container.grid_columnconfigure(0, weight=2)  # for analytics_frame
    container.grid_columnconfigure(1, weight=1)  # for best_sellers_frame
    container.grid_columnconfigure(2, weight=2)  # for pie_chart
    container.grid_rowconfigure(3, weight=1)     # Row for both frames

    # Header frame for the sales overview title
    header_frame = ctk.CTkFrame(container, fg_color="#372724", width=1275, height=70, corner_radius=5)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Sales overview label
    sales_container_lbl = ctk.CTkLabel(
        header_frame,
        text="Sales Overview",
        font=("Inter", 32, "bold"),
        text_color="#EBE0D6",
        compound="left"
    )
    sales_container_lbl.pack(anchor="nw", pady=10, padx=25)

    # Frame displaying sales cards
    cards_display_frame = ctk.CTkFrame(container, fg_color="#EBE0D6")
    cards_display_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    # Metric cards side by side in the same row
    # DALE - ADDING OF SALES 
    total_sales = get_total_income()  # Call the function to get the total sales value
    profit = get_profit()
    display_value = f"{profit:.2f}"  # Format the total sales value as a string with two decimal places

    avg_order = get_avg_order()
    display_value1 = f"{avg_order:.2f}"  # Format the total sales value as a string with two decimal places


    create_metric_card(cards_display_frame, "TOTAL SALES REVENUE", total_sales, 0, 0)
    create_metric_card(cards_display_frame, "SALES TODAY", total_sales, 0, 1)
    create_metric_card(cards_display_frame, "TOTAL INCOME", display_value, 0, 2)
    create_metric_card(cards_display_frame, "AVERAGE ORDER VALUE", display_value1, 0, 3)

    # Container for analytics
    analytics_frame = ctk.CTkFrame(container, fg_color="#372724", height=425, width=400, corner_radius=10)
    analytics_frame.grid(row=2, column=0, padx=(50, 50), pady=(2, 20), sticky="nsew")

    # Analytics header
    analytics_frame_header = ctk.CTkFrame(analytics_frame, fg_color="#372724")
    analytics_frame_header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    # Title label for the analytics frame
    header_label = ctk.CTkLabel(analytics_frame_header, text="CASH FLOW",
                                font=("Inter", 18, "bold"),
                                fg_color="#372724", text_color="#FFFFFF", width=370)
    header_label.grid(row=0, column=0, padx=50, pady=(10, 10))

    # Prevent grid propagation to maintain sizing
    analytics_frame.grid_propagate(0)

    # Analytics Data Frame (for displaying cash flow)
    analytics_data_frame = ctk.CTkFrame(analytics_frame, fg_color="#F1EBEB", height=350, width=580)
    analytics_data_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    # Add a label with the message "Click to view"
    click_to_view_label = ctk.CTkLabel(analytics_data_frame, text="Click to view", fg_color="#F1EBEB", text_color="#000000")
    click_to_view_label.place(relx=0.5, rely=0.5, anchor="center")

    # Event handler to display the line chart
    def on_analytics_frame_click(event):
        display_line_chart(analytics_data_frame)

    # Bind the click event to the analytics_data_frame
    analytics_data_frame.bind("<Button-1>", on_analytics_frame_click)

    # Grids
    analytics_frame.grid_rowconfigure(1, weight=1)
    analytics_frame.grid_columnconfigure(0, weight=1)
    
    analytics_data_frame.grid_rowconfigure(0, weight=1)
    analytics_data_frame.grid_columnconfigure(0, weight=1)



    # Top Products Frame 
    best_sellers_frame = ctk.CTkFrame(container, fg_color="#372724", height=200, width=600, corner_radius=10)
    best_sellers_frame.grid(row=2, column=1, padx=(10, 30), pady=(2, 20), sticky="nw")

    best_sellers_frame.grid_propagate(0)
    
    # Title label for the top sellers frame
    header_label = ctk.CTkLabel(best_sellers_frame, text="TOP-SELLING PRODUCTS",
                                font=("Inter", 18, "bold"), corner_radius=5,
                                fg_color="#372724", text_color="#FFFFFF", width=580, height=45)
    header_label.grid(row=0, column=0, padx=10, pady=(5, 5))

    # Fetch top-selling items
    top_selling_items = get_top_selling_items()
    # DALE 
    for idx, (item_name, sales_count) in enumerate(top_selling_items):
        # Fetch details for the current top-selling item
        top_selling_itemDetails = get_top_selling_item_details(item_name)
        
        button = ctk.CTkButton(
            best_sellers_frame,
            text=f"{item_name}",
            command=lambda details=top_selling_itemDetails: open_product_modal(details),
            font=("Inter", 16, "bold"),
            height=40, fg_color="#F1EBEB", width=580, border_color="black", text_color="#372724",
            cursor="hand2"
        )
        button.grid(row=1 + idx, column=0, padx=10, pady=4, sticky="w")


    # DALE - New Container
    # DALE - Adding of Current Categories for Analysis
    new_container = ctk.CTkFrame(container, fg_color="#372724", width=150, height=150, corner_radius=10)
    new_container.grid(row=2, column=1, columnspan=2, padx=(16,170), pady=(250, 20), sticky="nsew")

    # Label for new container
    new_container_label = ctk.CTkLabel(new_container, text="Product Category Analysis",
                                    font=("Inter", 18, "bold"),
                                    text_color="#FFFFFF")
    new_container_label.pack(pady=(10, 10), padx=10)

 
    # Fetch and display each category name as a button
    categories = get_product_categories()
    category_names = [category[1] for category in categories]

    # Create a button for each category name 
    for category in category_names:
        category_button = ctk.CTkButton(
            new_container,
            text=f"{category}",
            command=lambda name=category: open_product_modal_pieChart(name),
            font=("Inter", 14),
            height=40, fg_color="#F1EBEB", width=580, border_color="black", text_color="#372724",
            cursor="hand2"
        )
        category_button.pack(anchor="w", padx=10, pady=4)


    return container

# DALE 

open_windows = []

def close_all_windows():
    """Closes all open Tkinter windows."""
    for window in open_windows[:]:  # Create a copy to avoid modification issues
        window.destroy()  # Closes each window
    open_windows.clear()  # Clear the list after closing all windows

def open_product_modal(product_details):
    if not product_details:
        print("No product details available.")
        return

    close_all_windows()

    modal = ctk.CTkToplevel()
    modal.title(f"Details for {product_details['product_name']}")
    modal.geometry("400x300")

    # Track this modal in the open windows list
    open_windows.append(modal)

    # Display each detail with a label
    name_label = ctk.CTkLabel(modal, text=f"Product Name: {product_details['product_name']}")
    name_label.pack(pady=5)

    category_label = ctk.CTkLabel(modal, text=f"Category: {product_details['product_category']}")
    category_label.pack(pady=5)

    sales_label = ctk.CTkLabel(modal, text=f"Total Sales: {product_details['total_sales']}")
    sales_label.pack(pady=5)

    price_label = ctk.CTkLabel(modal, text=f"Unit Price: ₱{product_details['unit_price']}")
    price_label.pack(pady=5)

    revenue_label = ctk.CTkLabel(modal, text=f"Total Revenue: ₱{product_details['total_revenue']}")
    revenue_label.pack(pady=5)

    # Ensure modal is removed from open_windows when closed
    modal.protocol("WM_DELETE_WINDOW", lambda: safe_remove_modal(modal))
    modal.mainloop()


def safe_remove_modal(modal):
    try:
        open_windows.remove(modal)
    except ValueError:
        pass  # Ignore if modal is not in the list
    modal.destroy()