import PySimpleGUI as sg

menu_layout = [
    ['File', ['Open', 'Exit']],
    ['Help', ['About']]
]

layout = [
    [sg.Menu(menu_layout)]
]

window = sg.Window("Menu App", layout, resizable=True)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    if event == "Open":
        print("File Opened")

    if event == "About":
        sg.popup("This is a simple GUI App.")

window.close()