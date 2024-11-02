from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk
from enum import Enum
import json
import os
from sqlite3 import *

root = Tk()
root.title("SpotifyListener")

label = Label(root, text="Select the data Folder")
label.pack()

class FunctionSelection(Enum):
    artist = ("artist", "master_metadata_album_artist_name")
    song = ("song", "master_metadata_track_name")
    album = ("album", "master_metadata_album_album_name")

def get_enum_key(display_name):
    for option in FunctionSelection:
        if option.value[0] == display_name:
            return option.value[1]

current = tk.StringVar(value=FunctionSelection.artist.value[0])
options = [option.value[0] for option in FunctionSelection]
tk.OptionMenu(root, current, *options).pack()


entry = Entry(root)
entry.pack()


def load_file():
    entry_text = entry.get()
    counter = 0
    selected_option = get_enum_key(current.get())
    directory_name = fd.askdirectory()

    for filename  in os.listdir(directory_name):
        if filename.endswith(".json") and filename.startswith("Streaming_History_Audio"):
            with open (directory_name + "/" + filename, 'r', encoding="utf8") as file:
                song_directory_list = json.load(file)
                for song_instance in song_directory_list:
                    if song_instance.get(selected_option) == entry_text:
                        counter = counter + 1
    print(counter)




open_button = ttk.Button(
    root,
    text="File",
    command=load_file
)

open_button.pack()
name = entry.get()
root.mainloop()