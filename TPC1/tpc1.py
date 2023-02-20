def merge(list1, list2):
    i = 0
    j = 0
    
    while (i < len(list1) and j < len(list2)):
        if list1[i] < list2[j]:
            yield list1[i]
            i += 1
        elif list1[i] > list2[j]:
            yield list2[j]
            j += 1
        else:
            yield list1[i]
            i += 1
            j += 1
            
    for x in range(i, len(list1)):
        yield list1[x]
        
    for x in range(j, len(list2)):
        yield list2[x]

class Selector:
    def __init__(self, condition, name):
        self.condition = condition
        self.name = name
        
    def selects(self, e):
        return self.condition(e)
    
class EqSelector(Selector):
    def __init__(self, value):
        super().__init__(lambda e: e == value, str(value))
        
class RangeSelector(Selector):
    def __init__(self, min, max):
        super().__init__(lambda e: e >= min and e <= max, str(min) + "-" + str(max))

class TotalSelector(Selector):
    def __init__(self):
        super().__init__(lambda e: True, "Total")


class Splitter:
    def __init__(self, column):
        #TODO: validate
        self.column = column

    def __getElem__(self, line, headers):
        if isinstance(self.column, int):
            return line[self.column]
        if isinstance(self.column, str):
            return line[headers.index(self.column)]
        raise TypeError("Invalid splitter")

    def splitLines(self, lines, headers):
        pass

class SelectorSplitter(Splitter):
    def __init__(self, column, selectors):
        super().__init__(column)
        self.selectors = selectors
    
    def splitLines(self, lines, headers):
        return [(s.name, [l for l in lines if s.selects(self.__getElem__(l, headers))]) for s in self.selectors]
    
class StepSplitter(Splitter):
    def __init__(self, column, step, start = None, stop = None):
        super().__init__(column)    
        #TODO: validate
        self.step = step
        self.start = start
        self.stop = stop
    
    def splitLines(self, lines, headers):
        buckets = {}
        
        for l in lines:
            i = self.__getElem__(l, headers) // self.step
            if (i not in buckets):
                buckets[i] = []
            buckets[i].append(l)

        start = min(buckets) if self.start is None else self.start // self.step
        stop = max(buckets) + 1 if self.stop is None else self.stop // self.step
        
        return [(f"{i * self.step}-{(i + 1) * self.step - 1}", \
                 buckets[i] if i in buckets else []) for i in range(start, stop)]

class Table:
    def __init__(self, headers, lines = []):
        #TODO: validation
        self.headers = headers
        self.lines = lines

    def printStat(self, splitter):
        split = splitter.splitLines(self.lines, self.headers)
        print("\t|".join([h for h,_ in split]))
        print("\t|".join([str(sum(1 for _ in l)) for _,l in split]))
        print()
    
    def printRelation(self, column_splitter, line_splitter):
        aux_split = column_splitter.splitLines(self.lines, self.headers)
        split = [[(h,str(sum(1 for _ in s))) for h,s in line_splitter.splitLines(lines, self.headers)] for _,lines in aux_split]
        
        column_headers = [h for h,_ in aux_split]
        line_headers = []
        for column in split:
            line_headers = list(merge(line_headers, [h for h,_ in column]))
        
        relation = [(header, [next((v for h,v in c if h == header), "0") for c in split]) for header in line_headers]

        #print([(h,list(v)) for h,v in relation])
        print("\t|" + "\t|".join(column_headers))
        for name, line in relation:
            print(name + "\t|" + "\t|".join(line))
        print()

def parse(filename, types):
    file = open(filename, "r")
    lines = list(filter(None,file.read().split("\n")))
    file.close()
    
    headers = lines[0].split(",")
    table_lines = [[t(e) for e,t in zip(line.split(","), types)] for line in lines[1:]]
    return Table(headers, table_lines)


table = parse("myheart.csv", [int,str,int,int,int,int])
doencaSplitter = SelectorSplitter("temDoença",[EqSelector(1),EqSelector(0),TotalSelector()])

#table.printStat(Splitter("sexo",[EqSelector("M"),EqSelector("F"),TotalSelector()]))
table.printRelation(doencaSplitter,SelectorSplitter("sexo",[EqSelector("M"),EqSelector("F"),TotalSelector()]))
table.printRelation(doencaSplitter,StepSplitter("idade",5))
table.printRelation(doencaSplitter,StepSplitter("colesterol",10))