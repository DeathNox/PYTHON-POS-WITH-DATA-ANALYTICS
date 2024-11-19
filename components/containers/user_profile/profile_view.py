import customtkinter as ctk
import mysql.connector

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'pos_new'
}

def open_profile(user_id, account_type):
    """Create a profile window and display account type-specific information."""
    profile_window = ctk.CTkToplevel()
    profile_window.title("Profile")
    profile_window.geometry("400x300")

    # Fetch user information from tbl_users
    user_info = fetch_user_info(user_id)
    role_label = ctk.CTkLabel(profile_window, text=f"Account Type: {account_type}", font=("Arial", 14, "bold"))
    role_label.pack(pady=10)

    # Display user information
    name = f"{user_info.get('first_name', 'N/A')} {user_info.get('last_name', 'N/A')}"
    name_label = ctk.CTkLabel(profile_window, text=f"Name: {name}")
    email_label = ctk.CTkLabel(profile_window, text=f"Email: {user_info.get('email_address', 'N/A')}")
    contact_label = ctk.CTkLabel(profile_window, text=f"Contact: {user_info.get('contact', 'N/A')}")
    
    name_label.pack(pady=5)
    email_label.pack(pady=5)
    contact_label.pack(pady=5)

def fetch_user_info(user_id):
    """Fetch user details from tbl_users."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT first_name, last_name, contact, email_address FROM tbl_users WHERE user_id = %s", (user_id,))
        user_info = cursor.fetchone()
        return user_info if user_info else {}
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return {}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
