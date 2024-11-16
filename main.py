from customtkinter import CTk, CTkFrame
import tkinter as tk
from components.containers.forms.login_form import login_form_container
import sys, os




def main():
      
      window()
      

# main window

def window():
      

      root = CTk()
      root.geometry(CenterWindowToDisplay(root, 1680, 900, root._get_window_scaling()))
      root.resizable(False, False)
      root.title("Point of Sales | Company Name")
      icon = os.path.join(sys.path[0], 'imgs/sidepanel_icons/dummylogo.ico')
      
      root.iconbitmap(icon)
      
      
            
      background_frame = CTkFrame(root, fg_color="#372724")  
      background_frame.pack(fill="both", expand=True)
      
      
      content_frame = login_form_container(background_frame)
      content_frame.pack(fill="both", expand=True)
      

      root.mainloop()

def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    
  
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    
    return f"{width}x{height}+{x}+{y}"

if __name__ == "__main__":
    main()      
