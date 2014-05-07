# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:59:43 2013

@author: Stephen
"""

import csv

def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def read_graph(filename):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    for (node1, node2) in tsv: make_link(G, node1, node2)
    return G

# Read the marvel comics graph
marvelG = read_graph('marvel')

#build conn_dict by pairing everyone together
conn_dict = {}

print len(marvelG)

count = 0

'''
for node in marvelG:
    count+=1
    print count
    #all pairs in node are connected
    L = [i for i in marvelG[node]]
    for i in xrange(len(L)-1):
        for j in xrange(i+1, len(L)):
            s1 = str(L[i]) + ',' + str(L[j])
            s2 = str(L[j]) + ',' + str(L[i])
            
            if s1 in conn_dict:
                conn_dict[s1]+=1
            elif s2 in conn_dict:
                conn_dict[s2]+=1
            else:
                conn_dict[s1]=1


highest = 0
saved = ''

print len(conn_dict)

for pair in conn_dict:
    if conn_dict[pair]>highest:
        saved = pair
        highest = conn_dict[pair]
        print pair, conn_dict[pair]

'''

            
    