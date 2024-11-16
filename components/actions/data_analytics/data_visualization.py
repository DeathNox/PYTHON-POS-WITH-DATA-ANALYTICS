import matplotlib.pyplot as plt  
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import customtkinter as ctk  

# Example for MySQL connection
engine = create_engine('mysql+pymysql://root:root@localhost/pos_cafe')
db = engine.connect()  # This creates a connection to the database

def close_figures():
    plt.close('all')  # Closes all open figures


def open_product_modal_pieChart(category_name):
    pie_chart(category_name)


def pie_chart(category_name):
    try:
        # Close previous figures to avoid overlap
        close_figures()

        # Use a fresh connection each time by creating it within the function
        with engine.connect() as db:
            # Query to get total quantity sold for each product in the selected category
            query = f"""
            SELECT product_name, SUM(quantity) AS total_quantity
            FROM tbl_sales
            WHERE product_category = '{category_name}' AND unit_price > 1
            GROUP BY product_name
            """
            df = pd.read_sql_query(query, db)
            
            if df.empty:
                print(f"No data found for category '{category_name}'.")
                return

            # Create the pie chart using Matplotlib
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)  # Set explicit DPI
            df.set_index('product_name').plot.pie(y='total_quantity', legend=False, autopct='%1.1f%%', ax=ax)
            ax.set_title(f"Best-Selling Products in {category_name}")
            ax.set_ylabel('')  # Hide y-label for better appearance

            plt.show()  # This will display the pie chart in a separate window

    except Exception as e:
        print(f"Error - unable to connect / convert to data: {e}")


def display_line_chart(frame, period='daily'):
    try:
        # Close previous figures to avoid overlap
        close_figures()

        # Clear the frame before embedding a new figure
        for widget in frame.winfo_children():
            widget.pack_forget()

        # Use a fresh connection each time by creating it within the function
        with engine.connect() as db:
            # Query to get total sales for each date
            query = """
            SELECT order_date, SUM(sub_total) as total_sale
            FROM tbl_sales
            GROUP BY order_date
            """
            df = pd.read_sql_query(query, db)
            
            if df.empty:
                print("No sales data found.")
                return

            # Convert order_date to datetime
            df['order_date'] = pd.to_datetime(df['order_date'])

            # Aggregate sales data by the specified period
            if period == 'daily':
                df_agg = df.set_index('order_date').resample('D').sum()
            elif period == 'weekly':
                df_agg = df.set_index('order_date').resample('W').sum()
            elif period == 'monthly':
                df_agg = df.set_index('order_date').resample('M').sum()
            else:
                raise ValueError("Invalid period. Choose from 'daily', 'weekly', or 'monthly'.")

            # Create the Matplotlib figure and plot
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(df_agg.index, df_agg['total_sale'], marker='o', color='g')
            ax.set_title(f'Cumulative Sales Revenue ({period.capitalize()})')
            ax.set_xlabel('Date')
            ax.set_ylabel('Sales Revenue')
            ax.grid(True)

            # Format the x-axis labels to 'YY-MM-DD'
            ax.xaxis.set_major_formatter(plt.FixedFormatter(df_agg.index.strftime('%y-%m-%d')))

            # Embed the Matplotlib figure in the Tkinter Frame
            canvas = FigureCanvasTkAgg(fig, master=frame)  # Attach figure to the frame
            canvas.draw()  # Draw the canvas
            canvas.get_tk_widget().pack(fill='both', expand=True)  # Make it fill the frame

            # Ensure the Tkinter main loop is running
            if not frame.winfo_ismapped():
                frame.update_idletasks()
                frame.update()

            frame.update_idletasks()
            frame.update()
            
            plt.show()
    except Exception as e:
        print(f"Error - unable to connect / convert to data: {e}")