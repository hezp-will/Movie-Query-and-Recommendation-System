import customtkinter as ctk
import tkinter as tk


class ResultFrame(ctk.CTkScrollableFrame):
    def __init__(self, *args, header_name="ResultFrame", **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.header_name = header_name
        self.header = ctk.CTkLabel(self, text='Search Results', font=("Helvetica bold", 16))
        self.header.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nswe")

        # self.result = tk.Listbox(self, width=100, height=20)
        # self.result.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        self.scrollbar = ctk.CTkScrollbar(self)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.grid(row=1, column=1, sticky="nswe")

        # Create a Listbox widget
        self.listbox = tk.Listbox(self, yscrollcommand=self.scrollbar.set)

        # listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

        # Attach the scrollbar to the Listbox widget
        self.scrollbar.configure(command=self.listbox.yview)

        self.recomm_label = ctk.CTkLabel(self, text='Recommended List', font=("Helvetica bold", 16))
        self.recomm_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nswe")

        self.scrollbar2 = ctk.CTkScrollbar(self)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar2.grid(row=3, column=1, sticky="nswe")

        # Create a Listbox widget
        self.listbox2 = tk.Listbox(self, yscrollcommand=self.scrollbar2.set)

        # listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox2.grid(row=3, column=0, padx=10, pady=10, sticky="nswe")

        # Attach the scrollbar to the Listbox widget
        self.scrollbar.configure(command=self.listbox2.yview)

        self.scrollbar3 = ctk.CTkScrollbar(self)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar3.grid(row=6, column=1, sticky="nswe")

        # Create a Listbox widget
        self.listbox3 = tk.Listbox(self, yscrollcommand=self.scrollbar3.set)

        # listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox3.grid(row=6, column=0, padx=10, pady=10, sticky="nswe")

        self.want_label = ctk.CTkLabel(self, text='Want List', font=("Helvetica bold", 16))
        self.want_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="nswe")

        self.move_button = ctk.CTkButton(self, text="Move to the Want List", command=lambda: self.move_selected_item(self.listbox,
                                                                                                    self.listbox2,
                                                                                                    self.listbox3))
        self.move_button.grid(row=4, column=0, padx=10, pady=10, sticky="nswe")

    def move_selected_item(self, from_listbox1, from_listbox2, to_listbox):
        # Get the index of the selected item in both source listboxes
        selected_indices1 = from_listbox1.curselection()
        selected_indices2 = from_listbox2.curselection()

        # Loop through the selected indices in from_listbox1 and move the items
        for index in selected_indices1:
            item = from_listbox1.get(index)
            to_listbox.insert(ctk.END, item)

        # Loop through the selected indices in from_listbox2 and move the items
        for index in selected_indices2:
            item = from_listbox2.get(index)
            to_listbox.insert(ctk.END, item)


