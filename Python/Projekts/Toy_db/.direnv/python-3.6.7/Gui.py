#!/usr/bin/python3

"""
Goal: Demonstrate some minor database concepts
from popular databases like MySQL, PostgreSQL or Oracle.

Execution: Gui based

Contributor:
David Anthony Parham
"""

import hashlib
import json
import tkinter as tk
from itertools import count
from os import listdir
from os.path import dirname, isfile, join, realpath
from time import sleep
from tkinter import messagebox
from tkinter.ttk import Combobox

from password_strength import PasswordPolicy
from PIL import Image, ImageTk

# import the backend functionalities
import Database

FONT = ("Helvetica", 15)
IMG = "images/database.png"


# password rules
POLICY = PasswordPolicy.from_names(
    length=6,  # min length: 6
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


class ToyDB_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginPage, DatabasePage, StartPage, CreatePage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.database = None

    def show_frame(self, cont):
        """ show the different pages"""
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        welcome_msg = tk.Label(
            self,
            text=("Welcome, to the Database GUI Application!"),
            anchor="w",
            font=("Helvetica", 20),
        )
        welcome_msg.place(x=80, y=30, height=60)

        instruction_msg = tk.Label(
            self,
            text=("Introduction: Create and/or manage existing databases"),
            anchor="w",
            font=FONT,
        )
        instruction_msg.place(x=80, y=170, height=60)

        img = ImageTk.PhotoImage(Image.open(IMG))
        img_label = tk.Label(self, image=img)
        img_label.image = img
        img_label.place(x=620, y=85, width=100, height=123)

        create_database_button = tk.Button(
            self,
            text="Create Database",
            command=lambda: controller.show_frame(CreatePage),
            font=FONT,
        )
        create_database_button.place(x=80, y=270, width=200, height=40)

        existing_database_button = tk.Button(
            self,
            text="Use existing Database",
            command=lambda: controller.show_frame(LoginPage),
            font=FONT,
        )
        existing_database_button.place(x=400, y=270, width=250, height=40)


class CreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.database_id = tk.StringVar()
        database_name = tk.Label(self, text=("Database Name: "), anchor="w", font=FONT)
        database_name.place(x=140, y=30, width=200, height=30)
        self.database_entry = tk.Entry(self, textvariable=self.database_id, font=FONT)
        self.database_entry.place(x=400, y=30, width=200, height=30)

        self.user_id = tk.StringVar()
        admin_user = tk.Label(self, text=("Admin Name: "), anchor="w", font=FONT)
        admin_user.place(x=140, y=80, width=200, height=30)
        self.user_entry = tk.Entry(self, textvariable=self.user_id, font=FONT)
        self.user_entry.place(x=400, y=80, width=200, height=30)

        self.password_id = tk.StringVar()
        admin_password = tk.Label(self, text=("Admin Password:"), anchor="w", font=FONT)
        admin_password.place(x=140, y=130, width=200, height=30)
        self.password_entry = tk.Entry(self, textvariable=self.password_id, font=FONT)
        self.password_entry.place(x=400, y=130, width=200, height=30)

        self.confirm_password_id = tk.StringVar()
        confirm_admin_password = tk.Label(
            self, text=("Confirm Password:"), anchor="w", font=FONT
        )
        confirm_admin_password.place(x=140, y=180, width=200, height=30)
        self.confirm_user_entry = tk.Entry(
            self, textvariable=self.confirm_password_id, font=FONT
        )
        self.confirm_user_entry.place(x=400, y=180, width=200, height=30)

        enter_button = tk.Button(
            self,
            text="OK",
            command=lambda: self.create_database(
                self.database_id,
                self.user_id,
                self.password_id,
                self.confirm_user_entry,
                controller,
            ),
            font=FONT,
        )
        enter_button.place(x=140, y=270, width=120, height=40)

        cancel_button = tk.Button(
            self, text="Quit", command=controller.destroy, font=FONT
        )
        cancel_button.place(x=310, y=270, width=120, height=40)

        restart_button = tk.Button(
            self, text="Restart", command=lambda: self.clear_text(), font=FONT
        )
        restart_button.place(x=480, y=270, width=120, height=40)

        return_button = tk.Button(
            self, text="←", command=lambda: controller.show_frame(StartPage), font=FONT
        )
        return_button["border"] = "0"
        return_button.place(x=10, y=10, width=40, height=20)

    def clear_text(self):
        """empty all input fields"""
        for input_field in [
            self.confirm_user_entry,
            self.database_entry,
            self.user_entry,
            self.password_entry,
        ]:
            input_field.delete(0, "end")
        return True

    def create_database(self, database, user, password, confirm_password, controller):
        """create a database"""
        database = database.get()
        username = user.get()
        password = password.get()
        password_similarity = confirm_password.get()
        controller.database = database

        if password == password_similarity:
            if len(POLICY.test(password)) == 0:
                Database.mode_db(
                    mode=1,
                    db_name=database,
                    username=username,
                    password=password,
                    terminal=False,
                )
                messagebox.showinfo(
                    "Create database",
                    "Successfully created database: {}".format(database),
                )
                controller.show_frame(DatabasePage)

            else:
                messagebox.showinfo(
                    "Error: Password strength",
                    """\nYour password is not strong enough.\nPlease make sure to uphold the password policy:\nAt least 6 characters\n1 uppercase\n1. digit\n1. special character""",
                )
        else:
            messagebox.showinfo(
                "Error: Password", "Passwords do not match. Please try again"
            )

        return True


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.hidden = True
        self.bind("<<ShowFrame>>", self.on_show_frame)

        database_name = tk.Label(self, text="Database: ", anchor="w", font=FONT)
        database_name.place(x=140, y=30, width=200, height=30)
        self.drop_down = Combobox(self, font=FONT)
        self.drop_down["value"] = self.databases_in_directory()
        self.drop_down.current(0)
        self.drop_down.place(x=400, y=30, width=200, height=30)

        self.user_id = tk.StringVar()
        user_name = tk.Label(self, text="Username: ", anchor="w", font=FONT)
        user_name.place(x=140, y=80, width=200, height=30)
        user_entry = tk.Entry(self, textvariable=self.user_id, font=FONT)
        user_entry.place(x=400, y=80, width=200, height=30)

        self.pw_id = tk.StringVar()
        pw = tk.Label(self, text="Password: ", anchor="w", font=FONT)
        pw.place(x=140, y=130, width=200, height=30)
        self.pw_entry = tk.Entry(self, show="*", textvariable=self.pw_id, font=FONT)
        self.pw_entry.place(x=400, y=130, width=200, height=30)

        check_button = tk.Checkbutton(
            self, text="Show Password", command=self.password, font=FONT
        )
        check_button.place(x=400, y=180, width=180, height=40)

        enter_button = tk.Button(
            self,
            text="OK",
            command=lambda: self.check_credentials(
                self.user_id, self.pw_id, self.drop_down, controller
            ),
            font=FONT,
        )
        enter_button.place(x=140, y=270, width=120, height=40)

        cancel_button = tk.Button(
            self, text="Quit", command=controller.destroy, font=FONT
        )
        cancel_button.place(x=480, y=270, width=120, height=40)

        return_button = tk.Button(
            self, text="←", command=lambda: controller.show_frame(StartPage), font=FONT
        )
        return_button["border"] = "0"
        return_button.place(x=10, y=10, width=40, height=20)

    def on_show_frame(self, event):
        self.drop_down["value"] = self.databases_in_directory()

    def password(self):
        """ Show/hide password """
        if self.hidden:
            self.pw_entry.configure(show="")
            self.hidden = False
        else:
            self.pw_entry.configure(show="*")
            self.hidden = True
        return True

    def check_credentials(self, user, password, db, controller):
        """check if the credentials belong to this database"""

        print("Trying to login...")

        def encrypt_string(hash_string):
            sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
            return sha_signature

        try:
            db_name = db.get().split("  ")[1]
            user_data = self.get_db(db_name)
            user = user.get()
            password = password.get()
            password = encrypt_string(password)
            controller.database = db_name
            data = user_data.get("credentials")

        except IndexError:
            messagebox.showerror(
                "Login failed!",
                "There are no existing databases yet. Please create some first",
                icon="warning",
            )
            return False

        if user in data:
            if data.get(user) == password:
                print("Connection with Database has been established")
                controller.show_frame(DatabasePage)
            else:
                messagebox.showinfo(
                    "Login failed!",
                    "Your username/password is invalid. Please try again.",
                )

        else:
            print("Wrong user or password has been entered")
        return True

    def get_db(self, database):
        """get database from current path"""
        with open(database, "r") as file:
            data = json.load(file)
            return data

    def databases_in_directory(self):
        """display all files with the '.db' extension in the current path"""
        mypath = dirname(realpath(__file__))
        counter = count(0)
        database = [
            "{}:  {}".format(next(counter), f)
            for f in listdir(mypath)
            if isfile(join(mypath, f)) and "db" in f
        ]
        if database is None or database == []:
            database = ["---No databases---"]
        return database


class DatabasePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        database_event = tk.Label(self, text="Database events: ", anchor="w", font=FONT)
        database_event.place(x=140, y=30, width=200, height=30)

        self.drop_down = Combobox(self, font=FONT)
        self.drop_down["value"] = self.database_events()
        self.drop_down.current(0)
        self.drop_down.place(x=350, y=30, width=350, height=30)

        self.table_id = tk.StringVar()
        table = tk.Label(self, text="Table: ", anchor="w", font=FONT)
        table.place(x=140, y=80, width=200, height=30)
        self.table_entry = tk.Entry(self, textvariable=self.table_id, font=FONT)
        self.table_entry.place(x=350, y=80, width=350, height=30)

        self.key_id = tk.StringVar()
        table_key = tk.Label(self, text="Key: ", anchor="w", font=FONT)
        table_key.place(x=140, y=130, width=200, height=30)
        self.table_key_entry = tk.Entry(self, textvariable=self.key_id, font=FONT)
        self.table_key_entry.place(x=350, y=130, width=350, height=30)

        self.value_id = tk.StringVar()
        table_value = tk.Label(self, text="Value: ", anchor="w", font=FONT)
        table_value.place(x=140, y=180, width=200, height=30)
        self.table_value_entry = tk.Entry(self, textvariable=self.value_id, font=FONT)
        self.table_value_entry.place(x=350, y=180, width=350, height=30)

        enter_button = tk.Button(
            self,
            text="OK",
            command=lambda: self.execute_event(
                self.drop_down, controller, self.table_id, self.key_id, self.value_id
            ),
            font=FONT,
        )
        enter_button.place(x=140, y=270, width=120, height=40)

        cancel_button = tk.Button(
            self, text="Quit", command=controller.destroy, font=FONT
        )
        cancel_button.place(x=480, y=270, width=120, height=40)

        return_button = tk.Button(
            self,
            text="Logout",
            command=lambda: controller.show_frame(StartPage),
            font=FONT,
        )
        return_button["border"] = "0"
        return_button.place(x=10, y=10, width=60, height=30)

    def database_events(self):
        """display all database events in the drop_down box"""
        event_lst = [
            "Insert entity in table",
            "Get instance from table",
            "Delete instance from table",
            "Delete table",
            "Create table",
            "Delete database",
            "Reset database",
        ]
        counter = count(0)
        events = ["{}:  {}".format(next(counter), f) for f in event_lst]

        return events

    def execute_event(self, event, controller, table=None, key=None, value=None):
        """execute the specific event through the backend"""
        mode = str(int(event.get()[0]) + 2)
        table = table.get()
        key = key.get()
        value = value.get()
        db_name = controller.database

        if mode == "2":
            messagebox.showinfo(
                "Insert Process msg",
                "{}".format(
                    Database.mode_db(
                        mode=mode,
                        db_name=db_name,
                        table=table,
                        key=key,
                        value=value,
                        terminal=False,
                    )
                ),
            )
        elif mode in "34":
            messagebox.showinfo(
                "Instance value:",
                "{}".format(
                    Database.mode_db(
                        mode=mode, db_name=db_name, table=table, key=key, terminal=False
                    )
                ),
            )
        elif mode in "56":
            messagebox.showinfo(
                "Table events:",
                "{}".format(
                    Database.mode_db(
                        mode=mode, db_name=db_name, table=table, terminal=False
                    )
                ),
            )

        elif mode in "78":
            mode = str(int(mode) + 1)
            self.query(mode, db_name, controller)
        self.clear_text()
        return True

    def query(self, mode, db_name, controller):
        """check if user really want's to proceed with this event"""
        msg_box = messagebox.askquestion(
            "Delete/Reset database",
            "Are you sure to delete/reset this database?",
            icon="warning",
        )
        if msg_box == "yes":
            messagebox.showinfo(
                "Delete/reset Database:",
                "{}".format(
                    Database.mode_db(mode=mode, db_name=db_name, terminal=False)
                ),
            )

            if mode == "8":
                controller.show_frame(StartPage)

        else:
            messagebox.showinfo(
                "Return", "You will return to the Database events screen"
            )

        return True

    def clear_text(self):
        """empty all input fields"""
        for input_field in [
            self.table_entry,
            self.table_key_entry,
            self.table_value_entry,
        ]:
            input_field.delete(0, "end")
        return True


if __name__ == "__main__":
    app = ToyDB_GUI()
    app.wm_title("Database GUI Application")
    app.wm_geometry("750x350")
    app.mainloop()
