import customtkinter as ctk

class ContainerFrame(ctk.CTkFrame):
    def __init__(self, parent,  fg_color="#EBE0D6", width=975, height=895, corner_radius=10, **kwargs):
      
        super().__init__(parent, fg_color="#EBE0D6", width=width, height=height, corner_radius=corner_radius, **kwargs)
        
       
        self.pack(side="left", fill="both", expand=True, padx=10, pady=20)
        