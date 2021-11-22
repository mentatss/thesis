import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV
import io

#Generate query for the forward search, returns id of all article that the origin links to
def forward_generator(sparql_obj, article):
    sparql_obj.setQuery(f'''
        SELECT ?id
        WHERE {{ 
        ?linkto dbo:wikiPageID ?id.
        ?origin dbo:wikiPageWikiLink  ?linkto.
        ?origin dbo:wikiPageID {article}.
        }}
        ''')
    sparql_obj.setReturnFormat(CSV) #CSV for quick and easy formating, also better performance
    qres = sparql_obj.query().convert().decode('u8')
    return qres

#Generate query for the backward search, returns id of all article that links to the origin
def backward_generator(sparql_obj, article):
    sparql_obj.setQuery(f'''
        SELECT ?id
        WHERE {{ 
        ?linkfrom dbo:wikiPageID ?id.
        ?linkfrom dbo:wikiPageWikiLink ?origin.
        ?origin dbo:wikiPageID {article}.
        }}
        ''')
    sparql_obj.setReturnFormat(CSV) #CSV for quick and easy formating, also better performance
    qres = sparql_obj.query().convert().decode('u8')
    return qres

#Is dst reachable from src within d hops?
def reachable(src, dst, d):
    # Return trivial answer when src is the same as dst
    if src == dst:
        return (True, 0)

    #Variable list
    queue_forward = [src]           #Querry queue for next depth
    queue_backward = [dst]
    visited_forward = [src]         #Visited nodes from search
    visited_backward = [dst]
    next_depth = []                 #Helper list to gather next querry queue
    depth_forward = 0               #Current search depth
    depth_backward = 0
    sparql = SPARQLWrapper('http://127.0.0.1:8890/sparql')  #SPARQL Endpoint

    #Iterate until either bound is reached or a path is found (common element in both search direction)
    while (depth_forward + depth_backward) < d and set(visited_forward).isdisjoint(visited_backward):   

        #Check which direction has less node to visit and search that direction
        if len(queue_forward) <= len(queue_backward):
            #Search in forward direction from src
            depth_forward += 1

            #Iterate through queue
            while queue_forward:
                article = queue_forward.pop(0)
                qres = forward_generator(sparql, article)
                #Gather node to be visites in next depth, as well as append to list of visited nodes
                next_depth += pd.read_csv(io.StringIO(qres)).id.to_list()
                visited_forward += pd.read_csv(io.StringIO(qres)).id.to_list()

            #Update new queue for next depth
            queue_forward = list(set(next_depth))
            next_depth.clear()

        else:
            #Search in backward direction from dst
            depth_backward +=1

            #Iterate through queue
            while queue_backward:
                article = queue_backward.pop(0)
                qres = backward_generator(sparql, article)
                #Gather node to be visites in next depth, as well as append to list of visited nodes
                next_depth += pd.read_csv(io.StringIO(qres)).id.to_list()
                visited_backward += pd.read_csv(io.StringIO(qres)).id.to_list()

            #Update new queue for next depth
            queue_backward = list(set(next_depth))
            next_depth.clear()

    actual_depth = depth_forward + depth_backward

    #Both set have common elements (isdisjoint() == False) -> reachable 
    #Both set have no common elements (isdisjoint() == True) -> not reachable 
    #Return opposite of isdisjoint()
    return (not set(visited_forward).isdisjoint(visited_backward), actual_depth)

#One directional BFS
def reachable2(src, dst, d):
    # Return trivial answer when src is the same as dst
    if src == dst:
        return (True, 0)

    #Variable list
    queue = [src]           #Querry queue for next depth
    visited = [src]         #Visited nodes from search
    next_depth = []         #Helper list to gather next querry queue
    depth = 0               #Current search depth
    sparql = SPARQLWrapper('http://127.0.0.1:8890/sparql')  #SPARQL Endpoint

    #Iterate until bound is reached
    while depth < d:
        #Search in forward direction from src
        depth += 1

        #Iterate through queue
        while queue:
            article = queue.pop(0)
            qres = forward_generator(sparql, article)
            temp = pd.read_csv(io.StringIO(qres)).id.to_list() #List of neighbor of article
            if dst in temp: return (True, depth)
            for node in temp:
                #Gather unvisited node to be visites in next depth, as well as append to list of visited nodes
                if node not in visited:
                    next_depth.append(node)
                    visited.append(node)

        #Update new queue for next depth
        queue = list(set(next_depth))
        next_depth.clear()

    return (dst in visited, depth)

#Optimized version of reachable, check for common elements on the fly
def reachable3(src, dst, d):
    # Return trivial answer when src is the same as dst
    if src == dst:
        return (True, 0)

    #Variable list
    queue_forward = [src]           #Querry queue for next depth
    queue_backward = [dst]
    visited_forward = [src]         #Visited nodes from search
    visited_backward = [dst]
    next_depth = []                 #Helper list to gather next querry queue
    depth_forward = 0               #Current search depth
    depth_backward = 0
    sparql = SPARQLWrapper('http://127.0.0.1:8890/sparql')  #SPARQL Endpoint

    #Iterate until either bound is reached or a path is found (common element in both search direction)
    while (depth_forward + depth_backward) < d:
        #Check which direction has less node to visit and search that direction
        if len(queue_forward) <= len(queue_backward):
            #Search in forward direction from src
            depth_forward += 1

            #Iterate through queue
            while queue_forward:
                article = queue_forward.pop(0)
                qres = forward_generator(sparql, article)
                temp = pd.read_csv(io.StringIO(qres)).id.to_list() #temp is list of neighbor of current article
                for node in temp:
                    if node in visited_backward:
                        #if a neigbour of the current article is already in the set of visited node in other direction, terminates
                        return (True, depth_forward + depth_backward)
                    elif node not in visited_backward: 
                        #Gather unvisited node to be visites in next depth, as well as append to list of visited nodes
                        next_depth.append(node)
                        visited_forward.append(node)
                    
            #Update new queue for next depth
            queue_forward = list(set(next_depth))
            next_depth.clear()

        else:
            #Search in backward direction from dst
            depth_backward +=1

            #Iterate through queue
            while queue_backward:
                article = queue_backward.pop(0)
                qres = backward_generator(sparql, article)
                temp = pd.read_csv(io.StringIO(qres)).id.to_list() #temp is list of neighbor of current article
                for node in temp:
                    #if a neigbour of the current article is already in the set of visited node in other direction, terminates
                    if node in visited_forward:
                        return(True, depth_forward + depth_backward)
                    elif node not in visited_backward:
                        #Gather unvisited node to be visites in next depth, as well as append to list of visited nodes
                        next_depth.append(node)
                        visited_backward.append(node) 
                
            #Update new queue for next depth
            queue_backward = list(set(next_depth))
            next_depth.clear()

    #Both set have common elements (isdisjoint() == False) -> reachable 
    #Both set have no common elements (isdisjoint() == True) -> not reachable 
    #Return opposite of isdisjoint()
    return (not set(visited_forward).isdisjoint(visited_backward), depth_forward + depth_backward)
