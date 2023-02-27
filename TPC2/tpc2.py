import sys
           
def suffixes(list):
    return [list[i:] for i in range(0, len(list))]    

def digits(input):
    i = 0
    while input[i] >= '0' and input[i] <= '9':
        i += 1
    return i

def match_len(input, word):
    input = input.lower()
    word = word.lower()
    
    if word == '\\d+':
        return digits(input)
    elif input.startswith(word):
        return len(word)
    else:
        return 0
 
def get_matches(input, *words):
    pos = 0
    while pos < len(input):
        suffix = input[pos:]
        pos += 1
        
        for i, word in enumerate(words):
            aux = match_len(suffix, word)
            if aux != 0:
                yield (i, suffix[:aux])
                pos += aux - 1
                break

on = True
sum = 0

for line in sys.stdin:
    for i, m in get_matches(line, 'On', 'Off', '\\d+', '='):
        if i == 0:
            on = True
        elif i == 1:
            on = False
        elif i == 2 and on:
            sum += int(m)
        elif i == 3:
            print(sum)