import numpy as np
import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random
import customtkinter as ctk
from sqlalchemy import create_engine


def connect_to_database():
    return create_engine("mysql+mysqlconnector://root:root@localhost/kapehan_pos")

# Load data from the database
def load_data():
    engine = connect_to_database()
    query_products = "SELECT product_id, product_name FROM tbl_products"
    query_ingredients = "SELECT product_id, ingredient_name, ingredient_category FROM tbl_product_ingredients"
    
    products_df = pd.read_sql(query_products, engine)
    ingredients_df = pd.read_sql(query_ingredients, engine)
    
    return products_df, ingredients_df
# ingredient matrix
def create_ingredient_matrix(ingredients_df, products_df):
    ingredient_matrix = ingredients_df.pivot_table(index='product_id', 
                                                   columns='ingredient_name', 
                                                   aggfunc='size', 
                                                   fill_value=0)
    ingredient_matrix = ingredient_matrix.reindex(products_df['product_id'])
    return ingredient_matrix.fillna(0)

#  Random Forest model
def train_random_forest(ingredient_matrix):
    X = ingredient_matrix.values  
    y = [1] * len(X) 



    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    return model

# hypothetical new product combinations
def generate_hypothetical_products(ingredients_df, num_combinations=5):
    ingredient_categories = {
        'Toppings': [],
        'Base Liquids': [],
        'Coffee Base': [],
        'Additives': []
    }

    for index, row in ingredients_df.iterrows():
        ingredient_name = row['ingredient_name']
        ingredient_category = row['ingredient_category']
        
        if ingredient_category in ingredient_categories:
            ingredient_categories[ingredient_category].append(ingredient_name)

    all_combinations = []


    for i in range(num_combinations):
        combination = []

        if ingredient_categories['Toppings']:
            combination.append(random.choice(ingredient_categories['Toppings']))
        if ingredient_categories['Base Liquids']:
            combination.append(random.choice(ingredient_categories['Base Liquids']))
        if ingredient_categories['Coffee Base']:
            combination.append(random.choice(ingredient_categories['Coffee Base']))
        if ingredient_categories['Additives']:
            combination.append(random.choice(ingredient_categories['Additives']))

      
        random.shuffle(combination)
        all_combinations.append(combination)

      
        print(f"Generated combination {i + 1}: {combination}")

    return all_combinations


def generate_product_name(ingredients):
    base_names = ["Latte", "Frappe", "Mocha"]
    name = ", ".join(ingredients) + " " + random.choice(base_names)
    return name


def on_suggest_button_click(self):
    new_product_suggestions = generate_hypothetical_products(self.ingredients_df)
    valid_suggestions = suggest_new_products(self.products_df, self.model, self.ingredient_matrix, new_product_suggestions)
    
    limited_suggestions = valid_suggestions[:3] if valid_suggestions else []
    
    if limited_suggestions:
        product_names = [generate_product_name(ingredients) for ingredients in limited_suggestions]
        suggestions_text = "Suggested New Products:\n" + "\n".join(product_names)
    else:
        suggestions_text = "No valid new product combinations found."
    
    self.suggestions_label.configure(text=suggestions_text)




def suggest_new_products(products_df, model, ingredient_matrix, new_combinations):
    valid_products = []
    existing_product_names = set(products_df['product_name'].str.lower())  

    for combination in new_combinations:
    
        ingredient_vector = pd.Series(0, index=ingredient_matrix.columns)
        for ingredient in combination:
            if ingredient in ingredient_vector.index:
                ingredient_vector[ingredient] = 1

        prediction = model.predict([ingredient_vector])[0]
        if prediction == 1:
            
            product_name = generate_product_name(combination).lower()
            if product_name not in existing_product_names:
                valid_products.append(combination)
                existing_product_names.add(product_name)

    return valid_products


