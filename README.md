# Bachelor thesis

This repo contains the source code and dataset that were utilized during the writing of the bachelor thesis by Hai Nam Tran at the TUHH. 

## Requirement

Following library in Python are needed:
- RDFLib and its extension SPARQLWrapper for the graph query
- scikit-learn and TensorFlow for the ML models
- pandas for general data manipulation

If setting up a local SPARQL endpoint, OpenLink Virtuoso is recommended for similar results with the thesis.


## Content

The data folder contains the datasets that were gathered by the author:
- *dataset.csv* and *dataset_alt.csv* are queries generated and executed with the normal (and optimized) algorithm respectively, the data in *dataset.csv* was used to train the predictor *reachable_no_opt.pkl*
- *distance.csv* contains queries used to train the distance predictor *distance_predictor.pkl*
- *workloadopt.csv* contains queries used to test the workload optimizer, the "profit" column was randomly generated as mentioned in the thesis.
- *idlist.csv* contains ids of wikipedia articles that matched the requirement in the thesis (more than 40 out-degree)
- *template.csv* contains template to conveniently create dataframe during the implementation.

Content of source code files:
- *reachable*: implementation of the reachability queue
- *helper*: helper functions (get names, ids, in and outdegree)
- *models* and *MLP*: implementation of ML models in sklearn and tensorflow
- *workloadopt*: implementation of the workload optimizer
- *dataset*: functions to sample queries

## General workflow

Here is a sample workflow:
- Generate random query and measure runtime (using *dataset*)
- Initialize ML models and train them (using *models* or *MLP*)
- Test the models with the workload optimizer (*workloadopt*)

If no local endpoint is available, DBPedia's endpoint can be queried, however runtime would be extremely long. The above mentioned datasets can be used if no endpoint is available. ML models can be trained directly on them (same datasets were used during the thesis).

The process of setting up a local endpoint is also discussed in the thesis, a helpful instruction can also be found [here](https://medium.com/@nadjetba/how-to-setup-dbpedia-and-geonames-on-openlink-virtuoso-f203321fd0fe).




## Contributing
Readers are welcomed to use, expand and modify the code. Further contribution to the topic of the thesis is appreciated!

Questions about the implementation/thesis are welcomed. I can also be reached at hai.tran(at)tuhh.de
