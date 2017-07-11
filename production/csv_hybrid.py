import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import matplotlib

matplotlib.style.use('ggplot')
print("Testing connection to DB")
path = os.getcwd()
conn = sqlite3.connect(path + '/database/logproc.db')
c = conn.cursor()
mappers=['gem','mem','snap','bowtie2']
architectures=['penguin', 'batcat']
datasets=['GCAT','na12878']
if conn != None:
    print ("Connection succesful")
for architecture in architectures:
    for dataset in datasets:
        for mapper in mappers:
            query = "SELECT architecture, mapper, dataset, policy, threads, value_mean, value_std, error_mean, error_std, max_mean, max_std, min_mean, min_std, counter  FROM results_hybrid_final WHERE counter= 'seconds'and dataset='" + str(dataset) + "' and architecture='" + str(architecture) + "' and mapper='"+ str(mapper) +"';"
            print("QUERY: ", query)
            df = pd.read_sql(query, con=conn)
            df.to_csv(path + '/files/CSV/HYB_' + str(mapper)  + "_" + str(architecture) + "_" + str(dataset)  + ".csv",sep=';')
            print (df.mean)
#grouped = df.groupby(["architecture", "mapper", "dataset", "policy", "threads", "socket", "counter"])
#df.plot(x='threads', y='mean')
#df.set_ylim(0, max(df.mean))
#plt.show()
