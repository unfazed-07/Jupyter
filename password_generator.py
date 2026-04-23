import PySimpleGUI as sg
layout = [[sg.Input(password_char='*', key='pass')],
[sg.Button("Check")],
[sg.Text("", key='out')]]
window = sg.Window("Login", layout, resizable=True)
while True:
    e, v = window.read()
    if e == sg.WINDOW_CLOSED: 
        break
    if e == "Check":
        if v['pass'] == "admin123":
            window['out'].update("Access Granted")
        else:
            window['out'].update("Access Denied")
        window.close()