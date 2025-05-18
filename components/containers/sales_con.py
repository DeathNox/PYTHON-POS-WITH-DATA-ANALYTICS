import customtkinter as ctk
from ..actions.db.fetch_top_sellers import get_top_selling_items, get_top_selling_item_details
from ..actions.db.fetch_sales import get_avg_order
from components.actions.data_analytics.data_visualization import open_product_modal_pieChart, display_line_chart, cash_flow_linegraph_weekly, cash_flow_linegraph_monthly, export_tbl_sales_to_excel
from .orders_con import get_total_income, get_profit, get_total_income_today
from ..actions.db.fetch_product_categories import get_product_categories
from ..actions.db.fetch_employee_sales import get_employee_sales_performance  # Import the database function
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# Function to create a metric card
def create_metric_card(frame, title, value, row, col):
    cards_width = 305
    cards_height = 150


    card = ctk.CTkFrame(frame, fg_color="#60514E", corner_radius=10, width=cards_width, height=cards_height)  
    card.grid(row=row, column=col, padx=(40, 0), pady=(20, 30))

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
    total_sales_today = get_total_income_today()  # Call the function to get the total sales value
    profit = get_profit()
    display_value = f"{profit:.2f}"  # Format the total sales value as a string with two decimal places

    avg_order = get_avg_order()
    display_value1 = f"{avg_order:.2f}"  # Format the total sales value as a string with two decimal places


    create_metric_card(cards_display_frame, "TOTAL SALES REVENUE", total_sales, 0, 0)
    create_metric_card(cards_display_frame, "SALES TODAY", total_sales_today, 0, 1)
    create_metric_card(cards_display_frame, "TOTAL INCOME", display_value, 0, 2)
    create_metric_card(cards_display_frame, "AVERAGE ORDER VALUE", display_value1, 0, 3)

    # Container for analytics
    analytics_frame = ctk.CTkFrame(container, fg_color="#372724", height=480, width=815, corner_radius=10)
    analytics_frame.grid(row=2, column=0, padx=(50, 50), pady=(2, 20), sticky="nsew")

    # Analytics header
    analytics_frame_header = ctk.CTkFrame(analytics_frame, fg_color="#372724")
    analytics_frame_header.grid(row=0, column=0, sticky="ew", padx=5, pady=5)


    analytics_data_fr = ctk.CTkFrame(analytics_frame, width=800, height=400, corner_radius=10, fg_color="#F2F1EF")
    analytics_data_fr.grid(row=1, column=0, padx=20, pady=(20, 20), sticky="nsew")

    # Adjust the placement of the buttons to align them horizontally above the chart
    button_frame = ctk.CTkFrame(container, fg_color="transparent")
    button_frame.place(x = 80, y= 240)

    ctk.CTkButton(button_frame, text="Daily", fg_color="#382C26", bg_color="transparent", text_color="#E9E4DB", hover_color="#6C635A", width=80,
              cursor="hand2", font=("Poppins", 14, "bold"), command=lambda: display_line_chart(analytics_data_fr, 'daily')).grid(row=0, column=0, padx=(0, 10))

    ctk.CTkButton(button_frame, text="Weekly", fg_color="#382C26", bg_color="transparent", text_color="#E9E4DB", hover_color="#6C635A", width=80,
              cursor="hand2", font=("Poppins", 14, "bold"), command=lambda: cash_flow_linegraph_weekly(analytics_data_fr, 'weekly')).grid(row=0, column=1, padx=(0, 10))

    ctk.CTkButton(button_frame, text="Monthly", fg_color="#382C26", bg_color="transparent", text_color="#E9E4DB", hover_color="#6C635A", width=80,
              cursor="hand2", font=("Poppins", 14, "bold"), command=lambda: cash_flow_linegraph_monthly(analytics_data_fr, 'monthly')).grid(row=0, column=2, padx=(0, 10))

    ctk.CTkButton(button_frame, text="Export Report", fg_color="#382C26", bg_color="transparent", text_color="#E9E4DB", hover_color="#6C635A", width=120,
                  cursor="hand2", font=("Poppins", 14, "bold"), command=export_tbl_sales_to_excel).grid(row=0, column=3, padx=(0, 10))

    # Title label for the analytics frame
    header_label = ctk.CTkLabel(analytics_frame_header, text="Cash Flow Analytic",
                                font=("Inter", 22, "bold"),
                                fg_color="#372724", text_color="#FFFFFF", anchor="center")
    header_label.grid(row=0, column=0, padx=(250, 400), pady=(10, 10))

    # Prevent grid propagation to maintain sizing
    analytics_frame.grid_propagate(0)

    # Analytics Data Frame (for displaying cash flow)


    # Bind the click event to the analytics_data_frame

    # Grids
    analytics_frame.grid_rowconfigure(1, weight=1)
    analytics_frame.grid_columnconfigure(0, weight=1)



    # Top Products Frame 
    best_sellers_frame = ctk.CTkFrame(container, fg_color="#372724", height=200, width=515, corner_radius=10)
    best_sellers_frame.grid(row=2, column=1, padx=(20, 30), pady=(2, 10), sticky="nw")

    best_sellers_frame.grid_propagate(0)
    best_sellers_frame.grid_columnconfigure(0, weight=1)
    
    # Title label for the top sellers frame
    header_label = ctk.CTkLabel(best_sellers_frame, text="Top Selling Products",
                                font=("Inter", 20, "bold"), corner_radius=5,
                                fg_color="#372724", text_color="#FFFFFF", width=500, height=45)
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
            font=("Inter", 18, "bold"),
            height=40, fg_color="#EBE0D6", width=500, border_color="black", text_color="#1E1E1E",
            cursor="hand2"
        )
        button.grid(row=1 + idx, column=0, padx=(50, 50), pady=4, sticky="w")


    # DALE - New Container
    # DALE - Adding of Current Categories for Analysis
    new_container = ctk.CTkFrame(container, fg_color="#372724",height=150, width = 650, corner_radius=10)
    new_container.grid(row=2, column=1, columnspan=2, padx=(20, 50), pady=(220, 20), sticky="nsew")

    new_container.grid_propagate(0)
    new_container.grid_columnconfigure(0, weight=1)

    # Label for new container
    new_container_label = ctk.CTkLabel(new_container, text="Product Category Analysis",
                                    font=("Inter", 18, "bold"),
                                    text_color="#FFFFFF")
    new_container_label.pack(pady=(20, 20), padx=10)

 
    # Fetch and display each category name as a button
    categories = get_product_categories()
    category_names = [category[1] for category in categories]

    # Create a button for each category name 
    for category in category_names:
        category_button = ctk.CTkButton(
            new_container,
            text=f"{category}",
            command=lambda name=category: open_product_modal_pieChart(name),
            font=("Inter", 18, "bold"),
            height=40, fg_color="#EBE0D6", width=500, border_color="black", text_color="#1E1E1E",
            cursor="hand2"
        )
        category_button.pack(anchor="w", padx=(50, 50), pady=4)


    return container

