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
        print
        print "Other Scope: ", other.scope
        print "Other Ranges: ", other.ranges
        print "Other Vals: ", other.vals
        print

        j = 0
        k = 0
        assignment = {}
        new_factors = []

        for l in self.scope:
            assignment[l] = 0
        for l in other.scope:
            assignment[l] = 0
        print assignment

        for i in range(len(self.ranges) * len(other.ranges) - 1):
            new_factors.append(self.vals[j] * other.vals[k])
            # for l = 0, ..., self.scope union other.scope
                assignment[l] = assignment[l] + 1
                if assignment[l] == self.ranges[l]:
                    assignment[l] = 0
                    # Loops back around to top is idea, mighjt not work
                    j = j - (self.ranges[l] - 1) * self.vals[l]
                    k = k - (other.ranges[l] - 1) * other.vals[l]
                elif assignment[l] == other.ranges[l]:
                    assignment[l] = 0
                    j = j - (self.ranges[l] - 1) * self.vals[l]
                    k = k - (other.ranges[l] - 1) * other.vals[l]
                else:
                    j = j + self.ranges[]


        """
        lengths_scopes = []
        for index, value in enumerate(other.scope):
            print index
            print value
            #lengths_scopes.append(value * self.ranges[index])
        #print "lengths_scopes: ", lengths_scopes
        new_vals = []
        for index, value in enumerate(other.vals):
            for index2, value2 in enumerate(other.vals):
                #print index2
                #print value2
                print ""
        """
        new_scope = self.scope
        for scope in other.scope:
            if scope not in self.scope:
                new_scope.append(scope)

        new_scope.reverse()
        new_vals = self.vals
        new_range = self.ranges
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
    #print "Num vars: ",num_vars
    #print "Ranges: ",ranges_list
    #print "Scopes: ",factor_scopes
    #print "Values: ",factor_vals
    #print "Factor zip", zip(factor_scopes, factor_vals, var_ranges)
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
