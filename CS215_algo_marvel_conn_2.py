# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:59:43 2013

@author: Stephen
"""

import csv, heapq

def dijkstra(G,v):
    heap = [(0,v,[])]
    heapq.heapify(heap)
    dist_so_far = {}
    dist_so_far[v] = [0,[]]
    final_dist = {}
    while len(final_dist) < len(G) and len(heap)>0:
        #w = shortest_dist_node(dist_so_far)
        #while True:
        (wval, wnode, path) = heapq.heappop(heap)
        # lock it down!
        if wnode not in final_dist:
            final_dist[wnode] = [wval, path]
            #final_dist[w] = dist_so_far[w]
            del dist_so_far[wnode]
        
            for x in G[wnode]:
                if x not in final_dist:
                    if x not in dist_so_far:
                        dist_so_far[x] = [final_dist[wnode][0] + G[wnode][x], path]
                        heapq.heappush(heap, (final_dist[wnode][0]+G[wnode][x], x, path+[x]))
                    elif final_dist[wnode][0] + G[wnode][x] < dist_so_far[x][0]:
                        dist_so_far[x] = [final_dist[wnode][0] + G[wnode][x], path]
                        heapq.heappush(heap, (final_dist[wnode][0]+G[wnode][x], x, path+[x]))
                    
    return final_dist

def make_char_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 1
    else:
        (G[node1])[node2] += 1
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 1
    else:
        (G[node2])[node1] += 1
        
    return G

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    #if node2 not in G:
        #G[node2] = {}
    #(G[node2])[node1] = 1
    return G

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    bookG = {}
    characterG = {}
    for (node1, node2) in tsv:
        make_link(G, node1, node2)
        make_link(bookG, node2, node1)
        
    for node in bookG:
        L = bookG[node].keys()
        for i in xrange(1, len(L)):
            char1 = L[i]
            for j in xrange(0,i):
                char2 = L[j]
                
                make_char_link(characterG, char1, char2)                
    
    
    
    for node in characterG:
        for match in characterG[node]:
            characterG[node][match] = 1.0/characterG[node][match]

    return characterG

def short_path(G, v):
    '''return shortest paths from v to all other nodes it can reach'''
    path_distance = {}
    path_distance[v] = 0
    
    open_list = [v]
    visited = {}
    
    while len(open_list) > 0:
        
        current = open_list.pop(0)
        visited[current] = 1
        
        for neighbor in G[current]:
            if neighbor not in visited:
                if neighbor not in path_distance:
                    path_distance[neighbor] = path_distance[current]+1
                if neighbor not in open_list:
                    open_list.append(neighbor)
        
        #del open_list[0]
    
    return path_distance
    
    
CHARS = ['SPIDER-MAN/PETER PAR','GREEN GOBLIN/NORMAN ','WOLVERINE/LOGAN ','PROFESSOR X/CHARLES ',
         'CAPTAIN AMERICA']


# Read the marvel comics graph
marvelG = read_graph('marvel2')

print len(marvelG)

shortest_paths_unweight = {}

for node in CHARS:
    shortest_paths_unweight[node] = short_path(marvelG, node)
    print node, len(shortest_paths_unweight[node])

shortest_weight = {}

for node in CHARS:
    shortest_weight[node] = dijkstra(marvelG, node)
    print node, len(shortest_weight[node])


total = 0

for hero in CHARS:
    for match in shortest_paths_unweight[hero]:
        if shortest_paths_unweight[hero][match] != len(shortest_weight[hero][match][1]):
            total+=1
            print hero, match
            print shortest_paths_unweight[hero][match], shortest_weight[hero][match][1]
            print total

print total

