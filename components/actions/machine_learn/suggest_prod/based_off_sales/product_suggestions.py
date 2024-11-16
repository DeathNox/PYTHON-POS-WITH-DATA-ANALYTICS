import pandas as pd
from itertools import combinations



def suggest_ingredient_combinations_based_on_sales(products_df, ingredients_df, sales_df):
    
    
    # Step 1: asdkhjsaldksja validity of sales data putaha
    if sales_df.empty:
        print("No valid sales data to generate suggestions.")
        return []

    # Step 2: Merge product and sales data on 'product_id'
    merged_sales = pd.merge(products_df, sales_df, on="product_id", how="left")
    merged_sales['total_sales'] = merged_sales['total_sales'].fillna(0)

    # Step 3: Identify top-selling products
    top_selling_products = merged_sales[merged_sales['total_sales'] > 0].sort_values(by="total_sales", ascending=False)
    top_product_ids = top_selling_products['product_id'].tolist()

    print("Top Selling Products:")
    print(top_selling_products)

    # Step 4: Get the ingredients for top-selling products
    ingredients_for_top_products = ingredients_df[ingredients_df['product_id'].isin(top_product_ids)]

    print("Ingredients for Top Selling Products:")
    print(ingredients_for_top_products)

    # Step 5: Check if we have ingredients for the top-selling products
    if ingredients_for_top_products.empty:
        print("No ingredients found for the top-selling products.")
        return []

    # Step 6: Generate ingredient combinations (based on ingredients for top-selling products)
    ingredient_combinations = ingredients_for_top_products.groupby(['ingredient_name', 'ingredient_category']).size().reset_index(name='count')

    print("Generated Ingredient Combinations:")
    print(ingredient_combinations)

    # Step 7: Return the combinations
    return ingredient_combinations


