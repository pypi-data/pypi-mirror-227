# JET DNN

JETDNN: Python package using Deep Neural Networks (DNNs) to find H-mode plasma pedestal heights from multiple engineering parameters in H-mode JET data.
Created by S. Frankel, J. Simpson and E. Solano.

[![DOI](https://zenodo.org/badge/682657741.svg)](https://zenodo.org/badge/latestdoi/682657741)

Installation
------------------

To use JETDNN, install it in the console using pip:
    
`$ pip install jetdnn`

or

`$ pip install JETDNN`

Requirements
------------------

The packages required to run JETDNN can be found on GitHub here: https://github.com/quasoph/jetdnn/blob/main/requirements.txt.

Functions
------------------

`jetdnn.predict_ped.single_ped()`

Predict a list of pedestal heights for a single type of pedestal, and calculate the mean squared error of these predictions.

### Arguments:

`csv_name` (string): filename of csv.

`input_cols` (list): list of column names (as strings) of engineering parameters to predict from.

`output_col` (string): name of column you'd like to predict.

`plot_col` (string): optional. Name of column you'd like to plot your predictions against, selected from the engineering parameters.

`learning_rate` (integer): optional. Value from 0.1 - 0.0001 representing the learning rate of the Keras Adam optimizer.
    Documentation for the Adam optimizer can be found here: https://keras.io/api/optimizers/adam/.

`epochs` (integer): optional. Number of epochs for training the DNN. Typical starting values may be 50 for a smaller dataset up to 500 for a large dataset.
    If not given, the function will use a default value of 50.

`batch_size` (integer): optional. Batch size for training the DNN, either 8, 16, 32 or 64. Smaller batch sizes may give more accurate predictions but take more time.
    If not given, the function will use a default value of 8.

`maxoutput` (Boolean): optional. Set equal to True to display a more detailed output, useful for debugging.

Returns:

    array: pedestal height predictions
    
    integer: mean squared error of these predictions.
