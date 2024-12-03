from tkinter import *
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pystray
import time
import json
import random
import string
import os
import keyboard
import subprocess
import sys
import ctypes
from PIL import Image, ImageDraw


Mentry = ''


def hide_file(file_path):
    # Set the file attribute to hidden
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)

def show_file(file_path):
    # Set the file attribute to normal (not hidden)
    FILE_ATTRIBUTE_NORMAL = 0x80
    ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_NORMAL)


# Functions
def setup_master_password():
    try:
        with open('master_password.json', 'r') as file:
            data = json.load(file)
            stored_master_password = data.get('master_password')

            if stored_master_password:
                return stored_master_password
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # If no master password is found, initiate first-time setup
    int_start.setup_window = ctk.CTk()

    StartLb = ctk.CTkLabel(int_start.setup_window,
                           text="This is your first time start up.\n Please input what you want the master "
                                "password to be.\n Once you input this it can not be changed!",
                           font=('Simple bold Jut Out', 15))
    StartLb.pack(pady=10)
    width = 600  # Width
    height = 400  # Height
    screen_width = int_start.setup_window.winfo_screenwidth()  # Width of the screen
    screen_height = int_start.setup_window.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    int_start.setup_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    int_start.setup_window.title("Check")
    ctk.set_appearance_mode("dark")
    master_password_entry = ctk.CTkEntry(int_start.setup_window, placeholder_text="Master Password",
                                         font=('Simple bold Jut Out', 15))
    submit_button = ctk.CTkButton(int_start.setup_window, text="Submit", font=('Simple bold Jut Out', 15),
                                  command=lambda: submit_master_password(master_password_entry.get(),
                                                                         int_start.setup_window))

    master_password_entry.pack(pady=10)
    submit_button.pack(pady=10)

    int_start.setup_window.mainloop()


def submit_master_password(master_password, setup_window):
    confirmation = messagebox.askquestion("Confirmation",
                                          "Are you sure you want to set this as your master password?\n It can not be changed once submitted.")
    if confirmation == 'yes':
        data = {"master_password": master_password}
        with open('master_password.json', 'w') as file:
            json.dump(data, file)

        wind2_from_star()


def generate_strong_password(length=12):
    # Define character sets for password generation
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine character sets
    all_characters = uppercase_letters + lowercase_letters + digits + special_characters

    # Ensure at least one character from each set is included
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_characters)
    ]

    # Generate remaining characters
    password += [random.choice(all_characters) for _ in range(length - 4)]

    # Shuffle the password to make it more random
    random.shuffle(password)

    # Convert the list to a string
    return ''.join(password)


def wind2_from_star():
    int_start.setup_window.destroy()
    windowEntry.EWindow = ctk.CTk()

    # setting tkinter window size
    width = 600  # Width
    height = 500  # Height
    screen_width = windowEntry.EWindow.winfo_screenwidth()  # Width of the screen
    screen_height = windowEntry.EWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    windowEntry.EWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))

    IntroLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Welcome to your password manager",
                           font=('Simple bold Jut Out', 30))
    IntroLb.pack(pady=20)

    addLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Here you can add a new account", font=('Simple bold '
                                                                                                  'Jut Out', 18))
    addLb.pack(pady=2)

    accountAdd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="account")
    accountAdd.pack(pady=2)

    accountUser = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="username or email")
    accountUser.pack(pady=2)

    passadd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="password")
    passadd.pack(pady=2)


    def save():

        saveacc = accountAdd.get()
        savepass = passadd.get()
        saveUser = accountUser.get()

        data_to_save = {
            "account": saveacc,
            "password": savepass,
            "username": saveUser
        }

        json_file_path = "Pass.json"
        save_to_json_file(json_file_path, data_to_save)
        test()

    def save_to_json_file(file_path, new_data):

        try:
            # Try to read existing data from the file
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, start with an empty dictionary
            existing_data = {"Accounts": []}

        # Append the new data to the existing "Accounts" list
        existing_data["Accounts"].append(new_data)

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)


    subBt = ctk.CTkButton(windowEntry.EWindow, text="Submit new account ", command=save)
    subBt.pack(pady=6)

    EditBt = ctk.CTkButton(windowEntry.EWindow, text="Edit an account", command=Edit)
    EditBt.pack(pady=6)

    viewBt = ctk.CTkButton(windowEntry.EWindow, text="View passwords", command=viewPage)
    viewBt.pack(pady=6)
    def generate_and_display_password():
        generated_password = generate_strong_password()
        # Display the generated password in a Label
        password_label.configure(text=f"Generated Password: {generated_password}")

    generate_button = ctk.CTkButton(windowEntry.EWindow, text="Generate Password", command=generate_and_display_password)
    generate_button.pack(pady=6)

    # Label to display the generated password
    password_label = ctk.CTkTextbox(
        windowEntry.EWindow,
        font=('Simple bold Jut Out', 12),
        width=300,
        height=25,
        wrap="word"
    )
    password_label.pack(pady=6)

    Quit = ctk.CTkButton(windowEntry.EWindow, text="Close", command=close_wind2)
    Quit.pack(pady=6)

    windowEntry.EWindow.mainloop()


