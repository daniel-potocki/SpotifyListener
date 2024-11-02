from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk
from enum import Enum
import json
import os
import sqlite3

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

def get_folder_path():
   print(fd.askdirectory())
   folder_path = fd.askdirectory()


def load_files_into_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spotifyData (
            artist_name TEXT NOT NULL,
            track_name TEXT NOT NULL,
            album_name TEXT NOT NULL,
            ms_listened INTEGER NOT NULL
        )
    ''')
    conn.commit()

    directory_name = fd.askdirectory()
    song_count = 0

    for filename in os.listdir(directory_name):
        if filename.endswith(".json") and filename.startswith("Streaming_History_Audio"):
            file_path = os.path.join(directory_name, filename)
            with open(file_path, 'r', encoding="utf8") as file:
                song_directory_list = json.load(file)

                for song_instance in song_directory_list:
                    if all(key in song_instance and song_instance[key]
                           for key in [
                               "master_metadata_track_name",
                               "master_metadata_album_artist_name",
                               "master_metadata_album_album_name",
                               "ms_played"]):

                        cursor.execute('''
                            INSERT INTO spotifyData (artist_name, track_name, album_name, ms_listened)
                            VALUES (:artist_name, :track_name, :album_name, :ms_listened)
                        ''', {
                            'artist_name': song_instance["master_metadata_album_artist_name"],
                            'track_name': song_instance["master_metadata_track_name"],
                            'album_name': song_instance["master_metadata_album_album_name"],
                            'ms_listened': song_instance["ms_played"]
                        })
                        song_count += 1
                    else:
                        print(f"Ein Eintrag in {filename} wurde übersprungen, da er unvollständig oder leer ist.")

    conn.commit()
    conn.close()

    print(f"{song_count} Songs erfolgreich in die Datenbank eingefügt.")


transfer_to_db_button = ttk.Button(
    root,
    text="transfer to db",
    command=load_files_into_db
)

open_button = ttk.Button(
    root,
    text="File",
    command=load_file
)

transfer_to_db_button.pack()
open_button.pack()
name = entry.get()
root.mainloop()