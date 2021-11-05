import pandas
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import io
import time

#Get 1st degree neighbour of origin article
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
SELECT ?id
WHERE { 
 ?linkto dbo:wikiPageID ?id.
 ?origin    dbo:wikiPageWikiLink  ?linkto.
 ?origin  dbo:wikiPageID 91386.
}
""")
sparql.setReturnFormat(CSV)
results = sparql.query().convert().decode('u8')
#read csv returen from query, add the neighbor to the list
c=pandas.read_csv(io.StringIO(results))
neighbor=c.id.to_list()

avgrun=[]
#for each 1st degree neighbour, do the same query to find 2nd degree neighbour and add to the list
for a in range(len(neighbor)):
    
    start=time.time()
    sparql.setQuery(f'''
        SELECT ?id
        WHERE {{ 
            ?linkto dbo:wikiPageID ?id.
            ?origin    dbo:wikiPageWikiLink  ?linkto.
            ?origin  dbo:wikiPageID {neighbor[a]}.
        }}
    ''')
    sparql.setReturnFormat(CSV)
    results = sparql.query().convert().decode('u8')
    c=pandas.read_csv(io.StringIO(results))
    neighbor+=c.id.to_list()
    runt=time.time()-start
    avgrun.append(runt)
    
print('Avg runtime: ', sum(avgrun)/len(avgrun))
print('Found:',len(neighbor),'2nd degree neighbours in', sum(avgrun),'secs')
