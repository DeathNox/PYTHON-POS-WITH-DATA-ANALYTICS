from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

# Create ingredient matrix with sales influence
def create_ingredient_matrix(ingredients_df, products_df, sales_df):
    if sales_df.empty:
        print("No sales data available. Returning empty ingredient matrix.")
        return pd.DataFrame()  # Return empty matrix if sales data is missing

    # Merge ingredients, products, and sales data on 'product_id'
    merged_df = pd.merge(ingredients_df, products_df, on="product_id", how="left")
    merged_df = pd.merge(merged_df, sales_df, on="product_id", how="left")
    
    print("After merging with sales data:")
    print(merged_df.head())

    # Create a pivot table with ingredients as columns
    ingredient_matrix = merged_df.pivot_table(index='product_id', 
                                              columns='ingredient_name', 
                                              values='total_sales', 
                                              aggfunc='sum', 
                                              fill_value=0)
    return ingredient_matrix

# Train the Random Forest model
def train_random_forest(ingredient_matrix, sales_df):
    # Ensure that ingredient_matrix and sales_df are not empty
    if ingredient_matrix.empty or sales_df.empty:
        print("Empty data received. Skipping model training.")
        return None
    
    X = ingredient_matrix.values
    
    # Example logic to create target labels based on sales (binary classification)
    sales_threshold = 10  # Adjust this based on your context
    y = (sales_df['total_sales'] > sales_threshold).astype(int)  # 1 if sales > threshold, else 0

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model
