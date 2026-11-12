import tensorflow as tf
import keras
from keras import Sequential
from keras import layers
from keras.activations import relu, tanh
from keras.regularizers import L2

import numpy as np

# Attribution: Claude Sonnet 5.5
class RangeScaling(layers.layerLayer):
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
        keras.Input(shape=(1152,)),   
        layers.Dense(384, activation=relu, name="encode1"),
        layers.Dense(128, activation=relu, name="encode2"),
        layers.Dense(64, name="latent"), #, activity_regularizer=L2(1e-4)),
        layers.Dense(128, activation=relu, name="decode1"),
        layers.Dense(384, activation=relu, name="decode2"),
        layers.Dense(1152, activation=tanh, name="decode3"),
        layers.Reshape((384,3), name="stack"),
        RangeScaling(), # desired arguments set as defaults
        layers.Reshape((1152,))
    ]
)

denseEncoder.compile(optimizer="adam", loss="mse", metrics=["cosine_similarity"])

X_train, X_validation, X_test = groove.asPandas(split=True)

track = X_train["data"].iloc[0]
bars = -(-len(track) // 16)
track = np.pad(track, 16 * bars)
X = np.asarray([track[32*n:32*(n+1)].flatten() for n in range(0,bars-1)])

Sequential.fit(X)