# DALE 

open_windows = []

# Keep track of scheduled after events
scheduled_after_events = []

def close_all_windows():
    """Closes all open Tkinter windows."""
    for window in open_windows[:]:  # Create a copy to avoid modification issues
        window.destroy()  # Closes each window
    open_windows.clear()  # Clear the list after closing all windows

def open_product_modal(product_details):
    
    from main import CenterWindowToDisplay
    
    if not product_details:
        print("No product details available.")
        return

    close_all_windows()



    modal = ctk.CTkToplevel()
    modal.title(f"Details for {product_details['product_name']}")
    modal.geometry(CenterWindowToDisplay(modal, 400, 300, modal._get_window_scaling()))
    modal.resizable(False, False)
    modal.configure(fg_color="#EBE0D6")
    
    open_windows.append(modal)

    # Display product name
    product_name_frame = ctk.CTkFrame(modal, fg_color="transparent")
    product_name_frame.pack(pady=5, padx=20, fill="x", anchor="w")  

    name_label_bold = ctk.CTkLabel(product_name_frame, text="Product Name:", text_color="black", font=("Inter", 18, "bold"))
    name_label_bold.pack(side="left", padx=(0, 5), anchor="w")

    name_label_regular = ctk.CTkLabel(product_name_frame, text=product_details['product_name'], text_color="black", font=("Inter", 18))
    name_label_regular.pack(side="left", anchor="w")

    # Display product category
    category_frame = ctk.CTkFrame(modal, fg_color="transparent")
    category_frame.pack(pady=5, padx=20, fill="x", anchor="w")  

    category_label_bold = ctk.CTkLabel(category_frame, text="Category:", text_color="black", font=("Inter", 18, "bold"))
    category_label_bold.pack(side="left", padx=(0, 5), anchor="w")

    category_label_regular = ctk.CTkLabel(category_frame, text=product_details['product_category'], text_color="black", font=("Inter", 18))
    category_label_regular.pack(side="left", anchor="w")

    header_frame = ctk.CTkFrame(modal, fg_color="#30211E")
    header_frame.pack(padx=10, pady=(25, 0), fill="x")

    header_frame.grid_columnconfigure(0, weight=1)
    header_frame.grid_columnconfigure(1, weight=1)
    header_frame.grid_columnconfigure(2, weight=1)

    # Header labels
    header_labels = ["Total Sales", "Unit Price", "Total Revenue"]
    for col, header in enumerate(header_labels):
        header_label = ctk.CTkLabel(
            header_frame, 
            text=header, 
            font=("Inter", 18, "bold"), 
            text_color="#F5F5F5"
        )
        header_label.grid(row=0, column=col, padx=10, pady=5, sticky="ew") 

  
    sales_table_frame = ctk.CTkFrame(modal, fg_color="#EBE0D6")
    sales_table_frame.pack(padx=10, pady=(0, 10), fill="x")

    # Configure columns for data rows
    sales_table_frame.grid_columnconfigure(0, weight=1)
    sales_table_frame.grid_columnconfigure(1, weight=1)
    sales_table_frame.grid_columnconfigure(2, weight=1)

    table_data = [
        [product_details['total_sales'], f"₱{product_details['unit_price']}", f"₱{product_details['total_revenue']}"]
    ]

    # Populate table rows
    for row_idx, row_data in enumerate(table_data):
        for col_idx, cell_data in enumerate(row_data):
            cell_label = ctk.CTkLabel(
                sales_table_frame, 
                text=cell_data, 
                font=("Inter", 18, "bold"), 
                text_color="#1E1E1E"
            )
            cell_label.grid(row=row_idx, column=col_idx, padx=10, pady=5, sticky="ew")  


    # Close button
    close_button = ctk.CTkButton(
        modal, 
        text="Close", 
        command=modal.destroy, 
        fg_color="#30211E", 
        hover_color="#594A47", 
        font=("Inter", 18, "bold")
    )
    close_button.pack(pady=(80, 0))


    # Ensure modal is removed from open_windows when closed
    modal.protocol("WM_DELETE_WINDOW", lambda: safe_remove_modal(modal))
    modal.mainloop()



