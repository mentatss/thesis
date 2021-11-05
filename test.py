import pandas
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import io
import time

#Get 1st degree neighbour of origin article
#When use with local endpoint, remove the line '?linkto  a  owl:Thing.' because local database does not have that
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
SELECT ?id
WHERE { 
 ?linkto  a  owl:Thing.
 ?linkto dbo:wikiPageID ?id.
 ?origin    dbo:wikiPageWikiLink  ?linkto.
 ?origin  dbo:wikiPageID 736.
}
""")
sparql.setReturnFormat(CSV)
results = sparql.query().convert().decode('u8')
#read csv returen from query, add the neighbor to the list
c=pandas.read_csv(io.StringIO(results))
neighbor=c.id.to_list()


#for each 1st degree neighbour, do the same query to find 2nd degree neighbour and add to the list
#also remove the line '?linkto  a  owl:Thing.' when use on local endpoint
for a in range(len(neighbor)):
    sparql.setQuery(f'''
        SELECT ?id
        WHERE {{ 
            ?linkto  a  owl:Thing.
            ?linkto dbo:wikiPageID ?id.
            ?origin    dbo:wikiPageWikiLink  ?linkto.
            ?origin  dbo:wikiPageID {neighbor[a]}.
        }}
    ''')
    sparql.setReturnFormat(CSV)
    results = sparql.query().convert().decode('u8')
    c=pandas.read_csv(io.StringIO(results))
    neighbor+=c.id.to_list()

    
print(len(neighbor))
