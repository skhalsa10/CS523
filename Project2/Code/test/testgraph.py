import matplotlib.pyplot as plt 
import networkx as nx
import scipy
from deadhistory import *

to_graph = [('uuauuucaacaaaau', 'LFQQN'), ('uuuuuucaacaaaau', 'FFQQN'), ('uuuuuucaacaaacu', 'FFQQT'), ('uuuuuucaucaaacu', 'FFHQT'), ('uuuguucaucaaacu', 'FVHQT'), ('uuuguucaucacacu', 'FVHHT'), ('uuuguucaucacacg', 'FVHHT'), ('uuuguucauuacacg', 'FVHYT'), ('uuucuucauuacacg', 'FLHYT'), ('uaucuucauuacacg', 'YLHYT'), ('uaccuucauuacacg', 'YLHYT'), ('uaccuacauuacacg', 'YLHYT'), ('uaccuacauuauacg', 'YLHYT'), ('uaccuaaauuauacg', 'YLNYT')]

unique_nodes = {x[1] for x in to_graph}
dead_nodes = set()
for x in dead_history:
    dead_nodes.update(x[1])
# edges = [(to_graph[i][1],to_graph[i+1][1],{'color': 'red'}) for i in range(len(to_graph)-1) ]
edges = [(to_graph[i][1],to_graph[i+1][1]) for i in range(len(to_graph)-1) ]
dead_edges = []
for x in dead_history:
    dead_edges.extend([(x[i][1],x[i+1][1]) for i in range(len(x)-1) ])


g = nx.Graph()
g.add_nodes_from(dead_nodes)
g.add_nodes_from(unique_nodes)
g.add_edges_from(dead_edges)
g.add_edges_from(edges)

options = {'node_color': 'green','node_size': 40,'width': 1, }
options2 = {'node_color': 'black','node_size': 50,'width': 1,}


nx.draw_planar(g, **options)
# nx.draw(g2, **options2)

# G = nx.petersen_graph()
# plt.subplot(121)

# nx.draw(G, with_labels=True, font_weight='bold')
# plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
plt.show()