def safe_remove_modal(modal):
    try:
        # Cancel any pending after events
        for event in scheduled_after_events:
            modal.after_cancel(event)
        scheduled_after_events.clear()

        open_windows.remove(modal)
    except ValueError:
        pass  # Ignore if modal is not in the list
    modal.destroy()
    
    
def performance_container(window, user_id):
    # Main container frame for sales overview
    container = ctk.CTkFrame(window, fg_color="#EBE0D6", width=1275, height=900, corner_radius=2)
    container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Add a "Generate Report" button
    generate_report_button = ctk.CTkButton(
        container,
        text="Generate Report",
        command=lambda: on_generate_report_click(generate_report_button, container),
        font=("Inter", 18, "bold"),
        fg_color="#60514E",
        text_color="white",
        hover_color="#372724",
        corner_radius=10,
        width=200,
        height=50
    )
    generate_report_button.pack(pady=(20, 10))  # Adjust padding as needed

    return container


def on_generate_report_click(button, container):
    # Hide the button
    button.pack_forget()

    # Call the function to display the employee sales performance
    display_employee_sales_performance(container)


def display_employee_sales_performance(container):
    # Fetch data from the database
    employee_sales_data = get_employee_sales_performance()  # Returns a list of tuples [(employee_name, sales), ...]
    print("Raw employee sales data:", employee_sales_data)  # Debugging output

    # Filter out invalid data (e.g., None values or invalid types)
    from decimal import Decimal  # Ensure Decimal is imported

    valid_data = [(name, sales) for name, sales in employee_sales_data if isinstance(name, str) and isinstance(sales, (int, float, Decimal))]
    print("Valid employee sales data:", valid_data)  # Debugging output

    # Separate the data into two lists for plotting
    employee_names = [data[0] for data in valid_data]
    sales_performance = [data[1] for data in valid_data]

    # Check if there's valid data to plot
    if not employee_names or not sales_performance:
        print("No valid employee sales data available to display.")
        messagebox.showinfo("No Data", "No valid employee sales data available to display today.")
        return

    # Generate a color for each bar using a colormap
    import matplotlib.cm as cm
    import numpy as np
    num_bars = len(employee_names)
    colors = cm.get_cmap('tab20', num_bars)(np.arange(num_bars))

    # Create the bar graph using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(employee_names, sales_performance, color=colors)
    ax.set_title('Employee Sales Performance', fontsize=16)
    ax.set_xlabel('Employee Names', fontsize=12)
    ax.set_ylabel('Sales Performance', fontsize=12)
    ax.tick_params(axis='x', rotation=0)

    # Embed the matplotlib figure into the Tkinter container
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill='both', expand=True)

    # Add a cleanup function to destroy the canvas and close the figure
    def cleanup_graph():
        canvas_widget.destroy()  # Destroy the Tkinter widget
        plt.close(fig)  # Close the matplotlib figure

    # Bind the cleanup function to the container's destroy event
    container.bind("<Destroy>", lambda event: cleanup_graph())