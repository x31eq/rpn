#!/usr/bin/env python3

import fractions, math, operator, re, sys
from functools import reduce

binary = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': pow,
        'l': math.log,
        }

unary = {'f': float, 'i': int, 'q': math.sqrt}

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
    elif token == 'r':
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    elif token == 's':
        stack = [sum(stack)]
    elif token == 'p':
        stack = [reduce(operator.mul, stack)]
    elif token in unary:
        stack.append(unary[token](stack.pop()))
    elif token in binary:
        b = stack.pop()
        if stack:
            stack.append(binary[token](stack.pop(), b))
        else:
            # Consistent with - as a unary operator
            stack.append(binary[token](0, b))
    else:
        raise SyntaxError("Bad token: " + token)

print(str(stack.pop()).replace('/', ':'))
