from db_setup.db_connect import mycursor  
import customtkinter as ctk
import bcrypt

def verify_user_credentials(username, entered_password):
    try:
        # Fetch the hashed password from the database
        query = "SELECT password FROM tbl_users WHERE username = %s"
        mycursor.execute(query, (username,))
        result = mycursor.fetchone()

        if result:
            hashed_password = result[0]
            # Verify the entered password against the hashed password
            if bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8')):
                return True, "success"  # Password is correct
            else:
                return False,  "password_incorrect"    # Password is incorrect
        else:
            return False,  "username_not_found" # User not found

    except Exception as e:
        print(f"Error: {e}")
        return False
