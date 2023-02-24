import sys
import re

pattern = re.compile(r'On|Off|\d+|=')

on = True
sum = 0

for line in sys.stdin:
    for m in re.finditer(pattern, line):
        if m.group() == 'On':
            on = True
        elif m.group() == 'Off':
            on = False
        elif m.group() == '=':
            print(sum)
        elif on:
            sum += int(m.group())