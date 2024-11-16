import customtkinter as ctk
from PIL import Image
from db_setup.db_connect import mycursor, db  
import mysql.connector

class ProfileIcon(ctk.CTkButton):
    def __init__(self, parent, user_id, **kwargs):
        self.user_id = user_id



        # Get the user account type and first name
        self.account_type = self.get_user_account_type(self.user_id)
        self.first_name = self.get_user_first_name(self.user_id)  
        profile_icon_path = self.get_profile_icon_path(self.account_type)

        try:
            profile_image = ctk.CTkImage(Image.open(profile_icon_path), size=(60, 60))
        except Exception as e:
            print(f"Error loading profile icon: {e}")
            profile_image = None

        super().__init__(parent, image=profile_image, text="", fg_color="transparent", hover_color="#483434", width=40, height=40, command=self.open_profile_view, **kwargs)


    def get_user_first_name(self, user_id):
        """Fetch the user's first name from tbl_users based on user ID."""
        try:
            mycursor.execute("SELECT first_name FROM tbl_users WHERE user_id = %s", (user_id,))
            result = mycursor.fetchone()
            if result:
                return result[0]  
            return "Guest"
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "Guest"

    def get_user_account_type(self, user_id):
        """Fetch the user's account type from tbl_users based on user ID."""
        try:
            mycursor.execute("SELECT account_type FROM tbl_users WHERE user_id = %s", (user_id,))
            account_type = mycursor.fetchone()
            return account_type[0] if account_type else "Guest"
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "Guest"

    def get_profile_icon_path(self, account_type):
        """Return the path to the profile icon based on the user's account type."""
        icon_paths = {
            'Admin': './imgs/user_profile/profile_admin.png',
            'Employee': './imgs/user_profile/profile_emp.png',
        }
        return icon_paths.get(account_type, './imgs/user_profile/profile_emp.png')

    def open_profile_view(self):
        """Open the profile view when the icon is clicked."""
        from components.containers.user_profile.profile_view import open_profile 
        open_profile(self.user_id, self.account_type)
