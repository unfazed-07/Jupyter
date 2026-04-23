import tkinter as tk
root = tk.Tk()

label = tk.Label(root, text = "Count = 0")

count = 0
def increase():
    global count
    count+=1
    label.confirg(text = f"Count = {count}")
root = tk.Tk()
label = tk.Label(root, text = "Count = 0")
label.pack()
btn = tk.Button(root, text = "Click Me", command=increase)
btn.pack()
root.mainloop()
import PySimpleGUI as sg

layout = [
    [sg.Text("Count = 0", key = "text")]
    [sg.Button("Click Me")]
]
window = sg.Window("Counter", layout, resizable=True)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    if event == "Click Me":
        count+=1
        window['text'].update(f"update{}")

