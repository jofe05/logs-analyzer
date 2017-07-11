import re
import os
import csv
import sqlite3


class RowDB:
    def __init__(self):
        idNumber = None
        arch = None
        mapper = None
        threads = None
        socket = None
        counterName = None
        counterValue = None
        expName = None
        dataSet = None

    def print_row_db(self):
        print (" --- Row adding to DB --- ")
        print (" idNumber: {0} Architecture: {1} Mapper: {2} Threads: {3} Instances: {4} Counter: {5} Value: {6} Experiment: {7} DataSet: {8}  ".format(self.idNumber, self.arch, self.mapper, self.threads, self.instance, self.counterName, self.counterValue, self.expName, self.dataSet))

    def row_to_list(self):
    	listRow=[]
    	listRow.append(self.idNumber)
    	listRow.append(self.arch)
    	listRow.append(self.mapper)
    	listRow.append(self.threads)
    	listRow.append(self.instance)
    	listRow.append(self.counterName)
    	listRow.append(self.counterValue)
    	listRow.append(self.expName)
    	listRow.append(self.dataSet)
    	return listRow


    
    def add_row_to_db(self, c):
        listRow = self.row_to_list()
        c.execute("INSERT INTO hybrid_enhanced(jobId, architecture, mapper, threads, instances, counter, value, policy, dataset) VALUES (?,?,?,?,?,?,?,?,?)", listRow)    
        print("Row Added")



if __name__ == "__main__":

    print(" **** Script Processor ****")
    print("Testing connection to DB")
    path = os.getcwd()
    conn = sqlite3.connect(path + '/database/logproc.db')
    c = conn.cursor()
    dup=0
    if conn != None:
        print ("Connection succesful")


    print("Working directory", path)
    pathLogs = path + "/files/input"
    outputLogs = path + "/files/csv/"
    foldersExp = os.listdir(pathLogs + '/hybrid')
    try:
        foldersExp.remove('.DS_Store')
    except ValueError:
        pass
    print(foldersExp)
    if "Y" == input('Want to continue? [Y/N]'):        
        for experiment in foldersExp:
            currentRow = RowDB()
            foldersDataset = os.listdir(pathLogs + '/hybrid/' + str(experiment))
            print ("path: ", pathLogs + '/' + str(experiment))
            try:
                foldersDataset.remove('.DS_Store')
            except ValueError:
                pass
            currentRow.expName = str(experiment)
            print(foldersDataset)
            for dataset in foldersDataset: 
                logs = os.listdir(pathLogs + '/hybrid/' + str(experiment) + '/' + str(dataset))
                currentRow.dataSet = dataset
                
                try:
                    logs.remove('.DS_Store')
                except ValueError:
                    pass
                print(logs)
                for file in logs:
                    print("Processing log file number:", file)
                    iFile = open(pathLogs + '/hybrid/' + str(experiment) + '/' + str(dataset) + '/' + str(file), 'r')
                    nameFile = str(file).replace(".txt", "")
                    #oFile = open(outputLogs + nameFile + '.csv', "w")
                    #writer = csv.writer(oFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL) 
                    nameFile = nameFile.split(".")
                    currentRow.idNumber = nameFile[0]
                    if (nameFile[2] == "batman" or nameFile[2] == "catwoman"):
                        currentRow.arch = 'batcat'
                    else:
                        currentRow.arch = nameFile[2]    
                    currentRow.mapper = nameFile[1]
                    currentRow.instance = nameFile[3]
    
                    for line in iFile:        
                        if re.match(" Performance counter stats for", line):
                                                                   
                            #threads =  re.findall(r' [0-9]* ',line)
                            threads = re.match(r'.* ([0-9]*) .*', line)
                            #print ("threads1: ", threads.group(1))
                            currentRow.threads = int(threads.group(1))
                                
                        if re.search('cache-misses',line) or re.search(' cycles  ',line) or re.search('instructions',line) or re.search(' cs ',line) or re.search('faults',line) or re.search('migrations',line) or re.search('bus-cycles',line) or re.search('idle-cycles-.*',line) or re.search('L1-dcache-.*',line) or re.search('LLC-.*',line) or re.search('dTLB-load-*',line) or re.search('iTLB-*',line) or re.search('branch-.*',line):
                            #print line
                            line_counter = line.split(" ")
                            line_counter = [x for x in line_counter if x != '']    #Crea un array con los elementos distinto a ''
                            #print ("Counters: ", line_counter[0:3])
                            currentRow.counterName = line_counter[1]
    
                            #Removes comma separator (thousands)
                            value = str(line_counter[0]).replace(",", "")
                            
                            try:
                                currentRow.counterValue = float(value)
                            except ValueError:
                                currentRow.counterValue = 0
                            
                            currentRow.print_row_db()
                            
                            try:
                                currentRow.add_row_to_db(c)
                            except sqlite3.IntegrityError:
                                dup=dup+1
                            #writer.writerow(line_counter[0:3])
                            #writer3.writerow(line_counter[0:3])
    
                        if re.search('seconds time elapsed', line):
    
                            line = line.lstrip(' ')
                            line_time = line.split(" ")
                            
    
                            currentRow.counterName = line_time[1]
                            currentRow.counterValue = line_time[0]
        
                            currentRow.print_row_db()
                            try:
                                currentRow.add_row_to_db(c)
                            except sqlite3.IntegrityError:
                                dup=dup+1
                            #writer.writerow(line_time2)
                                
        
    
    
    
    
                
    
    else: 
    	print("Nothing to do")
    conn.commit()

