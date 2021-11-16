import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV
import io

sparql = SPARQLWrapper('http://127.0.0.1:8890/sparql')

def get_id(article):
    sparql.setQuery(f'''
        SELECT ?id
        WHERE {{ 
        <{article}> dbo:wikiPageID ?id
        }}
    ''')
    sparql.setReturnFormat(CSV)
    qres = sparql.query().convert().decode('u8')
    c = pd.read_csv(io.StringIO(qres))
    return c.iat[0,0]

def get_name(id):
    sparql.setQuery(f'''
        SELECT ?name
        WHERE {{ 
        ?name dbo:wikiPageID {id}
        }}
    ''')
    sparql.setReturnFormat(CSV)
    qres = sparql.query().convert().decode('u8')
    c = pd.read_csv(io.StringIO(qres))
    return c.iat[0,0]

def get_inlink(id):
    sparql.setQuery(f'''
        SELECT count(?article) as ?inlink
        WHERE {{ 
        ?article dbo:wikiPageWikiLink ?source.
        ?source  dbo:wikiPageID {id}.
        }}
    ''')
    sparql.setReturnFormat(CSV)
    qres = sparql.query().convert().decode('u8')
    c = pd.read_csv(io.StringIO(qres))
    return c.iat[0,0]

def get_outlink(id):
    sparql.setQuery(f'''
        SELECT count(?article) as ?outlink
        WHERE {{ 
        ?source dbo:wikiPageWikiLink ?article.
        ?source  dbo:wikiPageID {id}.
        }}
    ''')
    sparql.setReturnFormat(CSV)
    qres = sparql.query().convert().decode('u8')
    c = pd.read_csv(io.StringIO(qres))
    return c.iat[0,0]
