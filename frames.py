import tkinter as tk
root = tk.Tk()

f1 = tk.Frame(root)
f2 = tk.Frame(root)

tk.Label(f1, text = "Name").pack()
name = tk.Entry(f1)
name.pack()

tk.Label(f2, text = "Age").pack()
age = tk.Entry(f2)

f1.pack()
f2.pack()

tk.Button(root, text = "Submit", command = lambda: print(name.get, age.get())).pack()


root.mainloop()