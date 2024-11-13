from components.actions.machine_learn.suggest_prod.based_off_inventory.generate_new_product import generate_hypothetical_products, suggest_new_products
from model import train_random_forest, create_ingredient_matrix
from data_processing import load_data

def generate_new_product():
    # Load data
    products_df, ingredients_df, sales_df = load_data()

    # Create ingredient matrix with sales influence
    ingredient_matrix = create_ingredient_matrix(ingredients_df, products_df, sales_df)

    # Train the model
    model = train_random_forest(ingredient_matrix)

    # Generate new product combinations
    new_product_suggestions = generate_hypothetical_products(ingredients_df)

    # Suggest new products based on trained model
    valid_suggestions = suggest_new_products(products_df, model, ingredient_matrix, new_product_suggestions)

    return valid_suggestions
