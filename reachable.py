import pandas as pd
import rdflib
from SPARQLWrapper import SPARQLWrapper, CSV
import io
import time

#Generate query for the forward search, returns all article that the origin links to
def forward_generator(sparql_obj, article):
    sparql_obj.setQuery(f'''
        SELECT ?id
        WHERE {{ 
        ?linkto dbo:wikiPageID ?id.
        ?origin dbo:wikiPageWikiLink  ?linkto.
        ?origin dbo:wikiPageID {article}.
        }}
        ''')
    sparql_obj.setReturnFormat(CSV)
    qres = sparql_obj.query().convert().decode('u8')
    return qres

#Generate query for the backward search, returns all article that links to the origin
def backward_generator(sparql_obj, article):
    sparql_obj.setQuery(f'''
        SELECT ?id
        WHERE {{ 
        ?linkfrom dbo:wikiPageID ?id.
        ?linkfrom dbo:wikiPageWikiLink ?origin.
        ?origin dbo:wikiPageID {article}.
        }}
        ''')
    sparql_obj.setReturnFormat(CSV)
    qres = sparql_obj.query().convert().decode('u8')
    return qres

def reachable(src, dst, d):
    if src == dst:
        return True

    queue_forward = []
    queue_backward = []
    visited_forward = []
    visited_backward = []
    depth_forward = 0
    depth_backward = 0
    sparql = SPARQLWrapper('http://127.0.0.1:8890/sparql')

    qres = forward_generator(sparql, src)
    queue_forward = pd.read_csv(io.StringIO(qres)).id.to_list()
    visited_forward += pd.read_csv(io.StringIO(qres)).id.to_list()
    depth_forward += 1

    qres = backward_generator(sparql, dst)
    queue_backward = pd.read_csv(io.StringIO(qres)).id.to_list()
    visited_backward += pd.read_csv(io.StringIO(qres)).id.to_list()
    depth_backward += 1

    while (depth_forward + depth_backward) < d and set(visited_forward).isdisjoint(visited_backward):    
        if len(queue_forward) > len(queue_backward):
            depth_forward += 1
            for article in queue_forward:
                qres = forward_generator(sparql, article)
                # queue_forward = pd.read_csv(io.StringIO(qres)).id.to_list()
                visited_forward += pd.read_csv(io.StringIO(qres)).id.to_list()
        else:
            depth_backward +=1
            for article in queue_backward:
                qres = backward_generator(sparql, article)
                # queue_backward = pd.read_csv(io.StringIO(qres)).id.to_list()
                visited_forward += pd.read_csv(io.StringIO(qres)).id.to_list()


    if (not set(visited_forward).isdisjoint(visited_backward)):
        return True

    return False

def main():
    if(reachable(682482, 7946, 3)):
        print('yeah')
    else:
        print('nah')

main()
