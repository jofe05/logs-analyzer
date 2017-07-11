import re
import os
import csv

class RowDB:
    def __init__(self):
        idNumber = None
        arch = None
        mapper = None
        threads = None
        socket = None
        counterName = None
        counterValue = None

    def printRowDB(self):
        print (" --- Row adding to DB --- ")
        print (" idNumber: {0} Architecture: {1} Mapper: {2} Threads: {3} Socket: {4} \
        	Counter: {5} Value: {6} ".format(self.idNumber, self.arch, self.mapper, self.threads, self.socket, self.counterName, self.counterValue))


if __name__ == "__main__":
	
    print(" **** Script Processor ****")
    path = os.getcwd()
    print("Working directory", path)
    pathLogs = path + "/GCAT/INPUT"
    outputLogs = path + "/GCAT/CSV/" 
    
    outputNumber = os.listdir(pathLogs)
    print("Logs to be processed: ")
    print(outputNumber)
    
    if "Y" == input('Want to continue? [Y/N]'):
    	for file in outputNumber:

            currentRow = RowDB() 

            print("Processing log file number:", file)
            iFile = open(pathLogs+'/'+str(file),'r')
            nameFile = str(file).replace( ".log", "") 
            oFile  = open(outputLogs+nameFile+'.csv', "w")        
            writer = csv.writer(oFile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL) 
            nameFile = nameFile.split("_")



            for arch in iFile:
            
                if re.match("batman", arch) or re.match("catwoman", arch) or re.match("penguin", arch):
                    #print("Architecture", arch)
                    arch = str(arch).replace("\n","") 
                    break

            currentRow.idNumber = nameFile[1]
            currentRow.arch = arch
            currentRow.mapper = nameFile[0]

            for line in iFile:        

                if re.match(" Performance counter stats for", line):
                                                           
                    #threads =  re.findall(r' [0-9]* ',line)
                    threads =  re.match(r'.* ([0-9]*) .*',line)

                    print ("threads1: ", threads.group(1))

                    #print ("threads1: ", threads.group(1))
                    #print ("threads1: ", threads.group(2))
                    #print ("threads_str ", str(threads))
                    #print ("threads_int", int(str(threads)))
                    


                    currentRow.threads = int(threads.group(1))

                    #line = line.lstrip(' ')
                    #line_title = line.split(" ")
                    #writer.writerow(line_title)

            
                if re.search('S[0-3]',line):    
                #print(line)
                    line_counter = line.split(" ")
                    line_counter = [x for x in line_counter if x != '']    #Crea un array con los elementos distinto a ''
                    line_counter = [x for x in line_counter if x != '16']  # Saca el elemento que sea igual a 16
                    line_counter[1], line_counter[2] = line_counter[2], line_counter[1]
                    currentRow.socket = line_counter[0]
                    currentRow.counterName = line_counter[1]

                    value = str(line_counter[2]).replace(",","") #Removes comma separator (thousands)
                    
                    if value.isdigit()
                        currentRow.counterValue = float(value)
                    else:
                    	currentRow.counterValue = 0 #For unsupported counters the default value is 0
                    
                    currentRow.printRowDB()

                    #writer.writerow(line_counter[0:3])
                    #writer3.writerow(line_counter[0:3])
                   
                if re.search('seconds time elapsed',line):
                    

                    line = line.lstrip(' ')
                    line_time = line.split(" ")
                    
                    currentRow.socket = 'S4'
                    currentRow.counterName = line_time[1]
                    currentRow.counterValue = line_time[0]

                    currentRow.printRowDB()
                    #writer.writerow(line_time2)
                    





            

    else: 
    	print("Nothing to do")


