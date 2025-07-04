import customtkinter as ctk
from components.containers.user_profile.profile_icon import ProfileIcon  # Import the new ProfileIcon class

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent, user_id, width=975, height=70, corner_radius=5, **kwargs):
        super().__init__(parent, fg_color="#372724", width=width, height=height, corner_radius=corner_radius, **kwargs)
        self.pack(side="top", fill="x")
        
        # profile icon button in the header
        self.profile_icon = ProfileIcon(self, user_id=user_id)
        self.profile_icon.pack(side="right", padx=10, pady=10)

        # Access account type and first name from ProfileIcon
        self.account_type = self.profile_icon.account_type
        self.first_name = self.profile_icon.first_name

        # frame para mahold name and account type labels
        self.profile_info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.profile_info_frame.pack(side="right", padx=10, pady=10)

        # Name Label (Hello, [First Name])
        self.name_label = ctk.CTkLabel(self.profile_info_frame, text=f"Hello, {self.first_name}", font=("Inter", 16, "bold"), fg_color="transparent")
        self.name_label.grid(row=0, column=0, padx=5, pady=(5,0))

        # Account Type Label
        self.account_type_label = ctk.CTkLabel(self.profile_info_frame, text=f"{self.account_type}", font=("Inter", 14, "italic"), fg_color="transparent")
        self.account_type_label.grid(row=1, column=0, padx=5, pady=(0,5))
