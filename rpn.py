#!/usr/bin/env python3

import math, operator, re, sys
from fractions import Fraction
from functools import reduce

def percent(n, d):
    return float(n) / float(d) * 1e2

binary = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': pow,
        'l': math.log,
        '%': percent,
        }

unary = {'f': float, 'i': int, 'q': math.sqrt, 'v': math.sqrt}

tokens = re.findall(r'[\d.:box]+|\S', ' '.join(sys.argv[1:]))

stack = []

for token in tokens:
    if re.match(r'(0[box])?\d+$', token):
        stack.append(Fraction(int(token, base=0)))
    elif re.match(r'\d+:\d+$', token):
        n, d = token.split(':')
        stack.append(Fraction(int(n), int(d)))
    elif re.match(r'\d+.\d*$', token):
        stack.append(float(token))
    elif token == 'd':
        stack.append(stack[-1])
    elif token == 'm':
        m = []
        while stack and  not isinstance(stack[-1], list):
            m.append(stack.pop())
        m.reverse()
        stack.append(m)
    elif token == 'r':
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    elif token == 's':
        if stack and isinstance(stack[-1], list):
            stack.append(sum(stack.pop()))
        else:
            stack = [sum(stack)]
    elif token == 'p':
        if stack and isinstance(stack[-1], list):
            stack.append(reduce(operator.mul, stack.pop()))
        else:
            stack = [reduce(operator.mul, stack or [Fraction(1)])]
    elif token == 't':
        last = int(stack.pop())
        first = int(stack.pop())
        for i in range(first, last + 1):
            stack.append(Fraction(i))
    elif token in unary:
        a = stack.pop()
        if isinstance(a, list):
            for each in a:
                stack.append(unary[token](each))
        else:
            stack.append(unary[token](a))
    elif token in binary:
        b = stack.pop()
        a = stack.pop() if stack else 0
        if isinstance(a, list):
            if isinstance(b, list):
                for each in map(binary[token], a, b):
                    stack.append(each)
            else:
                for each in a:
                    stack.append(binary[token](each, b))
        else:
            stack.append(binary[token](a, b))
    else:
        raise SyntaxError("Bad token: " + token)

if stack:
    result = stack.pop()
    if isinstance(result, list):
        print(' '.join(str(item).replace('/', ':') for item in result))
    else:
        print(str(result).replace('/', ':'))
