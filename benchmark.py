import numpy as np
import pandas as pd

from pathlib import Path 
import urllib.request
import zipfile

from mido import MidiFile
import time

# Open data
groove_path = "data/groove/"

if not Path(groove_path).is_dir():
    try:
        print("Directory doesn't exist")
        # Create data directory and child downloads directory
        Path("data/downloads/").mkdir(parents=True, exist_ok=True)
        groove_url = "https://storage.googleapis.com/magentadata/datasets/groove/groove-v1.0.0-midionly.zip"
        # Pass data_dir directly into the load function
        urllib.request.urlretrieve(groove_url, "data/downloads/groove.zip")

        zipfile.ZipFile('data/downloads/groove.zip', 'r').extractall('data/')
    except:
        # Zip archive contains a reference to an incorrectly
        # formatted path and always throws an error
        pass



df_raw = pd.read_csv("data/groove/info.csv", usecols=["midi_filename", "time_signature", "split"])
df = df_raw[df_raw["time_signature"] == "4-4"]
df.drop(columns="time_signature")
df["midi_filename"] = groove_path + df["midi_filename"]


# Parse data
mid = MidiFile(df["midi_filename"][0])

total = 0

start = time.time()
for name in df["midi_filename"]:
    mid = MidiFile(name)
    n = len(mid.tracks)
    assert(n == 1)
    total += n

end = time.time()

print(f"It took {end - start:.3f} seconds to parse all {total} MIDI files")

