# login Form

# Frame 1
#Username
# Entry boc to take username

#Frame
# Password
# Entry boc to take password

# Button -> login print -> login success
import tkinter as tk
tk.Label(frame, text = "Usrna,e").pack()
p = tk.Entry(frame, show = "*")
p.pack()

tk.Button(frame, text = "Login", command = lambda: print("Login Success")).pack()
root.mainloop()