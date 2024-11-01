from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

root = Tk()
root.title("SpotifyListener")
label = Label(root, text="Select the data Folder")
entry = Entry(root, fg="green", bg="blue")

def select_file():
    filename = fd.askopenfilename()
open_button = ttk.Button(
    root,
    text="File",
    command= select_file
)

label.pack()
open_button.pack()
entry.pack()
name = entry.get()
root.mainloop()
