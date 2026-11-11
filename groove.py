import numpy as np
import pandas as pd

from pathlib import Path 
import urllib.request
import zipfile

from mido import MidiFile

from constants import *

download_dir = Path(download_path)
groove_dir = Path(groove_path)

def fetch(force_download=False, verbosity=0):
    if force_download or not (groove_dir/"info.csv").is_file():
        _download(verbosity)
        _extract(verbosity)
        _process_and_save(verbosity)

# Downloads and runs all subsequent steps
def _download(verbosity=0):
    if (verbosity > 0): print("Downloading...", end='', flush=True)
    # Pass data_dir directly into the load function
    urllib.request.urlretrieve(groove_url, download_path + 'groove.zip')
    if (verbosity > 0): print("\rDownloaded        ")

def _extract(verbosity=0):
    if (verbosity > 0): print("Extracting...", end='', flush=True)
    try:
        zipfile.ZipFile(download_path + 'groove.zip', 'r').extractall(groove_path + '../')
    except:
        # Zip archive contains a reference to an incorrectly formatted path and always throws an error
            pass
    if (verbosity > 0): print("\rExtracted        ")

def _process_and_save(verbosity = 0):
    if verbosity == 1:
        print("Parsing...", end='', flush=True)
    recordings_paths = _getTable()

    for i, fileName in enumerate(recordings_paths["midi_filename"]):
        if verbosity > 1 and i % 100 == 0:
            print(f"\r{i:04} tracks parsed", end='')
        
        mid = MidiFile(groove_path + fileName)

        # Divide each beat (4th) by 4 = 2^2 for 16ths
        ticks_per_16th = mid.ticks_per_beat >> 2
        half_16th = ticks_per_16th >> 0
        inv_ticks_per_16th = 1.0 / ticks_per_16th

        notes = []

        ticks = 0

        for msg in mid.tracks[0]:
            ticks += msg.time 
            if msg.type == 'note_on' and msg.velocity > 0:
                hitTime = (ticks + half_16th) // ticks_per_16th
                microTime = (ticks - (hitTime * ticks_per_16th)) * inv_ticks_per_16th
                
                notes.append(((hitTime, noteMap[msg.note]), [1, msg.velocity/128, microTime]))
        num_16ths = -(-(ticks+half_16th) // ticks_per_16th)
        grid = np.zeros((num_16ths, len(instrumentMap), 3))
        for note in notes:
            grid[note[0]] = note[1]
        # Save in same directory with new extension
        np.save(groove_path + fileName[:-4], grid)
    if verbosity > 0:
        print(f"\r{len(recordings_paths)} tracks parsed")

def _getTable():
    recordings_info = pd.read_csv(groove_path + "info.csv", usecols=["id", "bpm", "split", "midi_filename", "time_signature"])
    recordings_paths = recordings_info[recordings_info["time_signature"] == "4-4"]
    recordings_paths = recordings_paths.drop(columns="time_signature")
    return recordings_paths

def asPandas(preSplit = True):
    fetch()
    df = _getTable()
    data = []
    for filename in df["midi_filename"]:
        data.append(np.load(groove_dir / (filename[:-4] + ".npy")))
    df["data"] = data
    df = df.drop(columns="midi_filename")
    if not preSplit:
        return df
    train_set = df[df["split"] == "train"]
    val_set = df[df["split"] == "validation"]
    test_set = df[df["split"] == "test"]

    return (train_set, val_set, test_set)
    

if __name__ == "__main__":
    fetch(force_download=True, verbosity=1)

