'''
import networkx as nx
import matplotlib.pyplot as plt
G= nx.read_edgelist('facebook_combined.txt')
print(nx.info(G))
'''





'''
import networkx as nx
import pandas as pd

def _get_graph_file():
   G = nx.DiGraph()
   git = pd.read_csv('file.csv', skiprows=[1])
   G.add_weighted_edges_from(git.values)
   return G

print(_get_graph_file())
'''




import networkx as nx
import csv
import matplotlib.pyplot as plt
import pandas as pd

def _get_graph_file():
   G = nx.DiGraph()

   #Read the csv file
   file_obj = open('C:/Users/Harsh/Documents/Python Scripts/One.csv')
   git = pd.read_csv(file_obj,skiprows=[1])
   G.add_weighted_edges_from(git.values)
   return G

my_graph = _get_graph_file()
nx.draw(my_graph)
#print(_get_graph_file())
#print(my_graph.nodes())
#print(my_graph.edges())
#print(my_graph['kts']['blocklist-ipsets'])






