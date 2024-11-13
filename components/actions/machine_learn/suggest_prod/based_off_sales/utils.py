import random

# Generate a random product name based on ingredients
def generate_product_name(ingredients):
    base_names = ["Latte", "Frappe", "Mocha"]
    name = ", ".join(ingredients) + " " + random.choice(base_names)
    return name
