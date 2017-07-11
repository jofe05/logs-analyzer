
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
query = "SELECT architecture, mapper, dataset, policy, threads, instances, counter, value  FROM partitions;"
df = pd.read_sql(query, con=conn)
grouped = df.groupby(["architecture", "mapper", "dataset", "policy", "threads", "instances", "counter"])
results = grouped.agg([np.mean, np.std])
#results = grouped.aggregate({'mean' : np.sum, 'std' : np.mean})
results.rename(columns={"('value', 'mean')":"mean"})
results.rename(columns={"('value', 'std')":"std"})
try:
	results.to_sql('results_partitions', conn, if_exists='replace')
except ValueError:
	print("Table already exist - Nothing to do ")

conn.commit()





