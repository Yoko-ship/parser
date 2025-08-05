import customtkinter

class Interface:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("600x600")
        self.PADY = 5
        self.FONT = ("Times New Roman",20)
        self.labels()

    def __confirm_button(self):
        self.__url = self.url_entry.get()
        self.__product = self.product_entry.get()
        self.app.destroy()
    
    def labels(self):
        customtkinter.CTkLabel(self.app,text="Ссылка на сайт",font=self.FONT).pack(pady=self.PADY)
        self.url_entry = customtkinter.CTkEntry(self.app,placeholder_text="Url",width=300,font=self.FONT)
        self.url_entry.pack(pady=self.PADY)
        customtkinter.CTkLabel(self.app,text="Что вы хотите найти?",font=self.FONT).pack(pady=self.PADY)
        self.product_entry = customtkinter.CTkEntry(self.app,width=300,font=self.FONT,placeholder_text="Поиск")
        self.product_entry.pack(pady=self.PADY)
        self.confirm = customtkinter.CTkButton(self.app,width=300,text="Подтвердить",font=self.FONT,command=self.__confirm_button).pack(pady=self.PADY)
        self.app.mainloop()
    
    def get_informations(self):
        return (self.__url,self.__product)
    
