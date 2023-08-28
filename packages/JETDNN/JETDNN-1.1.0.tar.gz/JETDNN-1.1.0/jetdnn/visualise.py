import tensorflow
from tensorflow import keras
import predict
from keras.utils import plot_model
import matplotlib.pyplot as plt
import numpy as np

# VISUALISE MODELS

def display_model(model):

    """
    display_model

    Display a summary and save a Keras plot of a Deep Neural Network model.

    Args:
        model (Tensorflow Model): Deep Neural Network model build with build_and_test_single.
    
    Returns:
        None
    """
    print(model.summary())
    plot_model(model, to_file='dnn_model_plot.png', show_shapes=True, show_layer_names=True)
    return

# VISUALISE PREDICTIONS

def density_npm_plot(nepeds,delta_nes):

    """
    density_npm_plot

    Plot up to 10 predicted density pedestals using the Neutral Penetration Model (NPM).

    Args:
        nepeds (array): list of predicted density pedestal heights from build_and_test_single.
        delta_nes (array): list of characteristic neutral penetration lengths, from H-mode data.

    Returns:
        None
    """

    C = 2 # set this equal to constant
    x = np.linspace(0,5,100) # set tp cross section width
    for n in range(0,10):
        npm_vals = []
        for i in range(x): # for each x value calculate a bunch of points
            npm = nepeds[n] * np.tanh(C - (x/delta_nes[n]))
            npm_vals.append(npm)
        plt.plot(x,npm_vals)
    return