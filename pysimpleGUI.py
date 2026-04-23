import PySimpleGUI as sg

layout = [
    [sg.Text("Enter Name")],
    [sg.Input(key = 'name')],
    [sg.Button("Greet")]
]

window = sg.Window("App", layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Greet":

        print("Hello", values['name'])

window.close()
