import numpy as np
import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random
import customtkinter as ctk

# MySQL Database Connection
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="pos_new"
    )

# Load data from the database
def load_data():
    conn = connect_to_database()
    query_products = "SELECT product_id, product_name FROM tbl_products"
    query_ingredients = "SELECT product_id, ingredient_name, ingredient_category FROM tbl_product_ingredients"
    
    products_df = pd.read_sql(query_products, conn)
    ingredients_df = pd.read_sql(query_ingredients, conn)
    
    conn.close()
    
    return products_df, ingredients_df

# Create ingredient presence matrix
def create_ingredient_matrix(ingredients_df, products_df):
    ingredient_matrix = ingredients_df.pivot_table(index='product_id', 
                                                   columns='ingredient_name', 
                                                   aggfunc='size', 
                                                   fill_value=0)
    ingredient_matrix = ingredient_matrix.reindex(products_df['product_id'])
    return ingredient_matrix.fillna(0)

# Train the Random Forest model
def train_random_forest(ingredient_matrix):
    X = ingredient_matrix.values  
    y = [1] * len(X) 

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    return model

# Generate hypothetical new product combinations
def generate_hypothetical_products(ingredients_df, num_combinations=5):
    ingredient_categories = {
        'toppings': [],
        'base_liquids': [],
        'coffee_base': [],
        'additives': []
    }

    # Populate ingredient categories from the DataFrame
    for index, row in ingredients_df.iterrows():
        ingredient_name = row['ingredient_name']
        ingredient_category = row['ingredient_category']
        
        if ingredient_category in ingredient_categories:
            ingredient_categories[ingredient_category].append(ingredient_name)

    all_combinations = []

    # Generate unique combinations of ingredients
    for i in range(num_combinations):
        combination = []

        # Randomly select ingredients ensuring they come from different categories
        if ingredient_categories['toppings']:
            combination.append(random.choice(ingredient_categories['toppings']))
        if ingredient_categories['base_liquids']:
            combination.append(random.choice(ingredient_categories['base_liquids']))
        if ingredient_categories['coffee_base']:
            combination.append(random.choice(ingredient_categories['coffee_base']))
        if ingredient_categories['additives']:
            combination.append(random.choice(ingredient_categories['additives']))

        # Shuffle to randomize ingredient order in the combination
        random.shuffle(combination)
        all_combinations.append(combination)

      
        print(f"Generated combination {i + 1}: {combination}")

    return all_combinations

# Generate a product name based on the ingredients
def generate_product_name(ingredients):
    base_names = ["Latte", "Espresso", "Americano", "Frappuccino", "Mocha", "Cappuccino"]
    name = " & ".join(ingredients) + " " + random.choice(base_names)
    return name

# POS Application Class
class GenerateNewProduct:
    def __init__(self):
        self.products_df, self.ingredients_df = load_data()  # Load data from the database
        self.ingredient_matrix = create_ingredient_matrix(self.ingredients_df, self.products_df)  
        self.model = train_random_forest(self.ingredient_matrix)  # Train the model
        self.init_gui()  

    def init_gui(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("POS System")
        self.root.geometry("400x400")

        # Suggest new product button
        self.suggest_button = ctk.CTkButton(self.root, text="Generate Combinations", command=self.on_suggest_button_click)
        self.suggest_button.pack(pady=10)

        # Suggestions result label
        self.suggestions_label = ctk.CTkLabel(self.root, text="")
        self.suggestions_label.pack(pady=10)

        self.root.mainloop()

    def on_suggest_button_click(self):
            new_product_suggestions = generate_hypothetical_products(self.ingredients_df)
            valid_suggestions = self.suggest_new_products(new_product_suggestions)

          
            limited_suggestions = valid_suggestions[:3]  

            if limited_suggestions:
                  product_names = [generate_product_name(ingredients) for ingredients in limited_suggestions]
                  suggestions_text = f"Suggested New Products:\n" + "\n".join(product_names)
            else:
                  suggestions_text = "No valid new product combinations found."
            
            self.suggestions_label.configure(text=suggestions_text)


    def suggest_new_products(self, new_combinations):
      valid_products = []
      existing_product_names = set(self.products_df['product_name'].str.lower())  # Get existing product names in lowercase for comparison

      for combination in new_combinations:
            ingredient_vector = pd.Series(0, index=self.ingredient_matrix.columns)
            for ingredient in combination:
                  if ingredient in ingredient_vector.index:
                        ingredient_vector[ingredient] = 1

            input_vector = ingredient_vector.values.reshape(1, -1)
            prediction = self.model.predict(input_vector)[0]

            # print(f"Testing combination: {combination}, Prediction: {prediction}")  # Debugging o
            
            if prediction == 1:
                  product_name = generate_product_name(combination).lower()  
                  if product_name not in existing_product_names:  
                        valid_products.append(combination)

      return valid_products


