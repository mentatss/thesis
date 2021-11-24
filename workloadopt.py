import pandas as pd
import random

def Opt_RF(query, prediction_model, bounded_time):
    profit = 0
    query_set = pd.read_csv(query)
    model = pd.read_pickle(prediction_model)

    query_set['runtime_prediction'] = model.predict(query_set.filter(items=['in_src', 'out_src', 'in_dst', 'out_dst', 'bound'], axis=1))
    for index, row in query_set.iterrows():
        query_set.at[index, 'ratio']  = row['profit']/row['runtime_prediction']
    query_set.sort_values(by=['ratio'], ascending=False, inplace=True)
    query_set = query_set.reset_index(drop=True)

    actual_time = 0
    for index, row in query_set.iterrows():
        while actual_time < bounded_time:
            actual_time += row['runtime_prediction']
            profit += row['profit']
    return(profit)

def Opt_Rnd(query, bounded_time):
    profit = 0
    query_set = pd.read_csv(query)

    actual_time = 0
    while actual_time < bounded_time:
        index = random.randint(0, len(query_set))
        profit += query_set.at[index, 'profit']
        actual_time += query_set.at[index, 'runtime']

    return(profit)


def Opt_True(query, bounded_time):
    profit = 0
    query_set = pd.read_csv(query)

    for index, row in query_set.iterrows():
        query_set.at[index, 'ratio']  = row['profit']/row['runtime']

    query_set.sort_values(by=['ratio'], ascending=False, inplace=True)
    query_set = query_set.reset_index(drop=True)
    
    actual_time = 0
    for index, row in query_set.iterrows():
        while actual_time < bounded_time:
            actual_time += row['runtime']
            profit += row['profit']

    return(profit)

print(Opt_RF('data/workloadopt.csv', 'reachable_no_opt.pkl', 300000))

# print(Opt_RF('data/workloadopt.csv', 300000))