# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "jofe"
__date__ = "$Jul 21, 2015 10:47:11 AM$"

import re
import csv
import os

if __name__ == "__main__":
    print "*** Welcome to scriptProcessor 3.0 ***"
    outputNumber=[]
    #mac_path="/Users/Jofe/Dropbox/logProc3.0"
    linux_path = "/home/jofe/Dropbox/logProc3.0"
    pathLogs = linux_path + "/GCAT/INPUT"
    inputLogs = linux_path + "/GCAT/INPUT/"
    outputLogs = linux_path + "/GCAT/CSV/" 
    outputNumber = os.listdir(pathLogs)
    arch=""
    print "Logs to be processed: "
    print outputNumber
    if "Y"== raw_input('Want to continue? [Y/N]'):
        
        for i in outputNumber:
            print "Processing log file number:", i
            file = open(inputLogs+str(i),'r')
            
            for line in file:
                if re.match("catwoman", line) or re.match("batman", line):
                    arch = "_" + "batcat"
                if re.match("penguin", line):
                    arch = "_" + "penguin"

                nameFile = str(i).replace( ".log", "") 
                ofile  = open(outputLogs+nameFile+arch+'.csv', "wb")        
                writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                writer2 = csv.writer(ofile, delimiter=',' )            

                if re.match(" Performance counter stats for", line):
                    line = line.lstrip(' ')
                    line_title = line.split(" ")
                    writer2.writerow(line_title)
                    #print "Title: ", line_title
            
                if re.search('S[0-3]',line):    
                #print line
                    line_counter = line.split(" ")
                    line_counter = [x for x in line_counter if x != '']    #Crea un array con los elementos distinto a ''
                    line_counter = [x for x in line_counter if x != '16']  # Saca el elemento que sea igual a 16
                    line_counter[1], line_counter[2] = line_counter[2], line_counter[1]
                    writer.writerow(line_counter[0:3])
                
                if re.search('seconds time elapsed',line):
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
                
        ofile.close()                 
        print "File Processed"
    else:
        print "Invalid option - Nothing to do"
