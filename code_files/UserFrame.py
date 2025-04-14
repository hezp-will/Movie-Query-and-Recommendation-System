import customtkinter as ctk


class UserFrame(ctk.CTkFrame):
    def __init__(self, *args, header_name="UserFrame", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        

        self.header_name = header_name
        self.header = ctk.CTkLabel(self, text=self.header_name, font=("Helvetica bold", 16))
        self.header.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        self.uid_input_var = ctk.StringVar(self, value="")
        self.uid_input_var.trace("w", self.uid_callback)
        self.uid_input = ctk.CTkEntry(master=self, placeholder_text="user id", textvariable=self.uid_input_var, width=100, height=25, border_width=2, corner_radius=10)
        self.uid_input.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        
        self.uid_label_var = ctk.StringVar(self, value="Enter User ID")
        self.uid_label = ctk.CTkLabel(self, text="User ID", textvariable=self.uid_label_var, font=("Helvetica bold", 16))
        self.uid_label.grid(row=1, column=1, padx=10, pady=10, sticky="nswe")
    
    def uid_callback(self, *args):
        if self.uid_input_var.get().isdigit():
            self.uid_label_var.set("Welcome User {uid}, you are logged in.".format(uid=self.uid_input_var.get()))
    def get_value(self):
        return self.uid_input_var.get()