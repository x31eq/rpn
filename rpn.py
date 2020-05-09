#!/usr/bin/env python3

import fractions, operator, re, sys

operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        }

tokens = re.findall(r'[\d:]+|\S', ' '.join(sys.argv[1:]))

stack = []

for token in tokens:
    if re.match('\d+$', token):
        stack.append(fractions.Fraction(token))
    elif re.match('\d+:\d+$', token):
        n, d = token.split(':')
        stack.append(fractions.Fraction(int(n), int(d)))
    elif token == 'd':
        stack.append(stack[-1])
    elif token == 'r':
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    elif token in operations:
        b = stack.pop()
        stack.append(operations[token](stack.pop(), b))
    elif token == 's':
        stack = [sum(stack)]
    else:
        raise SyntaxError("Bad token: " + token)

print(str(stack.pop()).replace('/', ':'))
