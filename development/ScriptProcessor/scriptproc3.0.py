# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "jofe"
__date__ = "$Jul 21, 2015 10:47:11 AM$"

import re
import csv
import os

if __name__ == "__main__":
    print("*** Welcome to scriptProcessor 3.0 ***")
    outputNumber=[]
    nameMasterFile=[]
    dbRow=[]
    #mac_path="/Users/Jofe/Dropbox/logProc3.0"
    path = os.getcwd()
    print("Path", path)
    pathLogs = path + "/GCAT/INPUT"
    inputLogs = path + "/GCAT/INPUT/"
    outputLogs = path + "/GCAT/CSV/" 
    outputNumber = os.listdir(pathLogs)
    print("Logs to be processed: ")
    print(outputNumber)
    if "Y"== input('Want to continue? [Y/N]'):
        
        for i in outputNumber:
            nameMasterFile=[]
            print("Processing log file number:", i)
            file = open(inputLogs+str(i),'r')
            nameFile = str(i).replace( ".log", "") 
            ofile  = open(outputLogs+nameFile+'.csv', "w")        
            writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer2 = csv.writer(ofile, delimiter=',' )  
            #Está claro que esto se podría hacer de una manera más inteligente si supiese usar RE.
            mapper = nameFile.split("_")  
            nameMasterFile.append(mapper[0])    


            #if re.match("bowtie2",nameFile):
                #mapper = re.match("bowtie2",nameFile)
            
            print("Mapper",mapper[0])
            print("Log Number", mapper[1])

            for arch in file:
            
                if re.match("batman", arch) or re.match("catwoman", arch) or re.match("penguin", arch):
                    print("Architecture", arch)
                    dbRow.append(mapper[1])
                    dbRow.append(arch)
                    dbRow.append(mapper[0])
                    #arch=str(arch).replace("\n","")
                    #nameMasterFile.append(arch)
                    break

            #nameMasterFile='_'.join(nameMasterFile)
            #print("NameMasterFile:", nameMasterFile)  
            #print("NameMasterFile:", '_'.join(nameMasterFile))
            #ofileMaster  = open(outputLogs+nameMasterFile+'.csv', "a") 
            #writer3 = csv.writer(ofileMaster, delimiter=';' )  
            
                       
            for line in file:        

                if re.match(" Performance counter stats for", line):
                    
                    
                    
                    threads = re.findall(r' [0-9]* ',line)
                    print ("Threads: ", threads)                    
                    dbRow.append(threads) 
                    line = line.lstrip(' ')
                    line_title = line.split(" ")
                    writer2.writerow(line_title)
                    #print("Title: ", line_title)
            
                if re.search('S[0-3]',line):    
                #print(line)
                    line_counter = line.split(" ")
                    line_counter = [x for x in line_counter if x != '']    #Crea un array con los elementos distinto a ''
                    line_counter = [x for x in line_counter if x != '16']  # Saca el elemento que sea igual a 16
                    line_counter[1], line_counter[2] = line_counter[2], line_counter[1]
                    dbRow.append(line_counter[0:3])
                    print("Line to save in DB:", dbRow)
                    dbRow=[]
                    writer.writerow(line_counter[0:3])
                    #writer3.writerow(line_counter[0:3])
                   
                if re.search('seconds time elapsed',line):
                    print ("seconds line: ", line)
                    line = line.lstrip(' ')
                    line_time = line.split(" ")
                    line_time2=[]
                    #Cambiar para el caso
                    line_time = [x for x in line_time if x != '']
                    line_time = [x for x in line_time if x != '(']
                    line_time = [x for x in line_time if x != ')']
                    line_time = [x for x in line_time if x != '+-']
                    #VER
                    line_time2.append(" ")
                    line_time2.append("seconds time elapsed")
                    line_time2.append(line_time[0])
                    line_time2.append(" ")
                    
                    #line_time2.append("std desviation")
                    #line_time2.append(line_time[4])
                    
                    
                    
                    
                    writer.writerow(line_time2)
                    #writer3.writerow(line_time2)
                
        ofile.close()                 
        print("File Processed")
    else:
        print("Invalid option - Nothing to do")
