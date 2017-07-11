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
        print (" idNumber: {0} Architecture: {1} Mapper: {2} Threads: {3} Socket: {4} Counter: {5} Value: {6} Experiment: {7} DataSet: {8}  ".format(self.idNumber, self.arch, self.mapper, self.threads, self.socket, self.counterName, self.counterValue, self.expName, self.dataSet))

    def row_to_list(self):
    	listRow=[]
    	listRow.append(self.idNumber)
    	listRow.append(self.arch)
    	listRow.append(self.mapper)
    	listRow.append(self.threads)
    	listRow.append(self.socket)
    	listRow.append(self.counterName)
    	listRow.append(self.counterValue)
    	listRow.append(self.expName)
    	listRow.append(self.dataSet)
    	return listRow


    
    def add_row_to_db(self, c):
        listRow = self.row_to_list()
        c.execute("INSERT INTO mem_policies(jobId, architecture, mapper, threads, socket, counter, value, policy, dataset) VALUES (?,?,?,?,?,?,?,?,?)", listRow)    
        print("Row Added")



if __name__ == "__main__":

    print(" **** Script Processor ****")
    print("Testing connection to DB")
    path = os.getcwd()
    dup=0
    conn = sqlite3.connect(path + '/database/logproc.db')
    c = conn.cursor()
    if conn != None:
        print ("Connection succesful")


    print("Working directory", path)
    pathLogs = path + "/files/input"
    outputLogs = path + "/files/csv/"
    foldersExp = os.listdir(pathLogs)
    foldersExp.remove('.DS_Store')
    foldersExp.remove('partitioning')
    foldersExp.remove('hybrid')
    print("Experiments to be processed: ")
    print(foldersExp)
    if "Y" == input('Want to continue? [Y/N]'):
        for experiment in foldersExp:
            currentRow = RowDB()
            foldersDataset = os.listdir(pathLogs + '/' + str(experiment))
            try:
                foldersDataset.remove('.DS_Store')
            except ValueError:
                pass
            currentRow.expName = str(experiment)
            print(foldersDataset)
            for dataset in foldersDataset: 
                logs = os.listdir(pathLogs + '/' + str(experiment) + '/' +str(dataset))
                currentRow.dataSet = dataset
                
                try:
                    logs.remove('.DS_Store')
                except ValueError:
                    pass
                print(logs)

                for file in logs:
                    print("Processing log file number:", file)
                    iFile = open(pathLogs + '/' + str(experiment) + '/' +str(dataset) + '/' + str(file), 'r')
                    nameFile = str(file).replace(".log", "")
                    #oFile = open(outputLogs + nameFile + '.csv', "w")
                    #writer = csv.writer(oFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL) 
                    nameFile = nameFile.split("_")
    
                    for arch in iFile:
                    
                        if re.match("batman", arch) or re.match("catwoman", arch) or re.match("penguin", arch):
                            #print("Architecture", arch)
                            arch = str(arch).replace("\n", "")
                            if (arch == "batman" or arch=="catwoman"):
                                arch = "batcat"
                            break
                    currentRow.idNumber = nameFile[1]
                    currentRow.arch = arch
                    currentRow.mapper = nameFile[0]
    
                    for line in iFile:        
                        if re.match(" Performance counter stats for", line):
                                                                   
                            #threads =  re.findall(r' [0-9]* ',line)
                            threads = re.match(r'.* ([0-9]*) .*', line)
        
                                   
                            #print ("threads1: ", threads.group(1))
                            #print ("threads1: ", threads.group(2))
                            #print ("threads_str ", str(threads))
                            #print ("threads_int", int(str(threads)))
                            currentRow.threads = int(threads.group(1))
        
                            #line = line.lstrip(' ')
                            #line_title = line.split(" ")
                            #writer.writerow(line_title)
                        if re.search('S[0-3]', line):
                        #print(line)
                            line_counter = line.split(" ")
                            line_counter = [x for x in line_counter if x != '']
                            line_counter = [x for x in line_counter if x != '16']
                            currentRow.socket = line_counter[0]
                            value = str(line_counter[1]).replace(",", "")
                            if line_counter[2] == "supported>":
                                currentRow.counterName = line_counter[3]
                                currentRow.counterValue = 0

                            else:
                                currentRow.counterName = line_counter[2]
                                currentRow.counterValue = float(value)

    
                            #Removes comma separator (thousands)
                            
                            
                            #try:
                                #currentRow.counterValue = float(value)
                            #except ValueError:
                                #currentRow.counterValue = 0
                            currentRow.print_row_db()
                            try:
                                currentRow.add_row_to_db(c)
                            except sqlite3.IntegrityError:
                                dup=dup+1
                                #currentRow.print_row_db()
                                print("Row duplicated - won't be added to DB")
                            #writer.writerow(line_counter[0:3])
                            #writer3.writerow(line_counter[0:3])
    
                        if re.search('seconds time elapsed', line):
    
                            line = line.lstrip(' ')
                            line_time = line.split(" ")
                            
                            currentRow.socket = 'S4'
                            currentRow.counterName = line_time[1]
                            currentRow.counterValue = line_time[0]
        
                            #currentRow.print_row_db()
                            try:
                                currentRow.add_row_to_db(c)
                            except sqlite3.IntegrityError:
                                dup=dup+1
                                #currentRow.print_row_db()
                                print("Row duplicated - won't be added to DB")
                            #writer.writerow(line_time2)
                            
    
    
    
    
    
                

    else: 
    	print("Nothing to do")
    conn.commit()
    print ("Duplicates: ", dup)

