import customtkinter as ctk

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent, width=975, height=70, corner_radius=5, **kwargs):
        super().__init__(parent, fg_color="#372724", width=width, height=height, corner_radius=corner_radius, **kwargs)
        self.pack(side="top", fill="x")

  