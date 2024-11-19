import pandas as pd
from sqlalchemy import create_engine

def connect_to_database():
    return create_engine("mysql+mysqlconnector://root:password@localhost/pos_new")

def load_data():
    engine = connect_to_database()

    # Query to fetch products
    query_products = "SELECT product_id, product_name, product_price FROM tbl_products"
    # Query to fetch ingredients
    query_ingredients = "SELECT product_id, ingredient_name, ingredient_category FROM tbl_product_ingredients WHERE product_id IS NOT NULL"
    # Query to aggregate sales data
    query_sales = """
        SELECT product_id, SUM(quantity) AS total_sales 
        FROM tbl_sales 
        WHERE product_id IS NOT NULL
        GROUP BY product_id
    """

    # Load the data into DataFrames
    products_df = pd.read_sql(query_products, engine)
    ingredients_df = pd.read_sql(query_ingredients, engine)
    sales_df = pd.read_sql(query_sales, engine)

    # If sales_df is empty, create a placeholder DataFrame
    if sales_df.empty:
        print("No sales data found, creating an empty sales DataFrame.")
        sales_df = pd.DataFrame(columns=["product_id", "total_sales"])

    # Debug print the data
    print("Loaded products_df:")
    print(products_df.head())
    print("Loaded ingredients_df:")
    print(ingredients_df.head())
    print("Loaded sales_df:")
    print(sales_df.head())

    # Return the three DataFrames
    return products_df, ingredients_df, sales_df

