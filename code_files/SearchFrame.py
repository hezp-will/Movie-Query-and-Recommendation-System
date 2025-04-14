import customtkinter as ctk
from SearchInput import SearchInputFrame


class SearchFrame(ctk.CTkFrame):
    def __init__(self, *args, header_name="SearchFrame", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.header_name = header_name

        self.header = ctk.CTkLabel(self, text=self.header_name, font=("Helvetica bold", 16))
        self.header.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        self.search_input_frame = SearchInputFrame(self)
        self.search_input_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="nswe")

        self.switch_var = ctk.StringVar(value='on')
        self.switch = ctk.CTkSwitch(master=self, text="Need A Recommended List?", variable=self.switch_var, onvalue='on', offvalue='off', height=30, width=50, font=("Helvetica bold", 16))
        self.switch.grid(row=2, column=0, padx=10, pady=(5, 10), )
    
    def get_value(self):
        """ returns entry values as a list"""
        return self.search_input_frame.get_value()