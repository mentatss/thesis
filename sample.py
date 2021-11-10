import pandas as pd
from urllib.parse import unquote
import random

n = 2000000 #number of rows in the file
s = 10000 #desired sample size
skip = sorted(random.sample(range(n),n-s))

f=pd.read_csv("C:/Users/haina/Downloads/dbpedia_1_subject_counts_o9_tops.txt/test2.csv", delim_whitespace=True, header=None, skiprows=skip)

for a in range (len(f)):
     f.iat[a,0] = unquote(f.iat[a,0])

f.to_csv("C:/Users/haina/Downloads/dbpedia_1_subject_counts_o9_tops.txt/test3.csv", index=False, header=False)