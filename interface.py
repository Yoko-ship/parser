import customtkinter

class Interface:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.app = customtkinter.CTk()
        self.app.geometry("600x600")
        self.PADY = 5
        self.FONT = ("Arial",14)
        self.app.protocol("WM_DELETE_WINDOW",self.__on_close)
        title = customtkinter.CTkLabel(
            self.app,
            text="Добро пожаловать в поиск товаров 🛒",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=20)

        self.is_closed = False
        self.is_multiple = False
        self.__product = ""
        self.__user_choice = ""
        self.__price = 0
        self.__multiple_price = 0
        self.checkbox_var = customtkinter.StringVar(value="Один сайт")
        self.checkbox = customtkinter.CTkSwitch(
            self.app,
            text="Режим: поиск по одному сайту / всем сайтам",
            variable=self.checkbox_var,
            onvalue="Один сайт",
            offvalue="Много сайтов",
            command=self.checkbox_event
        )
        self.checkbox.pack(pady=self.PADY)
        self.current_frame = self.create_single_site_frame()
        self.app.mainloop()


    def __on_close(self):
        self.is_closed = True
        self.app.destroy()

    def __confirm(self,is_multiple=False):
        if is_multiple:
            self.is_multiple = True    
            product = self.multiple_product_entry.get().strip()
            try:
                self.__multiple_price = int(self.multiple_price_entry.get().strip())
            except ValueError:
                self.error_multiple_labels.configure(fg_color="red",text="⚠ Укажите цену в цифрах!")
                return
            if not product:
                self.error_multiple_labels.configure(fg_color="red",text="⚠ Введите название товара")
                return
            
            self.multiple_products = product
            self.app.destroy()
        else:
            self.__product = self.product_entry.get().strip()
            self.__user_choice = self.option_menu_var.get().strip()
            try:
                self.__price = int(self.price_entry.get().strip())
            except ValueError:
                self.error_label.configure(fg_color="red",text="⚠ Укажите цену в цифрах!")
                return
            if not self.__product or not self.__user_choice:
                self.error_label.configure(fg_color="red",text="⚠ Введите название товара")
                return
            self.app.destroy()


    def checkbox_event(self):
        choice = self.checkbox_var.get()
        self.current_frame.destroy()
        if choice == "Один сайт":
            self.current_frame = self.create_single_site_frame()
        else:
            self.current_frame = self.create_multiple_site_frames()

    def create_single_site_frame(self):
        frame = self._create_frame()
        
        customtkinter.CTkLabel(frame,text="Выберите интернет магазин",font=self.FONT).pack(pady=self.PADY)
        self.option_menu_var = customtkinter.StringVar(value="OLX")
        self.option_menu = customtkinter.CTkOptionMenu(frame,values=["OLX","UZUM","Яндекс маркет","Озон"],variable=self.option_menu_var,width=300,font=self.FONT)
        self.option_menu.pack(pady=self.PADY)
        customtkinter.CTkLabel(frame,text="Что вы хотите найти?",font=self.FONT).pack(pady=self.PADY)
        self.product_entry = customtkinter.CTkEntry(frame,width=300,font=self.FONT,placeholder_text="Например: наушники")
        self.product_entry.pack(pady=self.PADY)
        customtkinter.CTkLabel(frame,text="Цена",font=self.FONT).pack(pady=self.PADY)
        self.price_entry = customtkinter.CTkEntry(frame,300,placeholder_text="До: ",font=self.FONT,height=35)
        self.price_entry.insert(customtkinter.END,0)
        self.price_entry.pack(pady=self.PADY)
        customtkinter.CTkButton(frame,width=300,text="🔍 Найти товар",font=self.FONT,command=lambda:self.__confirm(False)).pack(pady=self.PADY)
        self.error_label = customtkinter.CTkLabel(frame,text="",font=self.FONT)
        self.error_label.pack(pady=self.PADY)

        return frame
    
    def create_multiple_site_frames(self):
        frame_multiple = self._create_frame()
        customtkinter.CTkLabel(frame_multiple,text="Будет выполнен поиск по всем сайтам подряд.\nЭто может занять несколько минут ⏳",font=self.FONT).pack(pady=self.PADY)
        customtkinter.CTkLabel(frame_multiple,text="Что хотите найти",font=self.FONT).pack(pady=self.PADY)
        self.multiple_product_entry = customtkinter.CTkEntry(frame_multiple,width=300,font=self.FONT,placeholder_text="Поиск")
        self.multiple_product_entry.pack(pady=self.PADY)
        customtkinter.CTkLabel(frame_multiple,text="Цена",font=self.FONT).pack(pady=self.PADY)
        self.multiple_price_entry = customtkinter.CTkEntry(frame_multiple,300,placeholder_text="До: ",font=self.FONT,height=35)
        self.multiple_price_entry.insert(customtkinter.END,"0")
        self.multiple_price_entry.pack(pady=self.PADY)
        customtkinter.CTkButton(frame_multiple,width=300,font=self.FONT,command=lambda:self.__confirm(True),text="🔍 Найти товар").pack(pady=self.PADY)
        self.error_multiple_labels = customtkinter.CTkLabel(frame_multiple,text="",font=self.FONT)
        self.error_multiple_labels.pack(pady=self.PADY)
        return frame_multiple
    
    def _create_frame(self):
        frame = customtkinter.CTkFrame(self.app,corner_radius=15)
        frame.pack(pady=20,padx=20,fill='both',expand=True)
        return frame
    def get_informations(self):
        if not self.is_closed:
            if self.is_multiple:
                return (self.is_multiple,self.multiple_products,self.__multiple_price)
            return (self.__product,self.__user_choice,self.is_closed,self.__price)
        return (self.is_closed)
