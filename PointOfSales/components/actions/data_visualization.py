import matplotlib.pyplot as plt  
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import customtkinter as ctk  

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

    
