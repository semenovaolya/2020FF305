import pandas as pd
import re
import datetime
#читает файл по пути  и сохраняет DataFrame из него

class RenderFile():
    def __init__(self, path):
        self.filepath= path

    def file_to_dataframe(self):
        list=[]
        dataPattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s"
        timePattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2}\,\s'
        typePattern=r'(Info|Fatal|Warning|Error|Debug|Trace)\s{3,}'
        pat=dataPattern+timePattern+typePattern
        pat1=re.compile(dataPattern)
        pat2=re.compile(timePattern)
        pat3=re.compile(typePattern)
        with open(self.filepath, 'r') as file:
            for line in file:
                l=[]
                if (re.match(pat,line)):
                    r = pat1.findall(line)
                    l.append(str(r[0]))
                    c = pat2.findall(line)
                    l.append(c[0])
                    g = pat3.findall(line)
                    l.append(g[0])
                    line = re.sub(pat,'', line,re.IGNORECASE)
                    l.append(line)
                    list.append(l)

        dfLog = pd.DataFrame(list)
        dfLog.columns = ['Day', "Time", 'Type', 'Message']
        dfLog['Day'] = pd.to_datetime(dfLog['Day'])
        return dfLog

"""
    def file_to_dataframe(self):
        list = []
        timestampPattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}, "
        pattern = re.compile(timestampPattern)

        with open(self.filepath, 'r') as file:
            for line in file:
                if re.search(pattern, line):
                    res = line.split(" ", maxsplit=3)
                    res[-1] = res[-1].lstrip().rstrip("\n")
                    list.append(res)

        dfLog = pd.DataFrame(list)
        dfLog.columns = ['Day', "Time", 'Type', 'Message']
        dfLog['Day'] = pd.to_datetime(dfLog['Day'])
        return dfLog
"""


