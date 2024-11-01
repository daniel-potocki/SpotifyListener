from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import json
import os
from sqlite3 import *

root = Tk()
root.title("SpotifyListener")
label = Label(root, text="Select the data Folder")
entry = Entry(root)

def load_file():
    counter = 0
    directory_name = fd.askdirectory()
    for filename  in os.listdir(directory_name):
        if filename.endswith(".json") and filename.startswith("Streaming_History_Audio"):
            with open (directory_name + "/" + filename, 'r', encoding="utf8") as file:
                song_directory_list = json.load(file)
                for song_instance in song_directory_list:
                    if song_instance["master_metadata_album_artist_name"] == "Travis Scott":
                        counter = counter + 1
                        print(counter)
                        print(song_instance["master_metadata_album_artist_name"])

open_button = ttk.Button(
    root,
    text="File",
    command= load_file
)

label.pack()
open_button.pack()
entry.pack()
name = entry.get()
root.mainloop()