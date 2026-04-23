import PySimpleGUI as sg

layout = [
    [sg.Frame("Name Section", [
        [sg.Text("Enter Name"), sg.Input(key="name")]
    ])],

    [sg.Frame("Age Section", [
        [sg.Text("Enter Age:"), sg.Input(key="age")]
    ])],

    [sg.Button("Submit")]
]

window = sg.Window("Student Form", layout, resizable=True)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Submit":
        print("Name:", values["name"])
        print("Age:", values["age"])

window.close()