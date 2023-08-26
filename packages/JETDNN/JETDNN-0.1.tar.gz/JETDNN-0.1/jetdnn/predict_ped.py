import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

def single_ped(csv_name,input_cols,output_col,plot_col=None,learning_rate=None,epochs=None,batch_size=None,maxoutput=None): # arguments set to None are optional

    """
    REQUIRED ARGUMENTS:
    csv_name (string): filename of csv
    input_cols (list): list of column names (as strings) of engineering parameters to predict from
    output_col (string): name of column you'd like to predict
    
    OPTIONAL ARGUMENTS:
    plot_col (string): name of column you'd like to plot your predictions against, ideally from the engineering parameters
    learning_rate (integer): value from 0.1 - 0.0001 representing the learning rate of the Keras Adam optimizer (documentation here: _____)
    epochs (integer): number of epochs for training the DNN
    batch_size (integer): batch size for training the DNN
    maxoutput (Boolean): set True to display a more detailed output, useful for debugging
    
    FUTURE IDEAS:
    - create input for a separate test csv so training and testing data can be two separate files
    - automatically convert arguments to their required dtype at the start of this function
    - create warnings for incorrect dtypes etc

    Returns pedestal predictions as a list for a single pedestal, and the mean squared error of these predictions.
    """

    # DATA CLEANING

    data = pd.read_csv(os.path.abspath(csv_name),index_col=False,sep="\s{3,}|\s{3,}|\t+|\s{3,}\t+|\t+\s{3,}",skipinitialspace=True) # maybe change separator depending on testing
    if maxoutput == True:
        print(data.columns) # column names
        print(data.iloc[:,0]) # first column
        print(data.iloc[:,1]) # second column

    
    """
    SPLIT TRAIN AND TEST DATA
    """

    train_data, test_data = np.split(data.sample(frac=1,random_state=42),[int(.8*len(data))]) # this works!
    if maxoutput == True:
        print("Train and test data are of type " + str(type(train_data)))
        print("Train data size is " + str(train_data.size))
        print("Test data size is " + str(test_data.size))
    
    """
    GET INPUTS AND OUTPUTS
    """

    traininput = train_data[input_cols] # this is the correct format, list of a list, or [["x","y"]]
    trainoutput = train_data[output_col]

    testinput = test_data[input_cols]
    testoutput = test_data[output_col]

    """
    NORMALISATION LAYER
    """
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(np.array(traininput)) # adapting traininput means the DNN will accept however many input columns are given

    """
    MODEL BUILDING
    """

    def build_and_compile_model(norm,learnrate=None):
        model = keras.Sequential([
            norm,
            layers.Dense(128,activation="relu"),
            layers.Dropout(0.2), # could experiment with removing dropout layers, e.g. a separate function
            layers.Dense(128,activation="relu"),
            layers.Dropout(0.2),
            layers.Dense(1)
        ])
        if learnrate==None:
            model.compile(loss="mean_absolute_error",optimizer=tf.keras.optimizers.Adam(0.0005))
        else:
            model.compile(loss="mean_absolute_error",optimizer=tf.keras.optimizers.Adam(learnrate)) # this part may be finicky
        return model

    dnn_model = build_and_compile_model(normalizer,learning_rate)
    dnn_model.summary()

    """
    TRAINING
    """
    if epochs == None and batch_size == None:
        history = dnn_model.fit(x=traininput,y=trainoutput,validation_data=(testinput,testoutput),verbose=0,epochs=50,batch_size=8)
    elif epochs != None and batch_size == None:
        history = dnn_model.fit(x=traininput,y=trainoutput,validation_data=(testinput,testoutput),verbose=0,epochs=epochs,batch_size=8)
    elif epochs == None and batch_size != None:
        history = dnn_model.fit(x=traininput,y=trainoutput,validation_data=(testinput,testoutput),verbose=0,epochs=50,batch_size=batch_size)
    else:
        history = dnn_model.fit(x=traininput,y=trainoutput,validation_data=(testinput,testoutput),verbose=0,epochs=epochs,batch_size=batch_size) # options given if optional arguments are input


    """
    PREDICTION
    """
    predicted_ped = dnn_model.predict(testinput)

    """
    COMPILING
    The loss finds the mean error, then the optimizer aims to minimise this by changing the weights.
    """
    dnn_model.summary()

    def plot_loss(history):
        plt.plot(history.history["loss"], label="loss")
        plt.plot(history.history["val_loss"], label="val_loss")
        plt.ylim([0,5])
        plt.xlabel("Epoch")
        plt.ylabel(r"Error [pedestal height units]") # get this to obtain units from dataset
        plt.legend()
        plt.grid(True)

    plot_loss(history)
    plt.show()

    """
    RESHAPE DATA FOR PLOTTING
    """

    if maxoutput == True:
        print(np.shape(predicted_ped))

    flat_ped = []
    for sublist in predicted_ped.tolist():
        for item in sublist:
            flat_ped.append(item)
    
    if maxoutput == True:
        print(len(flat_ped))
        print(len(testinput))

    """
    PLOTTING

    Plots predicted and true pedestal heights against a chosen column from the input values.
    """

    x = np.array(testinput[plot_col])
    plt.plot(x,flat_ped,".",label="Predicted values")
    plt.plot(x,testoutput,".",label="True values")
    plt.xlabel(plot_col)
    plt.ylabel(output_col)
    plt.legend()
    plt.show()

    """
    PLOT ACCURACY
    """

    x = np.linspace(min(np.array(testoutput)),max(np.array(testoutput)),100)
    y = x
    plt.plot(testoutput,flat_ped,".",label = "Data points")
    plt.plot(x,y,label="y = x")
    plt.title("Accuracy")
    plt.xlabel(r"True values [$m^{-3}$]")
    plt.ylabel(r"Predicted values [$m^{-3}$]")
    plt.legend()
    plt.show()

    """
    EVALUATE ACCURACY
    """

    errs = []

    for n in range(0,len(flat_ped)):
        err = (flat_ped[n] - np.array(testoutput)[n])**2
        errs.append(err)

    m_s_e = sum(errs) / len(errs)
    print(m_s_e)

    return flat_ped, m_s_e

def multi_ped():
    """
    Function to predict multiple different pedestals from multiple inputs. May be less accurate as hyperparameters must be the
    same for all outputs, however less time consuming if you want to predict multiple types of pedestal.
    WIP.
    """

    return