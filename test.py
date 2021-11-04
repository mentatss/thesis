import pandas
import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import io
import time

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

c=pandas.read_csv(io.StringIO(results))
neighbor=c.id.to_list()

rtime=0

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
    start=time.time()
    c=pandas.read_csv(io.StringIO(results))
    neighbor+=c.id.to_list()
    run=time.time()-start
    rtime+=run

print(len(neighbor))
print(rtime)