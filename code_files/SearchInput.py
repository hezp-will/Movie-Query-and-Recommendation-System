import customtkinter as ctk


class SearchInputFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.label1 = ctk.CTkLabel(self, text="Movie Name")
        self.label1.grid(row=0, column=0, padx=10, pady=10)

        self.input1 = ctk.CTkEntry(master=self, placeholder_text="movie name", width=300, height=25, border_width=2, corner_radius=10)
        self.input1.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        self.label2 = ctk.CTkLabel(self, text="Movie Tag")
        self.label2.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

        self.input2 = ctk.CTkEntry(master=self, placeholder_text="movie tag", width=300, height=25, border_width=2, corner_radius=10)
        self.input2.grid(row=1, column=1, padx=10, pady=10, sticky="nswe")

        self.label3 = ctk.CTkLabel(self, text="Movie Genre")
        self.label3.grid(row=2, column=0, padx=10, pady=10, sticky="nswe")

        self.input3 = ctk.CTkEntry(master=self, placeholder_text="movie genre", width=300, height=25, border_width=2, corner_radius=10)
        self.input3.grid(row=2, column=1, padx=10, pady=10, sticky="nswe")


    def get_value(self):
        """ returns entry values as a list"""
        return [self.input1.get(), self.input2.get(), self.input3.get()]