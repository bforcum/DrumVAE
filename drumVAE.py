import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path 
import urllib.request
import zipfile

from mido import MidiFile


groove_path = Path("data/groove/")

if not groove_path.is_dir():
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

df = pd.read_csv("data/groove/info.csv", usecols=["midi_filename", "split"])


