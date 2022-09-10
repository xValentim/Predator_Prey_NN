import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
import numpy as np

class Policy:
    def __init__(self, load=False, pos=(0, 0)):
        self.pos = pos
        if not load:
            self.alpha = 0.01
            self.policy = keras.models.Sequential([
                keras.layers.Dense(25, activation="relu", input_shape=[25]),
                keras.layers.Dense(10, activation="relu"),
                keras.layers.Dense(5, activation="softmax"),
            ])
            self.policy.compile(optimizer=Adam(learning_rate=self.alpha))
        else:
            path_best_model = 'Training/my_model_PP_2'
            self.policy = keras.models.load_model(path_best_model)
        
        
    def __call__(self, state):
        pi = self.policy(state)
        return pi
    
def get_obs(array, pos):
    obs = []
    i, j = pos
    for ii in range(-2, 3, 1):
        row = []
        for jj in range(-2, 3, 1):
            row.append(array[(i + ii) % len(array)][(j + jj) % len(array)])
        obs.append(row)     
    return np.array(obs)

def apply_action(array, pos, action, model=None):
    i, j = pos
    if action == 0:
        array[i][j], array[i][(j + 1) % len(array)] = array[i][(j + 1) % len(array)], array[i][j]
        model.pos = (i, (j + 1) % len(array))
    elif action == 1:
        array[i][j], array[i][(j - 1) % len(array)] = array[i][(j - 1) % len(array)], array[i][j]
        model.pos = (i, (j - 1) % len(array))
    elif action == 2:
        array[i][j], array[(i - 1)  % len(array)][j] = array[(i - 1) % len(array)][j], array[i][j]
        model.pos = ((i - 1) % len(array), j)
    elif action == 3:
        array[i][j], array[(i + 1) % len(array)][j] = array[(i + 1) % len(array)][j], array[i][j]
        model.pos = ((i + 1) % len(array), j)
    
