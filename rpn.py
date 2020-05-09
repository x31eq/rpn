#!/usr/bin/env python3

import fractions, operator, re, sys

operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        }

tokens = re.findall(r'\d+|\S', ' '.join(sys.argv[1:]))

stack = []

for token in tokens:
    if re.match('\d+$', token):
        stack.append(fractions.Fraction(token))
    elif token in operations:
        b = stack.pop()
        stack.append(operations[token](stack.pop(), b))
    else:
        raise SyntaxError("Bad token: " + token)

result = stack.pop()

if result.denominator == 1:
    print(stack.pop())
else:
    print("{} {}/".format(result.numerator, result.denominator))