def wind2():
    Auth.CWindow.destroy()
    windowEntry.EWindow = ctk.CTk()
    # setting tkinter window size
    width = 600  # Width
    height = 500  # Height
    screen_width = windowEntry.EWindow.winfo_screenwidth()  # Width of the screen
    screen_height = windowEntry.EWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    windowEntry.EWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))

    IntroLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Welcome to your password manager",
                           font=('Simple bold Jut Out', 30))
    IntroLb.pack(pady=20)

    addLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Here you can add a new account", font=('Simple bold '
                                                                                                  'Jut Out', 18))
    addLb.pack(pady=2)

    accountAdd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="account")
    accountAdd.pack(pady=2)

    accountUser = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="username or email")
    accountUser.pack(pady=2)

    passadd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="password")
    passadd.pack(pady=2)



    def save():

        saveacc = accountAdd.get()
        savepass = passadd.get()
        saveUser = accountUser.get()

        data_to_save = {
            "account": saveacc,
            "password": savepass,
            "username": saveUser
        }

        json_file_path = "Pass.json"
        save_to_json_file(json_file_path, data_to_save)
        test()

    def save_to_json_file(file_path, new_data):

        try:
            # Try to read existing data from the file
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, start with an empty dictionary
            existing_data = {"Accounts": []}

        # Append the new data to the existing "Accounts" list
        existing_data["Accounts"].append(new_data)

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

    subBt = ctk.CTkButton(windowEntry.EWindow, text="Submit new account ", command=save)
    subBt.pack(pady=6)

    EditBt = ctk.CTkButton(windowEntry.EWindow, text="Edit an account", command=Edit)
    EditBt.pack(pady=6)

    viewBt = ctk.CTkButton(windowEntry.EWindow, text="View passwords", command=viewPage)
    viewBt.pack(pady=6)

    def generate_and_display_password():
        generated_password = generate_strong_password()
        password_label.configure(state="normal")  # Temporarily set it to normal to modify text
        password_label.delete("1.0", ctk.END)  # Clear any previous text
        password_label.insert("1.0", f"Generated Password: {generated_password}")  # Insert the new password
        password_label.configure(state="disabled")

    generate_button = ctk.CTkButton(windowEntry.EWindow, text="Generate Password", command=generate_and_display_password)
    generate_button.pack(pady=6)

    # Label to display the generated password
    password_label = ctk.CTkTextbox(
        windowEntry.EWindow,
        font=('Simple bold Jut Out', 12),
        width=300,
        height=25,
        wrap="word"
    )
    password_label.pack(pady=6)

    Quit = ctk.CTkButton(windowEntry.EWindow, text="Close", command=close_wind2)
    Quit.pack(pady=6)

    windowEntry.EWindow.mainloop()


def test():
    messagebox.showinfo("Submission", "Account added")
    hide_file('super_secret.json')
    hide_file('master_password.json')


