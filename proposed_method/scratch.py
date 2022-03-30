import yaml
import os
import argparse
import epynet
import torch
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch_geometric.utils import from_networkx
from sklearn.model_selection import train_test_split


# Custom modules
from epanet_loader import get_nx_graph
from visualisation import visualise
from epanet_simulator import epanetSimulator
from data_loader import battledimLoader, dataCleaner, dataGenerator
from early_stopping import EarlyStopping
from metrics import Metrics

# Import the .inp file using the EPYNET library
wdn = epynet.Network('C:/Users/aznur/PycharmProjects/LargeScale-DLM/L-TOWN_v2_Real.inp')

# Solve hydraulic model for a single timestep
wdn.solve()

G, pos, head = get_nx_graph(wdn, weight_mode='inv_pipe_length', get_head=True)

print('Importing dataset configuration...\n')

# Open the dataset configuration file
with open('C:/Users/aznur/PycharmProjects/LargeScale-DLM/data/dataset_configuration.yaml') as file:

    # Load the configuration to a dictionary
    config = yaml.load(file, Loader=yaml.FullLoader)

# Generate a list of integers, indicating the number of the node
# at which a  pressure sensor is present
sensors = [int(string.replace("n", "")) for string in config['pressure_sensors']]

colormap = pd.Series([1.0 if i in sensors else 0.0 for i in range(1,G.number_of_nodes()+1)])

# Generate a colormap
cmap = plt.get_cmap('coolwarm')

# Fit the datapoints to the colormap
color = cmap(colormap)

# Visualise the the model using our visualisation utility
axis = visualise(G, pos=pos, color = color, figsize = (60,32), edge_labels=True)

plt.show()