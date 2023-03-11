import re
import json

header = r'(\w+)(?:{(?:(\d+)|(\d+),(\d+))}(?:::(\w+))?)?'

class Header:
    def __init__(self, name, num, min, max, agg):
        self.name = name
        self.list = num or min or max
        
        if self.list:
            self.min = int(num if num else min)
            self.max = int(num if num else max)
            self.aggregate_name = "_" + agg if agg else ""
            self.aggregate = {"sum": sum, \
                              "media": lambda l: sum (l) / len(l), \
                              "": lambda x: x \
                             }[agg]
            
    def process(self, cell_iterator):       
        if self.list:
            aux = []
            
            for _ in range(0, self.min):
                aux.append(int(next(cell_iterator)))
                
            for _ in range(self.min, self.max):
                val = next(cell_iterator)
                if val != "":
                    aux.append(int(val))
            
            return {self.name + self.aggregate_name: self.aggregate(aux)}
        else:
            return {self.name: next(cell_iterator)}

f = open("input.txt", "r")
headers = list(map(lambda m: Header(*m), re.findall(header, f.readline())))

def parseLine(line):
    cells = iter(line.split(','))
    ans = {}
    for h in headers:
        ans.update(h.process(cells))
    return ans

entries = list(map(parseLine, f.read().split('\n')))
f.close()

f = open("output.txt", "w")
json.dump(entries, f, indent=4, ensure_ascii=False)
f.close()
