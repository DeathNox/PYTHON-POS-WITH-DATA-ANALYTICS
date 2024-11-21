import matplotlib.pyplot as plt  
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import customtkinter as ctk  
import matplotlib.dates as mdates

from matplotlib.ticker import MaxNLocator
from cycler import cycler

# Example for MySQL connection
engine = create_engine('mysql+pymysql://root:password@localhost/pos_new')
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
            WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) and DATE(order_date) <= CURDATE()
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

            # Define a custom color palette
            custom_palette = ['#4E79A7', '#F28E2B', '#FBFBFB', '#76B7B2', '#59A14F']


            # Apply the custom palette to Matplotlib
            plt.rc('axes', prop_cycle=cycler('color', custom_palette))
            plt.rcParams['axes.facecolor'] = '#EBE0D6'
            plt.rcParams['figure.facecolor'] = '#30211E'
            
            # Update rcParams for consistent text colors
            plt.rcParams['text.color'] = '#1E1E1E'  # Light color for general text
            plt.rcParams['axes.labelcolor'] = '#FBFBFB'  # Light color for axis labels
            plt.rcParams['xtick.color'] = '#FBFBFB'  # Light color for x-tick labels
            plt.rcParams['ytick.color'] = '#FBFBFB'  # Light color for y-tick labels
            plt.rcParams['axes.titlecolor'] = '#EBE0D6'  # Light color for title

            
        
        
            # Create the Matplotlib figure and plot
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(df_agg.index, df_agg['total_sale'], marker='o', label='Sales Revenue')
            ax.set_title(f'Cumulative Sales Revenue ({period.capitalize()})', fontsize=14)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Sales Revenue', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc='upper left', fontsize=10)

            # Format the x-axis labels to 'YY-MM-DD'
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Ensure clean integer tick spacing

            # Embed the Matplotlib figure in the Tkinter Frame
            canvas = FigureCanvasTkAgg(fig, master=frame)  # Attach figure to the frame
            canvas.draw()  # Draw the canvas
            canvas.get_tk_widget().pack(fill='both', expand=True)  # Make it fill the frame

            # Ensure the Tkinter main loop is running
            frame.update_idletasks()
            frame.update()
            
            plt.show()
    except Exception as e:
        print(f"Error - unable to connect / convert to data: {e}")