def Edit():
    windowEntry.EWindow.destroy()
    edit.editWindow = ctk.CTk()
    width = 600  # Width
    height = 500  # Height
    screen_width = edit.editWindow.winfo_screenwidth()  # Width of the screen
    screen_height = edit.editWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    edit.editWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))

    explainLb = ctk.CTkLabel(master=edit.editWindow, text="First what account do you want to change?",
                             font=('Simple bold Jut Out', 18))
    explainLb.pack(pady=8)

    SearchAccount = ctk.CTkEntry(master=edit.editWindow, placeholder_text="What account do you want to change?",
                                 font=('Simple bold Jut Out', 12))
    SearchAccount.pack(pady=4)

    acc_lookup = SearchAccount.get()
    acc_lookup = str(acc_lookup)

    def LookUp():
        searchList = []  # The list where we will store results.
        lineNum = 0
        global answer
        searchText = SearchAccount.get()
        substr = searchText.lower()  # Substring to search for.
        with open('Pass.json', 'rt') as myfile:
            for line in myfile:
                lineNum += 1
                if line.lower().find(substr) != -1:  # if case-insensitive match,
                    searchList.append("Line " + str(lineNum) + ": " + line.rstrip('\n'))
                    for SL in searchList:
                        answer = SL
                        print(answer)
                        print(acc_lookup)
        myfile.close()

    LookUpBt = ctk.CTkButton(master=edit.editWindow, text="Submit", font=('Simple bold Jut Out', 12), command=LookUp)
    LookUpBt.pack(pady=2)

    explainLb2 = ctk.CTkLabel(master=edit.editWindow, text="Now input all the new information you want to change",
                              font=('Simple bold Jut Out', 18))
    explainLb2.pack(pady=8)

    accountUser = ctk.CTkEntry(master=edit.editWindow, placeholder_text="username or email",
                               font=('Simple bold Jut Out', 12))
    accountUser.pack(pady=4)

    passadd = ctk.CTkEntry(master=edit.editWindow, placeholder_text="password", font=('Simple bold Jut Out', 12))
    passadd.pack(pady=4)
    input_new_user = accountUser.get()
    input_new_pass = passadd.get()
    acc_lookup = SearchAccount.get()

    def update_user(json_file, accounts, new_data):
        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Find the user with the given ID
        for user in data['Accounts']:
            if user['account'] == accounts:
                # Update user information
                user.update(new_data)
                break

        # Write the updated data back to the JSON file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

    def test_script():
        new_data = {
            "password": passadd.get(),
            "username": accountUser.get()
        }
        print(f"Acc_lookup: {acc_lookup}")
        print(f"New Data: {new_data}")
        update_user('Pass.json', SearchAccount.get(), new_data)
        test2()

    subBt = ctk.CTkButton(edit.editWindow, text="Submit Changes ", font=('Simple bold Jut Out', 12),
                          command=test_script)
    subBt.pack()
    BackBt = ctk.CTkButton(master=edit.editWindow, text="Back", font=('Simple bold Jut Out', 12),
                           command=back_from_edit)
    BackBt.pack(pady=8)
    Quit = ctk.CTkButton(master=edit.editWindow, text="Close", font=('Simple bold Jut Out', 12),
                         command=close_edit)
    Quit.pack(pady=8)
    edit.editWindow.mainloop()

def test2():
    messagebox.showinfo("Submission", "Account changed")


