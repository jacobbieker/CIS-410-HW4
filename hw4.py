__author__ = 'jacob'
# CIS 410/510pm
# Homework #4
# Daniel Lowd
# April 2016
#
# TEMPLATE CODE
import sys
import tokenize


#
# FACTOR CLASS -- EDIT HERE!
#

class Factor(dict):
    def __init__(self, scope_, vals_, range_,):
        self.scope = scope_
        self.vals = vals_
        self.ranges = range_

    def __mul__(self, other):

        # BEGIN PLACEHOLDER CODE -- DELETE THIS!
        new_vals = []
        for value in self.vals:
            for value2 in other.vals:
                new_vals.append(value * value2)
        new_scope = self.scope + other.scope
        new_range = self.ranges
        print "Factor Scope: ", new_scope
        print "Factor val: ", new_vals
        print "Factor range: ", new_range

        # Go through table and multiply
        # END PLACEHOLDER CODE
        return Factor(new_scope, new_vals, new_range)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other


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
    ranges_list = []
    for i in range(num_factors):
        ranges_list.append(var_ranges)

    factor_scopes = []
    for i in range(num_factors):
        factor_scopes.append([next_int() for i in range(next_int())])

    # Read in all factor values
    factor_vals = []
    for i in range(num_factors):
        factor_vals.append([next_float() for i in range(next_int())])

    # DEBUG
    print "Num vars: ",num_vars
    print "Ranges: ",ranges_list
    print "Scopes: ",factor_scopes
    print "Values: ",factor_vals
    print "Factor zip", zip(factor_scopes, factor_vals, var_ranges)
    return [Factor(s, v, r) for (s, v, r) in zip(factor_scopes, factor_vals, ranges_list)]


#
# MAIN PROGRAM
#

def main():
    factors = read_model()
    print factors
    # Compute Z by brute force
    f = reduce(Factor.__mul__, factors)
    z = sum(f.vals)
    print("Z = ", z)
    return


main()
