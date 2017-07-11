__author__ = "jofe"
__date__ = "$Jul 21, 2015 10:47:11 AM$"

import re
import csv
import os
import glob

if __name__ == "__main__":
    print ("*** Welcome to Instances Averager 1.0 ***")
   
    
    mappers = ['GEM', 'BOWTIE2', 'SNAP', 'MEM' ]
    archs = ['catwoman','penguin','batman' ]
    path = os.getcwd()
    pathLogs = path + "/GCAT/CSV/merge_test/"
    test2 = list()
    #ofile  = open('output/'+str(i)+'.csv', "wb")
    #writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
    #writer2 = csv.writer(ofile, delimiter=',' )
    #init_counters()
    
    #for mapper in mappers:
        #print "Counters for: ", mapper
    #for arch in archs:
    #    print "Arch: ", arch
    
    #iterations=10
    #for i in range(1,iterations):
    name='*.csv'
    listFiles=glob.glob(os.path.join(pathLogs, name))
    #print "List of Files", listFiles
    

    if listFiles:
        
        filename=iter(listFiles)
        test=next(filename)
        
        with open(test, 'r') as f:
            reader1 = csv.reader(f, delimiter=';')

            #print ("Filename", test)
            #t1=list(reader1)
        
            for row in reader1:
                print("row," ,row))
                


            
             
                        
                           
                            
                        

                #break
            #break
        #break
                    