def viewPage():
    view.scroll = ctk.CTk()
    width = 600  # Width
    height = 500  # Height
    screen_width = view.scroll.winfo_screenwidth()  # Width of the screen
    screen_height = view.scroll.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    view.scroll.geometry('%dx%d+%d+%d' % (width, height, x, y))
    windowEntry.EWindow.destroy()

    def search_account():
        search_term = entry.get()
        found_account = next((account for account in accounts if account['account'].lower() == search_term.lower()),
                             None)

        if found_account:
            account_info = f"Account: {found_account['account']}, Username: {found_account['username']}, Password: {found_account['password']}"
            conLb = ctk.CTkTextbox(
                master=view.scroll,
                font=('Simple bold Jut Out', 15),
                width=500,
                height=100,  # Adjust the height as needed
                wrap="word"  # Ensure text wraps nicely if it's long
            )
            conLb.pack(pady=6)
            conLb.configure(state="normal")  # Temporarily make it editable
            conLb.delete("1.0", ctk.END)  # Clear any previous content
            conLb.insert("1.0", account_info)  # Insert the new account info
            conLb.configure(state="disabled")
        else:
            not_found_label = ctk.CTkLabel(master=view.scroll, text=f"Account '{search_term}' not found",
                                           font=('Simple bold Jut Out', 15), foreground='red')
            not_found_label.pack()

    with open('Pass.json', 'r') as file:
        data = json.load(file)
        accounts = data.get('Accounts', [])

    vlb1 = ctk.CTkLabel(view.scroll, text="Your accounts can be viewed here", font=('Simple bold Jut Out', 16))
    ##vlb1.pack(pady=10)
    for account in accounts:
        account_info = f"Account: {account['account']}, Username: {account['username']}, Password: {account['password']}"
        conLb = ctk.CTkLabel(master=view.scroll, text=account_info, font=('Simple bold Jut Out', 15))
        ##conLb.pack()


    vlb2 = ctk.CTkLabel(view.scroll, text="Here you can search for accounts", font=('Simple bold Jut Out', 16))
    vlb2.pack(pady=10)

    entry = ctk.CTkEntry(view.scroll, font=('Simple bold Jut Out', 15))
    entry.pack(pady=6)

    search_button = ctk.CTkButton(view.scroll, text="Search", font=('Simple bold Jut Out', 15), command=search_account)
    search_button.pack(pady=6)

    BackBt = ctk.CTkButton(master=view.scroll, text="Back", font=('Simple bold Jut Out', 15), command=back_from_view)
    BackBt.pack(pady=6)

    #QuitBt = ctk.CTkButton(master=view.scroll, text="Close", font=('Simple bold Jut Out', 15), command=close_view)
    #QuitBt.pack(pady=6)

    view.scroll.mainloop()


def close_view():
    result = messagebox.askokcancel("Confirmation", "Are you sure you want to close the application?")
    if result:

        view.VWindow.destroy()
        os.system("taskkill /F /PID {}".format(os.getpid()))



def close_wind2():
    result = messagebox.askokcancel("Confirmation", "Are you sure you want to close the application?")
    if result:
        Auth.CWindow = ctk.CTk()
        windowEntry.EWindow.destroy()
        global Mentry
        # Access window1 from windowStart class
        width = 600  # Width
        height = 400  # Height
        screen_width = Auth.CWindow.winfo_screenwidth()  # Width of the screen
        screen_height = Auth.CWindow.winfo_screenheight()  # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        Auth.CWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
        Auth.CWindow.title("Check")
        ctk.set_appearance_mode("dark")
        lb1 = ctk.CTkLabel(Auth.CWindow, text="What is your master password?", font=('Simple bold Jut Out', 15))
        lb1.pack()

        Mentry = ctk.CTkEntry(Auth.CWindow)
        Mentry.pack(pady=10)

        bt1 = ctk.CTkButton(Auth.CWindow, text="enter", command=check_master_password)
        bt1.pack()

        bt2 = ctk.CTkButton(Auth.CWindow, text="Close", command=lambda: hide_window(Auth.CWindow))
        bt2.pack(pady=10)

        Auth.CWindow.protocol("WM_DELETE_WINDOW", lambda: hide_window(Auth.CWindow))

        Auth.CWindow.mainloop()

        #os.system("taskkill /F /PID {}".format(os.getpid()))


def close_edit():
    result = messagebox.askokcancel("Confirmation", "Are you sure you want to close the application?")
    if result:

        edit.editWindow.destroy()
        os.system("taskkill /F /PID {}".format(os.getpid()))


