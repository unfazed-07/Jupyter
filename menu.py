import tkinter as tk

root = tk.Tk()
root.title("Menu Example")


def open_file():
    print("File Opened")

def show_about():
    messagebox.showinfo("About", "This is a simple GUI app")
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff = 0)

file_menu = tk.