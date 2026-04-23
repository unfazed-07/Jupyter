import pysimpleGUI as sg

layout = [
    sg.Frame("Login"), [
        [sg.Text("Username"), sg.Input(key = 'user')],
        [sg.Text("Password"), sg.Input(password_char="*", key = "pass")]
    ],
    [sg.Button("Login")],
    [sg.Text(" ", key = "out")]

]