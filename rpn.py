#!/usr/bin/env python3

import fractions, operator, re, sys
from functools import reduce

operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': pow,
        }

tokens = re.findall(r'[\d.:]+|\S', ' '.join(sys.argv[1:]))

stack = []

for token in tokens:
    if re.match('\d+$', token):
        stack.append(fractions.Fraction(token))
    elif re.match('\d+:\d+$', token):
        n, d = token.split(':')
        stack.append(fractions.Fraction(int(n), int(d)))
    elif re.match('\d+.\d*$', token):
        stack.append(float(token))
    elif token == 'd':
        stack.append(stack[-1])
    elif token == 'f':
        stack.append(float(stack.pop()))
    elif token == 'r':
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    elif token in operations:
        b = stack.pop()
        if stack:
            stack.append(operations[token](stack.pop(), b))
        else:
            # Consistent with - as a unary operator
            stack.append(operations[token](0, b))
    elif token == 's':
        stack = [sum(stack)]
    elif token == 'p':
        stack = [reduce(operator.mul, stack)]
    else:
        raise SyntaxError("Bad token: " + token)

print(str(stack.pop()).replace('/', ':'))
