import re
import itertools
import functools
import operator
import dataclasses
import math

def product(vals):
    return functools.reduce(operator.mul, vals, 1)

example = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

example = open('15.txt').read().strip()

def HASH(string: str) -> int:
    value = 0
    for c in string:
        value = ((value + ord(c)) * 17) % 256
    return value

def HASHMAP(string):
    boxes = [{} for _ in range(256)]
    for part in string.split(','):
        label, focal = re.split('[-=]', part)
        boxno = HASH(label)

        if '-' in part and label in boxes[boxno]:
            del boxes[boxno][label]
        elif '=' in part:
            boxes[boxno][label] = int(focal)
    
    return boxes


print(sum(HASH(part) for part in example.split(',')))
print(sum(
    boxno * slotno * fl 
    for boxno, contents in enumerate(HASHMAP(example), 1)
    for slotno, (label, fl) in enumerate(contents.items(), 1)
))