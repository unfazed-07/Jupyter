import tkinter as tk
# root = tk.Tk()


# root.title("My First App")

# def  SayHello():
#     print("Hello Students")
# root = tk.Tk()
# btn = tk.Button(root, text = "Click Me😵‍💫", command = SayHello)
# btn2 = tk.Button(root, text = "Click Me 🥹", command = SayHello)
# btn.pack()

# root.mainloop()
def greet():
    name = entry.get()
    print("Hello:", name)

root = tk.Tk()
entry = tk.Entry(root)
entry.pack()
# btn = tk.Button(root, text = 'Greet', greet)


entry.mainloop()