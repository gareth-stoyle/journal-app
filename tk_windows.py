import customtkinter
import tkinter
from datetime import datetime
import db_functions

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Journal")
        self.geometry(f"{800}x{300}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")
        date = datetime.now().strftime("%d/%m/%Y")
        self.date_label = customtkinter.CTkLabel(self.sidebar_frame, text=date, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.date_label.grid(padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(padx=20, pady=(10, 20))

        # create textbox and submit button
        self.textbox = customtkinter.CTkTextbox(self, width=200)
        self.textbox.grid(row=0, rowspan=1, column=1, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.submit_button = customtkinter.CTkButton(self, text="Submit", height=35, command=self.submit)
        self.submit_button.grid(column=1, row=1, rowspan=1, padx=(20, 20), pady=(5, 20), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")        
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def refresh_window(self):
        self.update()
        self.update_idletasks()
    

    def submit(self):
        try:
            db = db_functions.DB()
            entry = self.textbox.get("1.0",'end-1c')
            db.submit_journal_entry(entry, datetime.now())
            tkinter.messagebox.showinfo("Success!", "Journal entry logged.")
            # refresh text entry
            self.textbox.delete('1.0', customtkinter.END)
            # refresh date label
            date = datetime.now().strftime("%d/%m/%Y")
            self.date_label.configure(text=date)
        except Exception as e:
            print(e)
            tkinter.messagebox.showerror("Error", e)
        


class LoginWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

        self.geometry("500x350")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(self.frame, text="Login System", font=("Robot", 24))
        self.label.pack(pady=12, padx=10)

        self.username_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=12, padx=10)

        self.button = customtkinter.CTkButton(self.frame, text="Login", command=self.login)
        self.button.pack(pady=12, padx=10)

        #not used atm
        self.checkbox = customtkinter.CTkCheckBox(self.frame, text="Remember me")
        self.checkbox.pack(pady=12, padx=10)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        db = db_functions.DB()
        if db.login(username, password):
            # unsure this is best way to get rid of login window
            # but destroy and quit are not working
            self.withdraw()
            app = MainWindow()
            app.mainloop()
        else:
            tkinter.messagebox.showerror("login failed","Please try again" )