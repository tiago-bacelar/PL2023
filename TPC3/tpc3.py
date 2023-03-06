import re
import json

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Name):
            return o.toJSON()
        return o.__dict__

nome = re.compile(r'([A-Z][a-z]*)( [A-Z][a-z]*)* ([A-Z][a-z]*)')
data = re.compile(r'(\d+)-(\d+)-(\d+)')
relacao = re.compile(r'irmao|primo|sobrinho|tio(?! avo)|tio avo')

class Name:
    def __init__(self, fullname):
        self.fullName = fullname
        m = re.match(nome, fullname)
        
        if m is None:
            self.firstName = None
            self.lastName = None
        else:
            self.firstName = m.group(1)
            self.lastName = m.group(3)
            
    def toJSON(self):
        return self.fullName

class Entry:
    def __init__(self, line):
        parts = line.split("::")
        
        self.no = int(parts[0])
        
        m = re.match(data, parts[1])
        self.year = int(m.group(1))
        self.month = int(m.group(2))
        self.day = int(m.group(3))
        
        self.name = Name(parts[2])
        self.father = Name(parts[3])
        self.mother = Name(parts[4])
        
        self.notes = parts[5]
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def parse(filename):
    f = open(filename, "r")
    ans = list(map(Entry, filter(None, f.read().split('\n'))))
    f.close()
    return ans

def writeJson(vals, filename):
    f = open(filename, "w")
    json.dump(vals, f, indent=4, cls=MyEncoder)
    f.close()

def frequency(entries, getValues):
    ans = {}
    for e in entries:
        vals = getValues(e)
        for val in vals:
            if val is not None:
                if val in ans:
                    ans[val] += 1
                else:
                    ans[val] = 1
    return sorted(ans.items())

def sortByFreq(freq):
    return sorted(freq, key=lambda kv: -kv[1])

def printFreq(freq):
    for k,v in freq:
        if len(str(k)) < 8:
            print(f"{k}\t\t| {v}")
        else:
            print(f"{k}\t| {v}")
    print()

processos = parse("processos.txt")
printFreq(frequency(processos, lambda e: [e.year]))
printFreq(sortByFreq(frequency(processos, lambda e: [e.name.firstName, e.father.firstName, e.mother.firstName]))[:5])
printFreq(sortByFreq(frequency(processos, lambda e: [e.name.lastName, e.father.lastName, e.mother.lastName]))[:5])
printFreq(frequency(processos, lambda e: re.findall(relacao, e.notes.lower())))
writeJson(processos[:20], "out.json")