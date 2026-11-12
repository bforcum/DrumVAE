import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Layer, Dense, Reshape
from tensorflow.keras.activations import relu, tanh
from tensorflow.keras.regularizers import L2

import numpy as np

# Attribution: Claude Sonnet 5.5
class RangeScaling(Layer):
    def __init__(self, lows=(0.0, 0.0, -0.5), highs=(1.0, 1.0, 0.5), **kwargs):
        super().__init__(**kwargs)
        # Minima of desired scaling intervals across last dimension of input
        self.lows = tf.constant(lows, dtype=tf.float32)
        # Maxima of scaling intervals
        self.highs = tf.constant(highs, dtype=tf.float32)

    def call(self, x):
        # Scale by ranges of each and add lows (minimums)
        return self.lows + (self.highs - self.lows) * tf.sigmoid(x)

    def get_config(self):
        cfg = super().get_config()
        cfg.update({"lows": self.lows.numpy().tolist(),
                    "highs": self.highs.numpy().tolist()})
        return cfg
# End attribution

import groove

denseEncoder = Sequential(
    [
        
        Dense(384, activation=relu, name="encode1"),
        Dense(128, activation=relu, name="encode2"),
        Dense(64, name="latent"), #, activity_regularizer=L2(1e-4)),
        Dense(128, activation=relu, name="decode1"),
        Dense(384, activation=relu, name="decode2"),
        Dense(1152, activation=tanh, name="decode3"),
        Reshape((384,3), name="stack"),
        RangeScaling(), # desired arguments set as defaults
        Reshape((1152,))
    ]
)

df = groove.asPandas()
track = df["data"].iloc[0]
X = np.asarray([track[32*n:32*(n+1)].flatten() for n in range(0,4)])

print(denseEncoder(X))