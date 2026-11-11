import numpy as np
import pandas as pd

import time
import groove

start = time.time()
groove.fetch(force_download=True)
end = time.time()

print(f"It took {end - start:.3f} seconds to parse all MIDI files")

