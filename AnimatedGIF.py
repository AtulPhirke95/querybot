from tkinter import *
root = Tk()

def update(x):
    img = PhotoImage(file='loader.gif',format='gif -index '+str(x))
    x += 1
    if x > 20: x = 0
    label.configure(image=img)
    label.img=img
    root.after(100, update, x)

label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()
