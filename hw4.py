__author__ = 'Theodore LaGrow'
__author__ = 'Jacob Bieker'
# CIS 410/510
# Homework #4
# Daniel Lowd
# April 2016
#
# Language: Python 3.5x
#
# Notes from HW4:
# Worked with Robert Marcy on the implimentation of the alogithm and logic behind __mult__
#
# Notes from HW5:
# (these are the notes)
#
# TEMPLATE CODE
import sys
import tokenize
import functools
from collections import Counter

#
# FACTOR CLASS
#

class Factor(dict):
    """
    Ranges = cardinality
    vals = phi
    scope =
    """
    def __init__(self, scope_, vals_, range_):
        self.scope = scope_
        self.vals = vals_
        self.ranges = range_

    def stride(self, l):
        """ Used to calculate the stride of each variable """
        if l not in self.scope:
            return 0
        s = 1
        self.scope.reverse()  # Needs to reverse the elements to iterate cleaner
        for i in self.scope:
            if (i == l):
                self.scope.reverse()  # Reverse back
                return s
            s *= self.ranges[i]

            # print "stride: ", s  # testing

    def __mul__(self, other):
        """ Method to brute force the multiplication """
        """ WARNING: do not try to impliment this function on alarm... """

        new_scope = []
        for scope in self.scope:
            new_scope.append(scope)
        for scope in other.scope:
            if scope not in self.scope:
                new_scope.append(scope)
        # print "new_scope", new_scope


        new_ranges = {}
        for i in new_scope:
            if (i in self.scope):
                # print "self.ranges: ", self.ranges # testing
                new_ranges[i] = self.ranges[i]
            elif (i in other.scope):
                new_ranges[i] = other.ranges[i]


        # print "new_range: ", new_ranges # testing




        x1Ux2_scope = len(new_scope)
        # print "x1Ux2_scope", x1Ux2_scope # testing

        x1Ux2_cardinality_values = 1
        for key in new_ranges:
            x1Ux2_cardinality_values *= new_ranges[key]
        # print "x1Ux2_cardinality_values", x1Ux2_cardinality_values # testing


        """ This is the start the implimentation of Alogithm 10.A.1 on pg. 359 """

        j, k = 0, 0  # Line 1
        assignment = []
        psi_values = []

        for l in range(x1Ux2_scope):  # Line 2
            assignment.append(0)  # Line 3

        for i in range(x1Ux2_cardinality_values - 1):  # Line 4
            psi_values.append(self.vals[j] * other.vals[k])  # Line 5

            for l in new_scope:  # Line 6 (modified from the actual algoithem)

                assignment[new_scope.index(l)] += 1  # Line 7

                if assignment[new_scope.index(l)] == new_ranges[l]:  # Line 8
                    assignment[new_scope.index(l)] = 0  # Line 9

                    j = j - (new_ranges[l] - 1) * Factor.stride(self, l)  # Line 10
                    k = k - (new_ranges[l] - 1) * Factor.stride(other, l)  # Line 11

                else:  # Line 12
                    j = j + Factor.stride(self, l)  # Line 13
                    k = k + Factor.stride(other, l)  # Lin3 14
                    break  # Line 15


        # print psi_values # testing

        psi_values.append(self.vals[j] * other.vals[k])
        new_scope.reverse()
        # END PLACEHOLDER CODE
        return Factor(new_scope, psi_values, new_ranges)  # Line 16

    def __rmul__(self, other):  # never used
        return self * other

    def __imul__(self, other):  # never used
        return self * other


def sum_out(factor, variable):
    '''
    Choose a random variable from all of the remaining variables that can be summed out
    Collect all the factors that have this random variable and multiply them together
    Sum out the chosen random variable from the resulting factor by summing all the variations of the chosen random
    variable for each combination of other random variables
    Repeat
    :param factor:
    :param variable:
    :return:
    '''
    debug = True

    new_vals = [x for x in factor.scope if variable not in x]
    if debug: print("New Vals: ", new_vals)

    new_factor = Factor(new_vals, factor.vals, factor.ranges)

    if len(new_vals) > 0:
        val_index = factor.scope.index(variable)
        if debug: print("Var Index: ", val_index)

        used_val = [False for x in range(len(factor.scope))]

        if debug:
            print("used var: ", used_val)
            print("stride: ", factor.stride(factor.scope[val_index]), ", card: ", factor.vals[val_index])

        psi = []
        for i in range(len(new_factor.scope)):
            psi.append(0)

            start = 0
            for k in range(len(factor.scope)):
                if used_val[k] == False:
                    start = k
                    break

            for j in range(len(factor.scope[val_index])):
                if debug:
                    print("start: ", start, " stride: ", factor.stride(val_index), " j: ", j)
                psi[i] += factor.vals[start + factor.stride(val_index) * j]
                used_val[start + factor.stride(val_index) * j] = True

            if debug:
                print("psi: ", i, " ", psi[i])

        new_factor.vals = psi[:]

    return new_factor


#
# READ IN MODEL FILE
#

# Read in all tokens from stdin.  Save it to a (global) buf that we use
# later.  (Is there a better way to do this? Almost certainly.)
curr_token = 0
token_buf = []


def read_tokens():
    global token_buf
    for line in sys.stdin:
        token_buf.extend(line.strip().split())
        # print "Num tokens:",len(token_buf)


def next_token():
    global curr_token
    global token_buf
    curr_token += 1
    return token_buf[curr_token - 1]


def next_int():
    return int(next_token())


def next_float():
    return float(next_token())


def read_model():
    # Read in all tokens and throw away the first (expected to be "MARKOV")
    read_tokens()
    s = next_token()

    # Get number of vars, followed by their ranges
    num_vars = next_int()
    var_ranges = [next_int() for i in range(num_vars)]

    # Get number and scopes of factors
    num_factors = int(next_token())
    factor_scopes = []
    for i in range(num_factors):
        factor_scopes.append([next_int() for i in range(next_int())])

    # Read in all factor values
    factor_vals = []
    for i in range(num_factors):
        factor_vals.append([next_float() for i in range(next_int())])

    ####################################################################
    # Get variable for the factor scopes
    # This is needed to get the ranges in the correct format

    var_dict = dict(zip(range(num_vars), var_ranges))
    factor_ranges = []
    for k in range(num_factors):
        factor_ranges.append({j: var_dict[j] for j in factor_scopes[k]})

    ####################################################################


    # Hella DEBUGing
    # print "Num vars: ",num_vars
    # print "Ranges: ",var_ranges
    # print "var_dict: ", var_dict
    # print "factor_ranges: ", factor_ranges
    print("Scopes: ", factor_scopes)
    # print "Values: ",factor_vals
    return [Factor(s, v, r) for (s, v, r) in zip(factor_scopes, factor_vals, factor_ranges)]


#
# MAIN PROGRAM
#

def main():
    factors = read_model()
    # loop through factors, choosing random variable to sum out and sending those factors to sum_out
    total_scope = []
    for factor in factors:
        total_scope.append(factor.scope)
    print(total_scope)
    # Compute Z by brute force... BRUUUUTTTTEEEEEEE
    f = functools.reduce(Factor.__mul__, factors)  # Nice function in Python! Whoot whoot!
    z = sum(f.vals)
    print("Z = ", z)
    return


main()