def back_from_edit():
    edit.editWindow.destroy()
    windowEntry.EWindow = ctk.CTk()
    # setting tkinter window size
    width = 600  # Width
    height = 500  # Height
    screen_width = windowEntry.EWindow.winfo_screenwidth()  # Width of the screen
    screen_height = windowEntry.EWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    windowEntry.EWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))

    IntroLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Welcome to your password manager",
                           font=('Simple bold Jut Out', 30))
    IntroLb.pack(pady=20)

    addLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Here you can add a new account", font=('Simple bold '
                                                                                                  'Jut Out', 18))
    addLb.pack(pady=2)

    accountAdd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="account")
    accountAdd.pack(pady=2)

    accountUser = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="username or email")
    accountUser.pack(pady=2)

    passadd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="password")
    passadd.pack(pady=2)

    def save():

        saveacc = accountAdd.get()
        savepass = passadd.get()
        saveUser = accountUser.get()

        data_to_save = {
            "account": saveacc,
            "password": savepass,
            "username": saveUser
        }

        json_file_path = "Pass.json"
        save_to_json_file(json_file_path, data_to_save)
        test()

    def save_to_json_file(file_path, new_data):

        try:
            # Try to read existing data from the file
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, start with an empty dictionary
            existing_data = {"Accounts": []}

        # Append the new data to the existing "Accounts" list
        existing_data["Accounts"].append(new_data)

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

    subBt = ctk.CTkButton(windowEntry.EWindow, text="Submit new account ", command=save)
    subBt.pack(pady=6)

    EditBt = ctk.CTkButton(windowEntry.EWindow, text="Edit an account", command=Edit)
    EditBt.pack(pady=6)

    viewBt = ctk.CTkButton(windowEntry.EWindow, text="View passwords", command=viewPage)
    viewBt.pack(pady=6)

    Quit = ctk.CTkButton(windowEntry.EWindow, text="Close", command=close_wind2)
    Quit.pack(pady=6)

    windowEntry.EWindow.mainloop()


def back_from_view():
    windowEntry.EWindow = ctk.CTk()
    view.scroll.destroy()
    # setting tkinter window size
    width = 600  # Width
    height = 500  # Height
    screen_width = windowEntry.EWindow.winfo_screenwidth()  # Width of the screen
    screen_height = windowEntry.EWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    windowEntry.EWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))

    IntroLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Welcome to your password manager",
                           font=('Simple bold Jut Out', 30))
    IntroLb.pack(pady=20)

    addLb = ctk.CTkLabel(master=windowEntry.EWindow, text="Here you can add a new account", font=('Simple bold '
                                                                                                  'Jut Out', 18))
    addLb.pack(pady=2)

    accountAdd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="account")
    accountAdd.pack(pady=2)

    accountUser = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="username or email")
    accountUser.pack(pady=2)

    passadd = ctk.CTkEntry(windowEntry.EWindow, placeholder_text="password")
    passadd.pack(pady=2)

    def save():

        saveacc = accountAdd.get()
        savepass = passadd.get()
        saveUser = accountUser.get()

        data_to_save = {
            "account": saveacc,
            "password": savepass,
            "username": saveUser
        }

        json_file_path = "Pass.json"
        save_to_json_file(json_file_path, data_to_save)
        test()

    def save_to_json_file(file_path, new_data):

        try:
            # Try to read existing data from the file
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty, start with an empty dictionary
            existing_data = {"Accounts": []}

        # Append the new data to the existing "Accounts" list
        existing_data["Accounts"].append(new_data)

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

    subBt = ctk.CTkButton(windowEntry.EWindow, text="Submit new account ", command=save)
    subBt.pack(pady=6)

    EditBt = ctk.CTkButton(windowEntry.EWindow, text="Edit an account", command=Edit)
    EditBt.pack(pady=6)

    viewBt = ctk.CTkButton(windowEntry.EWindow, text="View passwords", command=viewPage)
    viewBt.pack(pady=6)

    Quit = ctk.CTkButton(windowEntry.EWindow, text="Close", command=close_wind2)
    Quit.pack(pady=6)

    windowEntry.EWindow.mainloop()


def authenticate():
    stored_master_password = setup_master_password()
    if stored_master_password:
        ask_master_password(stored_master_password)

        check()


def ask_master_password(stored_master_password):
    window1 = windowStart.window1  # Access window1 from windowStart class
    password_entry = ctk.CTkEntry(window1, show="*", font=('Simple bold Jut Out', 15))
    submit_button = ctk.CTkButton(window1, text="Submit", font=('Simple bold Jut Out', 15),
                                  command=lambda: check_master_password(stored_master_password, password_entry.get()))

    password_entry.pack(pady=10)
    submit_button.pack(pady=10)


