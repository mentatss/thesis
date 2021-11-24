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
    actual_time, profit = 0
    for index, row in query_set.iterrows():
        while actual_time < bounded_time:
            actual_time += row['runtime_prediction']
            profit += row['profit']
            
    return(profit)

def Opt_Rnd(query, bounded_time):
    query_set = pd.read_csv(query)  #set of queries to be executed

    #Knapsack solver (random)
    actual_time, profit = 0
    while actual_time < bounded_time:
        index = random.randint(0, len(query_set))
        profit += query_set.at[index, 'profit']
        actual_time += query_set.at[index, 'runtime']

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
    actual_time, profit = 0
    for index, row in query_set.iterrows():
        while actual_time < bounded_time:
            actual_time += row['runtime']
            profit += row['profit']

    return(profit)

