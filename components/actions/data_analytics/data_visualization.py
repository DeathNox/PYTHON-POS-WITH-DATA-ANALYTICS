import matplotlib.pyplot as plt  
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import customtkinter as ctk  
import matplotlib.dates as mdates
from tkinter import filedialog

from matplotlib.ticker import MaxNLocator
from cycler import cycler

# Example for MySQL connection
engine = create_engine('mysql+pymysql://root:password@localhost/pos_new')
db = engine.connect()  # This creates a connection to the database
import mysql.connector 



try:
      
      db = mysql.connector.connect(
            
            host = "localhost",
            user = "root",
            password = "password",
            database = "pos_siaa"
      
      )
      
      if db.is_connected():
            db_info = db.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = db.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            print("\n")
      
      mycursor = db.cursor()
      
except mysql.connector.Error as err:
      print(err)

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
            widget.destroy()

        # Use a fresh connection each time by creating it within the function
        with engine.connect() as db:
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

            df['order_date'] = pd.to_datetime(df['order_date'])

            if period == 'daily':
                df_agg = df.set_index('order_date').resample('D').sum()
            elif period == 'weekly':
                df_agg = df.set_index('order_date').resample('W').sum()
            elif period == 'monthly':
                df_agg = df.set_index('order_date').resample('M').sum()
            else:
                raise ValueError("Invalid period. Choose from 'daily', 'weekly', or 'monthly'.")

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(df_agg.index, df_agg['total_sale'], marker='o', label='Sales Revenue')
            ax.set_title(f'Cumulative Sales Revenue ({period.capitalize()})', fontsize=14)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Sales Revenue', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc='upper left', fontsize=10)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

    except Exception as e:
        print(f"Error - unable to connect / convert to data: {e}")


def cash_flow_linegraph_weekly(frame, period='weekly'):
    try:
        close_figures()

        for widget in frame.winfo_children():
            widget.destroy()

        with engine.connect() as db:
            query = """
            SELECT 
                YEAR(order_date) AS year, 
                WEEK(order_date, 1) AS week, 
                SUM(sub_total) AS total_sale
            FROM tbl_sales
            WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 12 WEEK) 
            GROUP BY year, week
            ORDER BY year, week;
            """
            df = pd.read_sql_query(query, db)

            if df.empty:
                print("No sales data found for the current period.")
                return

            df['week_start_date'] = pd.to_datetime(
                df['year'].astype(str) + '-W' + df['week'].astype(str) + '-1',
                format='%G-W%V-%u'
            )
            df['week_label'] = 'W' + df['week'].astype(str).str.zfill(2)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['week_label'], df['total_sale'], marker='o', label='Sales Revenue')
            ax.set_title('Cumulative Sales Revenue (Weekly)', fontsize=14)
            ax.set_xlabel('Week', fontsize=12)
            ax.set_ylabel('Sales Revenue', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc='upper left', fontsize=10)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

    except Exception as e:
        print(f"Error - unable to connect / convert to data: {e}")


def cash_flow_linegraph_monthly(frame, period='monthly'):
    try:
        close_figures()

        for widget in frame.winfo_children():
            widget.destroy()

        with engine.connect() as db:
            query = """
            SELECT 
                YEAR(order_date) AS year, 
                MONTH(order_date) AS month, 
                SUM(sub_total) AS total_sale
            FROM tbl_sales
            WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
            GROUP BY year, month
            ORDER BY year, month;
            """
            df = pd.read_sql_query(query, db)

            if df.empty:
                print("No sales data found for the current period.")
                return

            df['month_label'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['month_label'], df['total_sale'], marker='o', label='Sales Revenue')
            ax.set_title('Cumulative Sales Revenue (Monthly)', fontsize=14)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Sales Revenue', fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(loc='upper left', fontsize=10)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

    except Exception as e:
        print(f"Error - unable to connect / convert to data: {e}")

def export_tbl_sales_to_excel():
    try:
        # Query to fetch all data from tbl_sales
        sql = "SELECT * FROM tbl_sales"
        mycursor.execute(sql)
        rows = mycursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in mycursor.description]

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Map existing headers to improved headers
        header_mapping = {
            "sales_id": "Sales ID",
            "invoice_id": "Invoice No.",
            "product_id": "Product Code",
            "product_name": "Product Name",
            "product_category": "Category",
            "quantity": "Quantity Sold",
            "unit_price": "Unit Price (₱)",
            "sub_total": "Subtotal (₱)",
            "order_date": "Order Date & Time"
        }
        df.rename(columns=header_mapping, inplace=True)

        # Ask the user where to save the file with a default name
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")],
                                                 title="Save Sales Report",
                                                 initialfile="Sales_Report.xlsx")
        if file_path:
            # Export to Excel
            df.to_excel(file_path, index=False)
            print(f"Sales report exported successfully to {file_path}")
    except Exception as e:
        print(f"Error exporting tbl_sales to Excel: {e}")