def check_master_password():
    try:
        with open('master_password.json', 'r') as file:
            data = json.load(file)
            stored_master_password = data.get('master_password', '')

        if stored_master_password == Mentry.get():
            wind2()

            # Continue with the rest of your application
        else:
            messagebox.showerror("Error", "Incorrect master password. Try again.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Windows classes
def check():
    global Mentry
    # Access window1 from windowStart class
    Auth.CWindow = ctk.CTk()
    width = 600  # Width
    height = 400  # Height
    screen_width = Auth.CWindow.winfo_screenwidth()  # Width of the screen
    screen_height = Auth.CWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    Auth.CWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
    Auth.CWindow.title("Check")
    ctk.set_appearance_mode("dark")
    lb1 = ctk.CTkLabel(Auth.CWindow, text="What is your master password?", font=('Simple bold Jut Out', 15))
    lb1.pack()

    Mentry = ctk.CTkEntry(Auth.CWindow)
    Mentry.pack(pady=10)

    bt1 = ctk.CTkButton(Auth.CWindow, text="enter", command=check_master_password)
    bt1.pack()


    bt2 = ctk.CTkButton(Auth.CWindow, text="Close", command=lambda: hide_window(Auth.CWindow))
    bt2.pack(pady=10)

    Auth.CWindow.protocol("WM_DELETE_WINDOW", lambda: hide_window(Auth.CWindow))

    Auth.CWindow.mainloop()


class windowStart:
    window1 = ctk.CTk()

    # setting tkinter window size
    width = 600  # Width
    height = 400  # Heigh
    screen_width = window1.winfo_screenwidth()  # Width of the screen
    screen_height = window1.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window1.geometry('%dx%d+%d+%d' % (width, height, x, y))

    window1.title("MPass")

    lb1 = ctk.CTkLabel(window1, text="What is your master password?", font=('Simple bold Jut Out', 15))
    lb1.pack()

    Mentry = ctk.CTkEntry(window1)
    Mentry.pack(pady=10)

    bt1 = ctk.CTkButton(window1, text="enter", command=wind2)
    bt1.pack()

    bt2 = ctk.CTkButton(window1, text="Close", command=window1.quit)
    bt2.pack(pady=10)


class int_start:
    setup_window = ctk.CTk()


class windowEntry:
    EWindow = ctk.CTk()
    EWindow.title("Entry page")
    # setting tkinter window size
    width = 600  # Width
    height = 400  # Height
    screen_width = EWindow.winfo_screenwidth()  # Width of the screen
    screen_height = EWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    EWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
    ctk.set_appearance_mode("dark")


class Auth:
    CWindow = ctk.CTk()

    # setting tkinter window size
    width = 600  # Width
    height = 400  # Height
    screen_width = CWindow.winfo_screenwidth()  # Width of the screen
    screen_height = CWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    CWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
    CWindow.title("Check")
    ctk.set_appearance_mode("dark")


class view:
    VWindow = ctk.CTk()

    scroll = ctk.CTkScrollableFrame(VWindow, width=600, height=400)
    scroll.place(x=10, y=10)
    VWindow.title("View page")
    # setting tkinter window size
    width = 600  # Width
    height = 400  # Height
    screen_width = VWindow.winfo_screenwidth()  # Width of the screen
    screen_height = VWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    VWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
    ctk.set_appearance_mode("dark")


class edit:
    editWindow = ctk.CTk()
    # setting tkinter window size
    width = 600  # Width
    height = 400  # Heigh
    screen_width = editWindow.winfo_screenwidth()  # Width of the screen
    screen_height = editWindow.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    editWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))
    editWindow.title("Edit page")
    ctk.set_appearance_mode('dark')

def hide_window(window):
    window.withdraw()

def create_image(width, height, color1, color2):
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 10, height // 10, width - width // 10, height - height // 10),
        fill=color2
    )
    return image


def run():
    authenticate()


def quit_app(icon, item):
    icon.stop()
    os._exit(0)

def show_window(icon, item):
    check()

def hide_window(window):
    window.withdraw()

def restore(window):
    window.deiconify()

def on_hotkey():
    Auth.CWindow.deiconify()  # Show the tkinter window upon hotkey trigger

# Register the global hotkey (Ctrl+Alt+A)
def register_hotkey():
    keyboard.add_hotkey('ctrl+alt', on_hotkey)

def second_key():
    keyboard.add_hotkey('ctrl+r', on_hotkey_second)

def on_hotkey_second():
    Auth.CWindow.withdraw()

# Example usage:

def main():
    ##second_key()
    register_hotkey()
    second_key()


    run()

if __name__ == "__main__":
    main()






