# -*- coding: utf-8 -*-
"""
Created on Mon Dec 02 09:08:16 2013

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
                        if G[wnode][x] >= final_dist[wnode][0]:
                            d = G[wnode][x]
                        else:
                            d = final_dist[wnode][0]
                        #dist_so_far[x] = [final_dist[wnode][0] + G[wnode][x], path]
                        dist_so_far[x] = [d, path]
                        #heapq.heappush(heap, (final_dist[wnode][0]+G[wnode][x], x, path+[x]))
                        heapq.heappush(heap, (d, x, path+[x]))
                    elif G[wnode][x] > dist_so_far[x][0]:
                        dist_so_far[x] = [G[wnode][x], path]
                        heapq.heappush(heap, (G[wnode][x], x, path+[x]))
                    
    return final_dist

def make_link(G, node1, node2, obscurity):
    obs = obscurity[node2]
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = obs
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = obs
    return G
    
def get_weights(filename):
    tsv = csv.reader(open(filename), delimiter='\t')
    
    obs = {}
    for (movie, year, weight) in tsv:
        obs[movie] = weight
    
    return obs

        

def read_graph(filename, obscurity):
    # Read an undirected graph in CSV format. Each line is an edge
    tsv = csv.reader(open(filename), delimiter='\t')
    G = {}
    for (node1, node2, year) in tsv:
        make_link(G, node1, node2, obscurity)
        
    return G
    
    
obscurity = get_weights('weights')
G = read_graph('imdb', obscurity)

test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
        #(u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}
        

for t in test:
    d = dijkstra(G, t[0])
    #print t, d[t[1]][0], test[t]
    
    
answer = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
          (u'Braine, Richard', u'Coogan, Will'): None,
          (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
          (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
          (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
          (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
          (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
          (u'Izquierdo, Ty', u'Kimball, Donna'): None,
          (u'Jace, Michael', u'Snell, Don'): None,
          (u'James, Charity', u'Tuerpe, Paul'): None,
          (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
          (u'McCabe, Richard', u'Washington, Denzel'): None,
          (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
          (u'Reid, R.D.', u'Boston, David (IV)'): None,
          (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
          (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
          (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
          (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
          (u'Sloan, Tina', u'Dever, James D.'): None,
          (u'Wasserman, Jerry', u'Sizemore, Tom'): None}
          
          
for a in answer:
    d = dijkstra(G, a[0])
    print a, d[a[1]][0]






