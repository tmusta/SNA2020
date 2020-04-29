import json
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

def most_collabs(data):
    keylist = list(data.keys())
    d = {"author": "name", "publications": 0, "colabs": 0}

    authorsList = []
    numberPublications = []
    colabs = []
    affList = []
    
    for k in keylist:
        if data[k].get('auths'):
            for authors in data[k]['auths']:
                if authors['name'] not in authorsList:
                    authorsList.append(authors['name'])
                    numberPublications.append(1)
                    colabs.append(len(data[k]['auths']))
                    affList.append(authors["affiliation"])
                else:
                    index = authorsList.index(authors['name'])
                    numberPublications[index] = numberPublications[index] + 1
                    colabs[index] = len(data[k]['auths']) + colabs[index]

    print("Total authors without repetition: ", len(authorsList))
    print()

    ##The authors are grouped with their publications and colaborations inside a list, and then
    ##sorted.
    rankingAuthors = []
    for i in range(len(authorsList)):
        d = {'author': authorsList[i], 'affiliation': affList[i], 'publications': numberPublications[i], 'colabs': colabs[i]}
        rankingAuthors.append(d)

    rankingAuthors = sorted(rankingAuthors, key = lambda i: i['colabs'], reverse=True)
    print(rankingAuthors[0])
    return {rankingAuthors[0]["author"]: {"links": [], "affiliation": rankingAuthors[0]["affiliation"]}}

def erdos_iter(data, graph, zero):
    for _, j in data.items():            
        if not "auths" in j:
            continue
        hits = [x["name"] for x in j["auths"] if x["name"] in graph[-2]]
        if len(hits):
            for k in j["auths"]:
                new = True

                for level in graph[:-1]:
                    if k["name"] in level:
                        new = False
                        break
                if not new:
                    continue
                if not k["name"] in graph[-1]:
                    graph[-1][k["name"]] = {"links":[], "affiliation":k["affiliation"]}
                    #graph[-1][k["name"]] = []
                for h in hits:
                    if not h in graph[-1][k["name"]]:
                        graph[-1][k["name"]]["links"].append(h)
    return graph

def erdos_graph(data, zero, diameter=2):
    ### CALCULATES ERDOS GRAPH UP TO SOME ERDOS NUMBER. IF NUMBER IS LESS THAN ZERO, WE CALCULATE FULL GRAPH
    #graph = [{zero: {"links": [], "affiliation"}}]
    graph = [zero]
    if diameter > 0:
        for i in range(diameter):
            graph.append({})
            graph = erdos_iter(data, graph, zero)
    else:
        while len(graph[-1]):
            graph.append({})
            graph= erdos_iter(data, graph, zero)
        del graph[-1]
    return graph

def get_erdos(data, zero, author):
    ### ERDOS DISTANCE BETWEEN TWO AUTHORS
    #graph = [{zero: []}]
    graph = [zero]
    while len(graph[-1]) and not author in graph[-1]:
        graph.append({})
        graph = erdos_iter(data, graph, zero)
    if not len(graph[-1]):
        return -1
    return len(graph) - 1

def visualize_erdos(graph, labels_on=True):
    G = nx.Graph()
    pos = nx.spring_layout(G)
    nodes = []
    edges = []
    colors = []
    ref_aff = ""
    for i,j in graph[0].items():
        ref_aff = j["affiliation"]
    
    labels = {}
    for i, level in enumerate(graph):
        for name, conns in level.items():
            G.add_node(name)
            nodes.append(name)
            if not i:
                colors.append((1, 0,0))
            else:
                if conns["affiliation"] == ref_aff:
                    colors.append((1, 1/(len(graph)-i+0.5), 1/(len(graph)-i+0.5)))
                else:
                    colors.append((1/(len(graph)-i+0.5), 1/(len(graph)-i+0.5), 1))
            for conn in conns["links"]:
                G.add_edge(name, conn)
                edges.append([name, conn])
        if labels_on:
            for x in level:
                labels[x] = x
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, nodelist=nodes, edgelist=edges, labels=labels, node_color=colors)
    plt.show()
            

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Usage: python erdos.py $JSON_DB [LABELS_ON]")
        exit()
    with open(sys.argv[1]) as f:
        data = json.load(f)
    labels_on = False
    if len(sys.argv) > 2:
        labels_on = True
    zero = most_collabs(data)
    print()
    print("Task 8. Amounts of authors with Erdos no. 0, 1, 2 respectively. Erdos no. 0 belongs to Jessica D. Sundquist")
    graph = erdos_graph(data, zero)
    for i, j in enumerate(graph):
        print(i, len(j))

    print()
    print("Task 9. Example of determining erdos distance between two scientists. Sundquist is used also here.")
    print("Barlage,Michael", get_erdos(data, zero, "Barlage,Michael"))

    print()
    print("Task 10. Visualization of erdos network up to no. 2")
    visualize_erdos(graph, labels_on=labels_on)
