from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as CTk
from components.actions.navigation import switch_to_orders, switch_to_home, switch_to_sales_con, switch_to_prodconfig, switch_to_prod_view, switch_to_inventory_con, log_out



def side_panel(window):
      
      
      # Side Panel Stylings
      
      side_panel = tk.Frame(window, bg="#E4CFBB", 
                              width = 175)
      
      side_panel.pack_propagate(False)
      side_panel.pack(side="left", fill="y",
                        padx = 8, pady = 8)
      
      company_logo = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/dummylogo.png")
      resized_logo = company_logo.resize((150, 150))
      company_logo = ImageTk.PhotoImage(resized_logo)

      logo_label = tk.Label(side_panel, image=company_logo, bg="#E4CFBB")
      logo_label.image = company_logo
      logo_label.pack(pady=10)

      label = tk.Label(side_panel, bg="#E4CFBB")
      label.pack(pady=10)
      
     

      return side_panel
   


def sidepanel_options(side_panel, window, content_frame):
      
      # START -  Pang navigate to other interfaces.
    
      def switch_to_orders_frame():
        switch_to_orders(window, content_frame)
      
      
      def switch_to_home_frame():
        switch_to_home(window, content_frame)
        
      def switch_to_view_prod_frame():
        switch_to_prod_view(window, content_frame)
      
      # def switch_to_prod_frame():
      #   switch_to_prodconfig(window, content_frame)
        
      def switch_to_sales_frame():
        
        switch_to_sales_con(window, content_frame)
        
        
      def switch_to_inventory_frame():
        
        switch_to_inventory_con(window, content_frame)
        
      def log_out_frame():
        log_out(window, content_frame, side_panel)
        
       # END -  Pang navigate to other interfaces.
      
      
      # START - home btn styling 
    
      menu_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/menu_icon_light.png")
      resized_icon = menu_btn_icon.resize((30, 40))
      ctk_menu_icon = CTk.CTkImage(dark_image=resized_icon, size=(25, 30))
      
      
      menu_btn = CTk.CTkButton(side_panel, text="Home", image=ctk_menu_icon,
                               font=("Inter", 18, "bold"),
                               compound="left", fg_color="#372724",
                               text_color="#EBE0D6", width=1000,
                               command=switch_to_home_frame)

      menu_btn.pack(pady = 10, padx = 10)
      
      # END - home btn styling 




      # START - orders_history btn styling
      
      orders_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/orders_icon_light.png")
      resized_icon = orders_btn_icon.resize((30, 40))
      ctk_orders_icon = CTk.CTkImage(dark_image=resized_icon, size=(20, 30))

    
      orders_btn = CTk.CTkButton(side_panel, text="Orders", image=ctk_orders_icon, 
                                 font=("Inter", 18, "bold"),
                                 compound="left",
                                 fg_color="#372724",
                                 text_color="#EBE0D6", width=1000,
                                 command=switch_to_orders_frame) # TODO: Add a switch to another containter function
       
       
      
      orders_btn.pack(pady=10, padx=10)
      
      # END- orders_history styling
      
      
      # START - Products styling btn
      
      products_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/products_icon.png")
      resized_icon = products_btn_icon.resize((30, 40))
      ctk_product_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))
      
      view_products_btn = CTk.CTkButton(side_panel, text="Products", image=ctk_product_icon,
                                        font=("Inter", 18, "bold"),
                                        compound="left",
                                        fg_color="#372724",
                                        text_color="#EBE0D6", width=1000,
                                        command=switch_to_view_prod_frame)
      
      view_products_btn.pack(pady=10, padx=10)
      
      
      # END - products styling btn
      
      
      
      # # START - add products styling btn
      
      # add_prod_btn_icon = Image.open("./imgs/sidepanel_icons/add_prod_icon_light.png")
      # resized_icon = add_prod_btn_icon.resize((30, 40))
      # ctk_addprod_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))
      
      
      # add_prod_btn = CTk.CTkButton(side_panel, text="Add Products", image=ctk_addprod_icon,
      #                              font=("Inter", 18, "bold"),
      #                              compound="left",
      #                               fg_color="#372724",
      #                               text_color="#EBE0D6", width=1000,
      #                               command=switch_to_prod_frame)
      
      # add_prod_btn.pack(pady=10, padx=10)
      
      
      # # END - add products styling btn
      
      
      # == START Sales styling btn === 
      
      sales_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/sales_icon.png")
      resized_icon = sales_btn_icon.resize((30, 40))
      ctk_sales_btn_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))
      
      sales_btn = CTk.CTkButton(side_panel, text="Sales", image=ctk_sales_btn_icon,
                                font = ("Inter", 18, "bold"),
                                compound="left",
                                fg_color="#372724",
                                text_color="#EBE0D6", width=1000,
                                command=switch_to_sales_frame
                                )
      
      sales_btn.pack(pady=10, padx = 10)
      
      
      # == END Sales styling btn ===
      
      
      # == START Inventory styling btn ==

        
      inventory_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/inventory_icon.png")
      resized_icon = inventory_btn_icon.resize((30, 40))
      ctk_inventory_btn_icon = CTk.CTkImage(dark_image=resized_icon, size=(30, 30))
      
      inventory_btn = CTk.CTkButton(side_panel, text="Inventory", image=ctk_inventory_btn_icon,
                                font = ("Inter", 18, "bold"),
                                compound="left",
                                fg_color="#372724",
                                text_color="#EBE0D6", width=1000,
                                command=switch_to_inventory_frame
                                )
      
      inventory_btn.pack(pady=10, padx = 10)
      
      
      
      
      # == END Inventory styling btn
      
      
      
      # START - signout btn styling
      
      signout_btn_icon = Image.open("C:/Users/Dale Chavez/Downloads/PointOfSales_Oct26/PointOfSales/imgs/sidepanel_icons/sign_out_icon_light.png")
      resized_icon = signout_btn_icon.resize((30, 40))
      
      ctk_signout_icon = CTk.CTkImage(dark_image=resized_icon, size=(25, 30))
      
      signout_btn = CTk.CTkButton(side_panel, text="Sign Out", image=ctk_signout_icon,
                                  font=("Inter", 18, "bold"),
                                  compound="left",
                                  fg_color="#372724",
                                  text_color="#EBE0D6", width=1000,
                                  command=log_out_frame)
      
      signout_btn.pack(side = "bottom",pady = 10, padx=10)
      
      # END - signout btn styling
      

