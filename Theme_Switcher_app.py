#Theme Swither App
# Features:
# Theme Menu
# Menu --> Light/Dark
# Change background color, text, color

import tkinter as tk

root = tk.Tk()
root.title("Theme App")

label = tk.Label(root, text = "Theme Exmaple")
label.pack()

menu2 = tk.Menu(root)

theme_menu = tk.Menu(menu2, tearoff=0)
theme_menu = add_command(label = "Light", command = light_theme)