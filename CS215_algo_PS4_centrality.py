# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 10:48:37 2013

@author: Stephen
"""

#udacity centrality
#Algorithm Class Prob Set 4

#read file named 'file'

f = open('file', 'r')

G = {}
actors = set()
#movies = set()

for line in f:
    (actor, movie, year) = line.split('\t')
    movie = movie + year[:-1]
    
    actors.update([actor])
    #movies.update([movie])    
    
    if actor not in G:
        G[actor] = [movie]
    else:
        G[actor].append(movie)
    
    
    
    
    if movie not in G:
        G[movie] = [actor]
    else:
        G[movie].append(actor)
    
    
f.close()


def centrality(G, v):
    distance_from_start = {}
    open_list = [v]
    distance_from_start[v] = 0
    while len(open_list)!=0:
        node = open_list[0]
        open_list = open_list[1:]
        #get all movies
        movs = G[node]
        #go thru movies and get connected actors
        for movie in movs:
            new_actors = [i for i in G[movie] if i not in distance_from_start]
                        
            open_list += new_actors
            
            for act in new_actors:
                #add these to distance_from_start
                distance_from_start[act] = distance_from_start[node] + 2
    
     
    return (sum(distance_from_start.values())+0.0)/len(distance_from_start)


cent = {}

top = []

def find_max(top):
    m = top[0]
    for i in range(1,len(top)):
        if top[i][1] > m[1]:
            m = top[i]
    return m

for actor in list(actors):
    cent[actor] = centrality(G, actor)
    #print actor, cent[actor]
    
    if len(top)<20:
        top.append((actor, cent[actor]))
    else:
        m = find_max(top)
        #print top, m
        if cent[actor] < m[1]:
            print "ADDED", actor, cent[actor]
            top.append((actor, cent[actor]))
            top.remove(m)

for p in top:
    print p



