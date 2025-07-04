from db_setup.db_connect import mycursor, db
import customtkinter as ctk
import bcrypt

def create_user_account(username, password, firstname, lastname, phone_number, role_choice, email_address):
    try:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_query = """
        INSERT INTO tbl_users (username, password, first_name, last_name, contact, account_type, email_address) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        user_data = (username, hashed_password, firstname, lastname, phone_number, role_choice, email_address)
        
        mycursor.execute(user_query, user_data)
        db.commit()
        
        return True

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False

      