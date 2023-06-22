import networkx as nx
from pyvis.network import Network
from networkx.algorithms import bipartite
import sys

loadpath = sys.argv[1]+sys.argv[2]+"_result/qcResult/"
# loadpath = "C:/Users/kwz50/IdeaProjects/PowerBarcoder/data/result/202306181609/"

# Create a new graph
G = nx.DiGraph()

# Add layers as nodes
G.add_node("Input Layer")
G.add_node("Hidden Layer 1")
G.add_node("Hidden Layer 2")
G.add_node("Output Layer")

# Add edges between layers
G.add_edge("Input Layer", "Hidden Layer 1")
G.add_edge("Hidden Layer 1", "Hidden Layer 2")
G.add_edge("Hidden Layer 2", "Output Layer")

# Initialize a Pyvis network
nt = Network(directed=True)

# Add nodes and edges to the network
for node in G.nodes:
    nt.add_node(node, title=node)

for edge in G.edges:
    src, tgt = edge
    nt.add_edge(src, tgt)

# Set network visualization options
nt.barnes_hut(overlap=0.2)

# Generate an HTML file with the visualization
nt.save_graph(loadpath+"hidden_layers.html")




B = nx.Graph()
B.add_nodes_from(['A', 'B', 'C', 'D', 'E'], bipartite=0)
B.add_nodes_from([1, 2, 3, 4], bipartite=1)
B.add_edges_from([('A', 1), ('B', 1), ('C', 1), ('C', 3), ('D', 4), ('E', 1), ('A', 2), ('E', 2)])

# Create a Pyvis network
nt2 = Network(height="500px", width="100%", notebook=False)

# Add nodes and edges to the network
for node in B.nodes:
    nt2.add_node(node,x=100,y=100)

for edge in B.edges:
    src, tgt = edge
    nt2.add_edge(src, tgt)

# Generate an HTML file with the visualization
nt2.save_graph(loadpath+"bipartite_graph.html")