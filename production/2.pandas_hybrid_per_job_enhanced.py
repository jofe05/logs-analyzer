
import pandas as pd
import numpy as np
import sqlite3
import os


print("Testing connection to DB")
path = os.getcwd()
conn = sqlite3.connect(path + '/database/logproc.db')
c = conn.cursor()

if conn != None:
    print ("Connection succesful")
query = "SELECT jobId, architecture, mapper, dataset, policy, threads, instances, counter, value  FROM hybrid_enhanced;"
df = pd.read_sql(query, con=conn)
grouped = df.groupby(["jobId", "architecture", "mapper", "dataset", "policy", "threads", "counter"])
results = grouped.agg([np.max, np.min, np.mean, np.std])



#results.rename(columns={"('value',_'amax')":"max"})
#results.rename(columns={"('value',_'mean')":"mean"})
#results.rename(columns={"('value',_'std')":"std"})

results.columns = ['max', 'min', 'value_perJob_mean', 'value_perJob_std']




try:
	results.to_sql('results_hybrid', conn, if_exists='replace')
except ValueError:
	print("Table already exist - Nothing to do ")

conn.commit()

query2 = "SELECT jobId, architecture, mapper, dataset, policy, threads, counter, value_perJob_mean, value_perJob_std, max, min  FROM results_hybrid;"
df2 = pd.read_sql(query2, con=conn)
grouped2 = df2.groupby(["architecture", "mapper", "dataset", "policy", "threads", "counter"])
results2 = grouped2.agg([np.mean, np.std])

a = list(results2.columns.values)
print("HEADERS:", a , " \n")

results2.columns = ['jobId_mean', 'jobId_std', 'value_mean', 'value_std', 'error_mean', 'error_std', 'max_mean', 'max_std', 'min_mean', 'min_std' ]

results2 = results2.drop('jobId_mean', 1)
results2 = results2.drop('jobId_std', 1)

a = list(results2.columns.values)
print("HEADERS:", a , " \n")


try:
	results2.to_sql('results_hybrid_final', conn, if_exists='replace')
except ValueError:
	print("Table already exist - Nothing to do ")




