import epynet
import numpy as np
import networkx as nx
from epynet import Network
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
from graph_utils import get_nx_graph

wds = epynet.Network('L-TOWN_v2_Real.inp')
wds.solve()

G = get_nx_graph(wds, mode='weighted')
A = np.array(nx.adjacency_matrix(G).toarray())
# D   = np.diag(np.sum(A, axis=0)**-.5)

D = np.sum(A, axis=0)
D[D != 0] = D[D != 0] ** -.5
D = np.diag(D)

I = np.eye(np.shape(A)[0])
L = I - np.dot(np.dot(D, A), D)
lambda_max = np.linalg.eigvalsh(L).max()
L_tilde = 2. * L / lambda_max - I

# Sanity check with PyG utils
# pyg_graph   = pyg.utils.from_networkx(G)
# L   = pyg.utils.get_laplacian(
#    pyg_graph.edge_index,
#    edge_weight     = pyg_graph.weight,
#    normalization   = 'sym'
#    )
# L   = pyg.utils.to_dense_adj(L[0], edge_attr=L[1]).squeeze(0).numpy()
# lambda_max  = np.linalg.eigvalsh(L).max()
# L_tilde = 2.*L/lambda_max-I

print('Conditional number of the Laplacian is {:f}.'.format(np.linalg.cond(L_tilde, 2)))
# print('Conditional number of the square of the Laplacian is {:f}.'.format(np.linalg.cond(np.power(L_tilde, 2), 2)))
# print('Conditional number of the cube of the Laplacian is {:f}.'.format(np.linalg.cond(np.power(L_tilde, 3), 2)))

# Coloring only nonzero elements
L_star = np.abs(L_tilde.copy())
vmin = L_star[L_star.nonzero()].min()
vmax = L_star.max()
L_star[L_star == 0] = np.nan

sns.set(font_scale=1.75, style='whitegrid')
figsize = (8, 6)
axlabel = "Node number"
barlabel = "Value of the Laplacian"
fig, ax = plt.subplots(figsize=figsize)
hmap = sns.heatmap(L_star,
                   norm=LogNorm(vmin=vmin, vmax=vmax),
                   cmap='viridis',
                   # linewidth   = .1,
                   # linecolor   = 'k',
                   cbar_kws={'label': barlabel},
                   square=True,
                   ax=ax
                   )
hmap.set_xlabel(axlabel)
hmap.set_ylabel(axlabel)

plt.show()
# ----- ----- ----- ----- ----- -----
# Diagram export
# ----- ----- ----- ----- ----- -----

fmt = 'pdf'
fname = 'laplace-' + 'l-town' + '-' + 'weighted' + '.' + fmt
fig.savefig(fname, format=fmt, bbox_inches='tight')
