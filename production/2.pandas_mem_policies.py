
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
query = "SELECT architecture, mapper, dataset, policy, threads, socket, counter, value  FROM mem_policies;"
df = pd.read_sql(query, con=conn)
grouped = df.groupby(["architecture", "mapper", "dataset", "policy", "threads", "socket", "counter"])
results = grouped.agg([np.mean, np.std])

results.rename(columns={"('value', 'mean')":"mean"})
results.rename(columns={"('value', 'std')":"std"})
#results = grouped.agg({'mean' : np.sum,'std' : np.mean})

try:
	results.to_sql('results_mem_policies', conn, if_exists='replace')
except ValueError:
	print("Table already exist - Nothing to do ")

conn.commit()





