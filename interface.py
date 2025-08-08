import customtkinter

class Interface:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("600x600")
        self.PADY = 5
        self.FONT = ("Times New Roman",20)
        self.app.protocol("WM_DELETE_WINDOW",self.__on_close)
        self.is_closed = False
        self.labels()


    def __on_close(self):
        self.is_closed = True
        self.app.destroy()

    def __confirm_button(self):
        self.__product = self.product_entry.get()
        self.__user_choice = self.option_menu_var.get()
        if not self.__product or not self.__user_choice:
            self.error_label.configure(fg_color="red",text="Пожалуста укажите товар!")
            return
        self.app.destroy()
        
    def labels(self):
        customtkinter.CTkLabel(self.app,text="Выберите интернет магазин",font=self.FONT).pack(pady=self.PADY)
        self.option_menu_var = customtkinter.StringVar(value="OLX")
        self.option_menu = customtkinter.CTkOptionMenu(self.app,values=["OLX","UZUM","Яндекс маркет","Озон"],variable=self.option_menu_var,width=300,font=self.FONT)
        self.option_menu.pack(pady=self.PADY)
        customtkinter.CTkLabel(self.app,text="Что вы хотите найти?",font=self.FONT).pack(pady=self.PADY)
        self.product_entry = customtkinter.CTkEntry(self.app,width=300,font=self.FONT,placeholder_text="Поиск")
        self.product_entry.pack(pady=self.PADY)
        self.confirm = customtkinter.CTkButton(self.app,width=300,text="Подтвердить",font=self.FONT,command=self.__confirm_button).pack(pady=self.PADY)
        self.error_label = customtkinter.CTkLabel(self.app,text="",font=self.FONT)
        self.error_label.pack(pady=self.PADY)
        self.app.mainloop()
    
    def get_informations(self):
        if not self.is_closed:
          return (self.__product,self.__user_choice,self.is_closed)
        else:
            return (self.is_closed)
