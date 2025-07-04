from db_setup.db_connect import mycursor  
import customtkinter as ctk
import bcrypt
from ...global_variable.global_var import logged_in_user

def verify_user_credentials(username, entered_password):
    global logged_in_user  # Declare it as global to modify the imported variable
    try:
        # Fetch the user_id, hashed password, and account_type from the database
        query = "SELECT user_id, password, account_type, username FROM tbl_users WHERE username = %s"
        mycursor.execute(query, (username,))
        result = mycursor.fetchone()

        if result:
            user_id = result[0]  # Fetching user_id from the result
            hashed_password = result[1]  # Fetching hashed password
            account_type = result[2]  # Fetching account_type from the result
            logged_in_user = result[3]  # Update the global variable
            # Verify the entered password against the hashed password
            if bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8')):
                return True, "success", user_id, account_type, logged_in_user  # Return 5 values
            else:
                return False, "password_incorrect", None, None, None  # Password is incorrect
        else:
            return False, "username_not_found", None, None, None  # User not found

    except Exception as e:
        print(f"Error: {e}")
        return False, str(e), None, None, None  # Return the error message along with None for missing values

