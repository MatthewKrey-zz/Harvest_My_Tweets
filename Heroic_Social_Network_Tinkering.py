# import NetworkX library for the creation, manipulation, and study of the structure of complex social networks 
# import unicodecsv package to support stdlib csv module as well as unicode 

import networkx as nx 
import unicodecsv as csv

# reencode Hero Social Network Data to UTF-8  

def reencode(file):
    for line in file:
        yield line.decode('windows-1250').encode('utf-8')
        
filepath = '/Users/matthewkrey/hero-network.csv'
        
csv_reader = csv.reader(reencode(open(filepath)), delimiter=";",quotechar='"')

sourceEncoding = "iso-8859-1"
targetEncoding = "utf-8"
source = open('/Users/matthewkrey/hero-network.csv')
target = open("target", "w")

target.write(unicode(source.read(), sourceEncoding).encode(targetEncoding))

sourceEncoding = 'cp1252'# cp1252 and windows-1250 coding are synonymous 

# There may be some redundant sourceEncoding above. However, I erred on the side of caution. 
# Open to constructive criticism here... 

# Iterate over the dataset to create nodes and edges 

graph = nx.MultiDiGraph(name = "hero-network")
with open(filepath, 'rU') as data:
    reader = csv.reader(data)
    for row in reader:
        graph.add_edge(*row)
    print graph

# Save the function for this iterator to work with this graph for future reference 

def graph_from_csv(filepath):
    graph = nx.MultiDiGraph(name = "hero-network")
    with open(filepath, 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            graph.add_edge(*row)
        return graph

# Test to check social graph size (# of edges), order (# of nodes) and some basic graph info
 
nx.info(graph)

filepath2 = '/Users/matthewkrey/comic-hero-network.gdf'

graph_alternate = nx.Graph(name = "Characters in Comics")
with open(filepath2, 'rU') as data:
    reader = csv.reader(data)
    for row in reader:
        if 'nodedef' in row[0]:
            handler = lambda row,G: G.add_node(row[0], TYPE = row[1])
        elif 'edgedef' in row[0]:
            handler = lambda row,G: G.add_edge(*row)
        else:
            handler(row, graph)
    print graph_alternate

def draw_ego_graph(graph, character, hops = 1):
    
    """
    Expecting a graph_from_gdf
    """
    
    # Get the Ego Graph and Position 
    ego = nx.ego_graph(graph, character, hops)
    pos = nx.spring_layout(ego)
    plt.figure(figsize = (12, 12))
    plt.axis('off')
    
    # Coloration and Configuration
    ego.node[character]["TYPE"] = "center"
    valmap = {"comic": 0.25, "hero": 0.54, "center": 0.87}
    types = nx.get_node_attributes(ego, "TYPE")
    values = [valmap.get(types[node], 0.25) for node in ego.nodes()]
    
    # Draw the graph
    nx.draw_networkx_edges(ego, pos, alpha = 0.4)
    nx.draw_networkx_nodes(ego, pos,
                           node_size = 80,
                           node_color = values,
                           cmap = plt.cm.hot, with_labels = False)
    plt.show()

graph2 = graph_alternate('comic-hero-network.gdf')
draw_ego_graph(graph2, "LONGBOW/AMELIA GREER")