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

def pop_vector(stack):
    """
    Return a vector from the stack.
    Also removes that return value from the stack.
    """
    if stack and isinstance(stack[-1], list):
        return stack.pop()

    result = []
    while stack and not isinstance(stack[-1], list):
        result.append(stack.pop())
    result.reverse()
    return result

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
    elif token == 'c':
        stack.append(len(pop_vector(stack[:])))
    elif token == 'd':
        stack.append(stack[-1])
    elif token == 'j':
        b = pop_vector(stack)
        a = pop_vector(stack)
        stack.append(a + b)
    elif token == 'm':
        stack.append(pop_vector(stack))
    elif token == 'r':
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    elif token == 's':
        stack.append(sum(pop_vector(stack)))
    elif token == 'p':
        stack = [reduce(operator.mul, pop_vector(stack) or [Fraction(1)])]
    elif token == 't':
        last = int(stack.pop())
        first = int(stack.pop() if stack else 0)
        stack.append(list(map(Fraction, range(first, last + 1))))
    elif token in unary:
        a = stack.pop()
        if isinstance(a, list):
            stack.append(list(map(unary[token], a)))
        else:
            stack.append(unary[token](a))
    elif token in binary:
        b = stack.pop()
        a = stack.pop() if stack else 0
        if isinstance(a, list):
            if isinstance(b, list):
                stack.append(list(map(binary[token], a, b)))
            else:
                stack.append([binary[token](each, b) for each in a])
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
