import shutil     
import os
import sys
import math
import itertools
def openfile(filename):
    with open(filename) as file_:
        for i in file_:
            yield i.strip()
 
 
def file_split(filename, parts):
    
  
   
    all_str = sum(1 for i in open(filename, 'r'))  
    count = math.ceil(all_str / parts)  
    offset = 0
    chunks = []  
    for i in range(parts):
        file_ = openfile(filename)
        chunks.append((itertools.islice(file_, offset, offset + count)))
        offset += count
 
    return chunks
 
 
def write_chunks(filename, chunks):
    for index, data in enumerate(chunks):
        with open('{}-{}.txt'.format(filename, index), 'w') as out:
            list(map(lambda line: out.write('{}\n'.format(line)), data))
 
 
target = ['log.txt']
for i in target:
    chunks = file_split(i, 5)
    write_chunks(i, chunks)

if(len(sys.argv) < 4):    
  print('Missing arguments!')
  exit(1)
                          
                          
file_name  = sys.argv[1]       
limitsize  = int(sys.argv[2])  
logsnumber = int(sys.argv[3]) 

if(os.path.isfile(file_name) == True):        
    logfile_size = os.stat(file_name).st_size 
    logfile_size = logfile_size / 1024

    if(logfile_size >= limitsize):
       if(logsnumber > 0):
          for currentFileNum in range(logsnumber, 1, -1):
             src = file_name + "_" + str(currentFileNum-1)    
             dst = file_name + "_" + str(currentFileNum)
             if(os.path.isfile(src) == True):          
                shutil.copyfile(src, dst)                      
                print("Copied " + src + " to " + dst)
          shutil.copyfile(file_name, file_name + "_1")
          print("Copied: " + file_name + "  to " + file_name + "_1")

       myfile = open(file_name, 'w')
       myfile.close()     