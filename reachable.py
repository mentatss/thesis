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

def reachable(src, dst, d):
    # Return trivial answer when src is the same as dst
    if src == dst:
        return True

    #Variable list
    queue_forward = [src]           #Querry queue for next depth
    queue_backward = [dst]
    visited_forward = [src]         #Visited nodes from search
    visited_backward = [dst]
    next_depth = []                 #Helper list to gather next querry queue
    depth_forward = 0               #Search depth
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
            queue_forward = next_depth
            next_depth = []

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
            queue_backward = next_depth
            next_depth = []

    #Both set have common elements (isdisjoint() == False) -> reachable 
    #Both set have no common elements (isdisjoint() == True) -> not reachable 
    #Return opposite of isdisjoint()
    return (not set(visited_forward).isdisjoint(visited_backward))
