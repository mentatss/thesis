import pandas as pd
import random

def Opt_RF(query, prediction_model, bounded_time):
    query_set = pd.read_csv(query)              #set of queries to be executed
    model = pd.read_pickle(prediction_model)    #prediction model

    #predict the runtime of the received set of queries
    query_set['runtime_prediction'] = model.predict(query_set.filter(items=['in_src', 'out_src', 'in_dst', 'out_dst', 'bound'], axis=1))

    #calculate profit to runtime ratio of each query
    for index, row in query_set.iterrows():
        query_set.at[index, 'ratio']  = row['profit']/row['runtime_prediction']

    #sort ratio and update index
    query_set.sort_values(by=['ratio'], ascending=False, inplace=True)
    query_set = query_set.reset_index(drop=True)

    #Knapsack solver (based on predicted runtime)
    actual_time = 0
    profit = 0
    for index, row in query_set.iterrows():
        actual_time += row['runtime_prediction']
        profit += row['profit']
        if actual_time > bounded_time:
            break
            
    return(profit)

def Opt_Rnd(query, bounded_time):
    query_set = pd.read_csv(query)  #set of queries to be executed

    #Knapsack solver (random)
    actual_time = 0
    profit = 0

    try:
        while actual_time < bounded_time:
            sample_query = query_set.sample()
            profit += sample_query.iat[0,8]
            actual_time += sample_query.iat[0,7]
            query_set = query_set.drop(sample_query.index)
    except: #error handling in case bounded is too large, all sample are taken
        return(profit)

    return(profit)


def Opt_True(query, bounded_time):
    query_set = pd.read_csv(query)  #set of queries to be executed

    #calculate profit to runtime ratio of each query
    for index, row in query_set.iterrows():
        query_set.at[index, 'ratio']  = row['profit']/row['runtime']

    #sort ratio and update index
    query_set.sort_values(by=['ratio'], ascending=False, inplace=True)
    query_set = query_set.reset_index(drop=True)
    
    #Knapsack solver (based on real rumtime)
    actual_time = 0
    profit = 0
    for index, row in query_set.iterrows():
        actual_time += row['runtime']
        profit += row['profit']
        if actual_time > bounded_time:
            break

    return(profit)
