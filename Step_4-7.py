""" Step 4 """
import json
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=np.inf)  

""" Open articles.json """
with open("articles.json") as f:
    data = json.load(f)

"""Extract values of articles"""
id = []  ## Get id of article
ref = []  ## Get references of article
title = [] ## Get title of article
for i, j in data.items():
    if 'refs' in j:
        id.append(i)
        title.append(j['title'])
        ref.append(j['refs'])

"""Fulfill an adjaceny matrix to draw the graph"""
adj_mtx = np.zeros((len(id),len(id))) ## Set a adjaceny matrix for drawing graph
for row in range(len(id)): ## Match all edges
    for n in ref[row]: 
        line = 0
        for x in id:
            if n == x:
                adj_mtx[row][line] = 1
            line = line + 1

"""Draw graph"""
G = nx.DiGraph()
n = 1
for i in title: ## Add nodes in initialled graph, n is id of node, title is the attribute of a node
    G.add_node(n,title = i)
    n = n + 1
G = nx.from_numpy_matrix(adj_mtx, create_using = G)
#nx.draw(G)

"""Calculate page rank of each papper and store them into their attributes"""
nx.set_node_attributes(G, nx.pagerank(G), 'Page Rank')

"""Set params of histogram ranking authorities"""
ranked_hubs = sorted(nx.hits_numpy(G)[0].items(), key = lambda d:d[1], reverse = True)  ## Sort pappers according to their hub values
hubs_x = []
hubs_y = []
for i in ranked_hubs:
    hubs_x.append(i[0])
    hubs_y.append(i[1])

"""Set params of histogram ranking authorities"""
ranked_auths = sorted(nx.hits_numpy(G)[1].items(), key = lambda d:d[1], reverse = True)  ## Sort pappers according to their auth values
auths_x = []
auths_y = []
for i in ranked_auths:
    auths_x.append(i[0])
    auths_y.append(i[1])

"""Draw histograms"""
plt.subplot(121)
plt.bar(range(len(hubs_x)), hubs_y, 1, color='g')
plt.xticks(range(len(hubs_x)), hubs_x)
plt.subplot(122)
plt.bar(range(len(auths_x)), auths_y, 1, color='r')
plt.xticks(range(len(auths_x)), auths_x)
plt.show()
