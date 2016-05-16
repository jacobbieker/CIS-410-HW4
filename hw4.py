__author__ = 'Theodore LaGrow'
__author__ = 'Jacob Bieker'
# CIS 410/510pm
# Homework #4
# Daniel Lowd
# April 2016
#
# Worked with Robert Marcy on the implimentation of the alogithm and logic behind __mult__
#
#
#
# TEMPLATE CODE
import sys
import functools
import tokenize


#
# FACTOR CLASS -- EDIT HERE!
#

class Factor(dict):
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

            # print("stride: ", s  # Used for testing code

    def __mul__(self, other):

        new_scope = []
        for t in self.scope:
            new_scope.append(t)
        for s in other.scope:
            if s not in self.scope:
                new_scope.append(s)
        print("new_scope", new_scope)

        new_ranges = {}
        for i in new_scope:
            # print(i #
            # print("self.scope: ", self.scope #
            if (i in self.scope):

                print("self.ranges: ", self.ranges)  #
                # print(i #
                new_ranges[i] = self.ranges[i]
            elif (i in other.scope):
                # print(i #
                new_ranges[i] = other.ranges[i]

        print("new_range: ", new_ranges)

        x1Ux2_scope = len(new_scope)
        print("x1Ux2_scope", x1Ux2_scope)

        x1Ux2_cardinality_values = 1
        for key in new_ranges:
            x1Ux2_cardinality_values *= new_ranges[key]
        print("x1Ux2_cardinality_values", x1Ux2_cardinality_values)

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


        # print(psi_values # testing

        psi_values.append(self.vals[j] * other.vals[k])
        new_scope.reverse()
        # END PLACEHOLDER CODE
        return Factor(new_scope, psi_values, new_ranges)  # Line 16

    def __rmul__(self, other):  # never used
        return self * other

    def __imul__(self, other):  # never used
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
        # print("Num tokens:",len(token_buf)


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

    ###########
    # Get variable for the factor scopes

    var_dict = dict(zip(range(num_vars), var_ranges))
    factor_ranges = []
    for k in range(num_factors):
        factor_ranges.append({j: var_dict[j] for j in factor_scopes[k]})



    # DEBUG
    print("Num vars: ", num_vars)
    print("Ranges: ", var_ranges)
    print("var_dict: ", var_dict)
    print("factor_ranges: ", factor_ranges)
    print("Scopes: ", factor_scopes)
    print("Values: ", factor_vals)
    return [Factor(s, v, r) for (s, v, r) in zip(factor_scopes, factor_vals, factor_ranges)]


#
# MAIN PROGRAM
#

def main():
    factors = read_model()
    for f in factors:
        print(f.ranges)
        print(f.scope)
    # Compute Z by brute force
    f = functools.reduce(Factor.__mul__, factors)
    # f = Factor.__mul__(factors[0], factors[1])
    print("values of f: ", f.values)
    print("scope of f: ", f.scope)
    z = sum(f.vals)
    print("Z = ", z)
    return


main()
