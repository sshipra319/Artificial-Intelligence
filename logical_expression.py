#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
from copy import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []



def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------
# Add all your functions here
#pl-true function check all connectives and,or,not,xor,if,iff

def pl_true(expression, model):
    if expression.connective[0].lower() == 'and':
        f = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                f = pl_true(subexpression, model)
                continue;
            f = f and pl_true(subexpression, model)
        return f
    elif expression.connective[0].lower() == 'not':
        f = not pl_true(expression.subexpressions[0], model)
        return f
    elif expression.connective[0].lower() == 'xor':
        f = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                f = pl_true(subexpression, model)
                continue;
            f = f ^ pl_true(subexpression, model)
        return f
    elif expression.connective[0].lower() == 'or':
        f = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                f = pl_true(subexpression, model)
                continue;
            f = f or pl_true(subexpression, model)
        return f

    elif expression.connective[0].lower() == 'if':
        exp1 = pl_true(expression.subexpressions[0], model)
        exp2 = pl_true(expression.subexpressions[1], model)
        return ( (not exp1) or exp2 )
    elif expression.connective[0].lower() == 'iff':
        exp1 = pl_true(expression.subexpressions[0], model)
        exp2 = pl_true(expression.subexpressions[1], model)
        return ( (not exp1) or exp2 ) and ( (not exp2) or exp1 )
    return model[expression.symbol[0]]

#tt-check-all function
def tt_check_all(kb, alpha, symbols, model):
    if not symbols:
        if pl_true(kb, model):
            return pl_true(alpha, model)
        else:
            return True
    p = symbols[0]
    rest = symbols[1:]
    return tt_check_all( kb, alpha, rest, extend(model, p, True) ) \
           and tt_check_all( kb, alpha, rest, extend(model, p, False) )


#to check symbols and statements with knowledge base
def tt_entails(K_B, statement, negation, symbolslist):
    
    try:
        output_file = open('result.txt', 'w')
    except:
        print('failed to create output file')
    k_b1 = []
    sym1 = []
    model = symbolslist.copy();
    read_symbols(K_B, k_b1)
    read_symbols(statement, sym1)
    k_b1 = list(set(k_b1))
    sym1 = list(set(sym1))
    k_b1.extend(sym1)
    symbols = list(set(k_b1))
    for symb in model.keys():
        try:
            symbols.remove(symb)
        except Exception:
            pass
    statem_true = tt_check_all(K_B, statement, symbols, model)
    statem_false = tt_check_all(K_B, negation, symbols, model)
    output_file = checkstatement(statem_true, statem_false, output_file)
    output_file.close()

# for reading  all the symbols in this function.
def read_symbols(expression, symbols):
    if expression.symbol[0]:
        symbols.append(expression.symbol[0])
    for subexpression in expression.subexpressions:
        read_symbols(subexpression, symbols)


def extend(model, symb, value):
    model[symb] = value
    return model

def checkstatement(statem_true, statem_false, output_file):
    if statem_true == True and statem_false == False:
        output_file.write('definitely true')
        print 'definitely true'
    elif statem_true == False and statem_false == False:
        output_file.write('possibly true, possibly false')
        print 'possibly true, possibly false'
    elif statem_true == False and statem_false == True:
        output_file.write('definitely false')
        print 'definitely false'
    elif statem_true == True and statem_false == True:
        output_file.write('both true and false')
        print 'both true and false'
    else:
        output_file.write('Error')
    print
    return output_file
