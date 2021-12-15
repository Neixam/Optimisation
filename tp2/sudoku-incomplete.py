#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sudoku"""

def var(i,j,k):
    """Return the literal Xijk.
    """
    return (1,i,j,k)

def neg(l):
    """Return the negation of the literal l.
    """
    (s,i,j,k) = l
    return (-s,i,j,k)

def initial_configuration():
    """Return the initial configuration of the example in td6.pdf
    
    >>> cnf = initial_configuration()
    >>> (1, 1, 4, 4) in cnf
    True
    >>> (1, 2, 1, 2) in cnf
    True
    >>> (1, 2, 3, 1) in cnf
    False
    """
    return [var(1,4,4), var(2,1,2), var(3,2,1), var(4,3,1)]

def at_least_one(L):
    """Return a cnf that represents the constraint: at least one of the
    literals in the list L is true.
    
    >>> lst = [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    >>> cnf = at_least_one(lst)
    >>> len(cnf)
    1
    >>> clause = cnf[0]
    >>> len(clause)
    3
    >>> clause.sort()
    >>> clause == [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    True
    """
    return [L]

import itertools

def at_most_one(L):
    """Return a cnf that represents the constraint: at most one of the
    literals in the list L is true
    
    >>> lst = [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    >>> cnf = at_most_one(lst)
    >>> len(cnf)
    3
    >>> cnf[0].sort()
    >>> cnf[1].sort()
    >>> cnf[2].sort()
    >>> cnf.sort()
    >>> cnf == [[neg(var(1,1,1)), neg(var(2,2,2))], \
    [neg(var(1,1,1)), neg(var(3,3,3))], \
    [neg(var(2,2,2)), neg(var(3,3,3))]]
    True
    """
    return [[neg(x), neg(y)] for x, y in itertools.combinations(L, 2)]

def assignment_rules(N):
	"""Return a list of clauses describing the rules for the assignment (i,j) -> k.
	>>> cnf = assignment_rules(4)
	>>> len(cnf)
	112
	"""
	cnf = []
	for i in range(1,N+1):
		for j in range(1,N+1):
			clause = [var(i,j,k) for k in range(1, N+1)]
			cnf += list(at_least_one(clause)) + list(at_most_one(clause))
	return cnf

def row_rules(N):
	"""Return a list of clauses describing the rules for the rows.
	>>> len(row_rules(4))
	112
	"""
	cnf = []
	for i in range(1, N+1):
		for k in range(1, N+1):
			clause = [var(i, j, k) for j in range(1, N+1)]
			cnf.extend(at_least_one(clause) + at_most_one(clause))
	return cnf

def column_rules(N):
	"""Return a list of clauses describing the rules for the columns.
	"""
	cnf = []
	for j in range(1, N+1):
		for k in range(1, N+1):
			clause = [var(i, j, k) for i in range(1, N+1)]
			cnf += list(at_least_one(clause)) + list(at_most_one(clause))
	return cnf

from math import sqrt

def subgrid_rules(N):
	"""Return a list of clauses describing the rules for the subgrids.
	>>> len(subgrid_rules(4))
	112
	"""
	cnf = []
	sqn = int(sqrt(N))
	for lala in range(0, N, sqn) :
		for lolo in range(0, N, sqn) :
			for k in range(1, N + 1) :
				clause = []
				for i in range(1, sqn + 1) :
					clause += [var(lala + i, lolo + j, k) for j in range(1, sqn + 1)]
				cnf.extend(at_least_one(clause) + at_most_one(clause))
	return cnf

def generate_rules(N):
    """Return a list of clauses describing the rules of the game.
    """
    cnf = []    
    cnf.extend(assignment_rules(N))
    cnf.extend(row_rules(N))
    cnf.extend(column_rules(N))
    cnf.extend(subgrid_rules(N))
    return cnf

def literal_to_integer(l, N):
	"""Return the external representation of the literal l.

    >>> literal_to_integer(var(1,2,3), 4)
    7
    >>> literal_to_integer(neg(var(3,2,1)), 4)
    -37
	"""
	(v,i,j,k) = l
	return v * (N**2 * (i - 1) + (j - 1) * N + k)

def to_cnf(rules, N) :
	with open("output.cnf", "w") as f :
		f.write("p cnf " + str(N**3) + " " + str(len(rules)) + "\n")
		for clause in rules :
			f.write(" ".join([str(literal_to_integer(var, N)) for var in clause]) + " 0\n")

def main():
	import doctest
	to_cnf(generate_rules(4) + [at_least_one(j) for j in initial_configuration()], 4)
	doctest.testmod()

if __name__ == "__main__":
    main()
