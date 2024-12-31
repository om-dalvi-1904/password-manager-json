from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
import os
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    ##password is assumed to be in list
    password_letter = [choice(letters) for i in range(randint(8,10))]
    password_number = [choice(numbers) for i in range(randint(2,4))]
    password_symbol = [choice(symbols) for i in range(randint(2,4))]
    password_list = password_letter + password_symbol + password_number
    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_text.insert(0, string=password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    website = website_text.get()
    email = email_text.get()
    password = password_text.get()
    data_dict = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="All the fields are compulsory.")
    else:
        try:
            with open("password.json", "r") as data_file:
                data = json.load(data_file) #or use pass keyword
        except FileNotFoundError:
            with open("password.json", "w") as data_file:
                json.dump(data_dict, data_file, indent=4)
        else:
            data.update(data_dict)
            with open("password.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_text.delete(0, END)
            email_text.delete(0, END)
            password_text.delete(0, END)
            website_text.focus()

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    try:
        with open("password.json", "r") as file:
             content = json.load(file)
             global website
             website = website_text.get()
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        for item in content:
            if item == website:
                messagebox.showinfo(title=website, message=f"Email: {content[item]['email']}\nPassword: {content[item]['password']}")
                break
            else:
                messagebox.showinfo(title="Error", message=f"No details found for the {website} saved.")
                break

#you can also define the find password function as

# def find_password():
#     website = website_text.get()
#     with open("password.json", "r") as file_data:
#         data = json.load(file_data)
#         if website in data:
#             email = data[website]["email"]
#             password = data[website]["password"]
#             messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")

# ---------------------------- UI SETUP ------------------------------- #
if os.environ.get("DISPLAY", "") == "":
    print("No display found. Running in non-GUI mode.")
else:
    window = Tk()
    window.title("Password Manager")
    window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

#labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)


#Entries
website_text = Entry(width=21)
website_text.focus()
website_text.grid(column=1, row=1)

email_text = Entry(width=40)
email_text.grid(column=1, row=2, columnspan=2)

password_text = Entry(width=21)
password_text.grid(column=1, row=3)


#Buttons
password_button = Button(text="Generate Password", command=generate_password, width=15)
password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=35, command=add)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", command=find_password, width=15)
search_button.grid(column=2, row=1)

window.mainloop()