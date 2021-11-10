from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3, CSV
import pandas as pd
import io
import time

df = pd.read_csv("C:/Users/haina/Downloads/dbpedia_1_subject_counts_o9_tops.txt/test3.csv",delim_whitespace=True, header=None)
article_list = list(df[0])


sparql = SPARQLWrapper('http://127.0.0.1:8890/sparql')
id_list = []

for article in article_list:
    sparql.setQuery(f'''
        SELECT ?id
        WHERE {{ 
        {article} dbo:wikiPageID ?id
        }}
    ''')
    sparql.setReturnFormat(CSV)
    qres = sparql.query().convert().decode('u8')
    c=pd.read_csv(io.StringIO(qres))
    id_list+=c.id.to_list()

dflist = pd.DataFrame(id_list, columns=["id"])
dflist.to_csv("C:/Users/haina/Downloads/dbpedia_1_subject_counts_o9_tops.txt/idlist.csv", index=False)