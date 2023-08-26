"""
INSPECT DATA
"""

import seaborn as sns
from .predict_ped import multi_ped

"""
Functions for plotting and inspecting data. E.g. seaborn pairplot, and if inputs have a certain correlation with the output, the program suggests using them for the DNN.
"""

def plot_params():

    sns.pairplot(train_data[["ne_ped_height_pre-ELM__10^19(m^-3)","Ip_(MA)","P_tot_(MW)","gas_flow_rate_of_main_species_10^22__(e/s)","B_(T)","triangularity"]],diag_kind = "kde")

    return
