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
    def __init__(self, scope_, vals_, range_):
        self.scope = scope_
        self.vals = vals_
        self.ranges = range_



    def stride(self, l):
        
        if l not in self.scope:
            return 0
        s = 1
        self.scope.reverse()
        for i in range(self.scope):
            if (i == l):
                self.scope.reverse()
                return s
            s *= self.range[i]
        
        print "stride: ", s




    def __mul__(self, other):
        print
        print "Self Scope: ", self.scope
        print "Self Ranges: ", self.ranges
        print "Self Vals: ", self.vals
        print
        print "Other Scope: ", other.scope
        print "Other Ranges: ", other.ranges
        print "Other Vals: ", other.vals

        
        
        print "first self.scope:   ", self.scope

        new_scope = []
        for t in self.scope:
            new_scope.append(t)
        for s in other.scope:
            if s not in self.scope:
                new_scope.append(s)
        print "new_scope", new_scope
        

        print "second self.scope:   ", self.scope


        new_ranges = {}
        for i in new_scope:
            #print i #
            #print "self.scope: ", self.scope #
            try:
                if (i in self.scope):
                
                    print "self.ranges: ", self.ranges #          
                    #print i #
                    new_ranges[i] = self.ranges[i]
                elif (i in other.scope):
                    #print i #
                    new_ranges[i] = other.ranges[i]
            except KeyError:
                print "Raised error: ", i

        print "new_range: ", new_ranges

        
        j, k = 0, 0
        assignment = {}

        x1Ux2_values = []
        x1Ux2_cardinality = []
        
        for i in range(len(self.ranges) * len(other.ranges) - 1):
            new_factors.append(self.vals[j] * other.vals[k])
            for l in new_scope:
                assignment[l] = assignment[l] + 1
                if assignment[l] == self.ranges[l]:
                    assignment[l] = 0
                    # Loops back around to top is idea, might not work
                    j = j - (self.ranges[l] - 1) * self.vals[l]
                    k = k - (other.ranges[l] - 1) * other.vals[l]
                elif assignment[l] == other.ranges[l]:
                    assignment[l] = 0
                    j = j - (self.ranges[l] - 1) * self.stride[self, l]
                    k = k - (other.ranges[l] - 1) * other.vals[other, l]
                else:
                    j = j + self.ranges[l]
                    k = k + self.ranges[l]
                    break
        

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
        factor_ranges.append({j:var_dict[j] for j in factor_scopes[k]})



    # DEBUG
    print "Num vars: ",num_vars
    print "Ranges: ",var_ranges
    print "var_dict: ", var_dict
    print "factor_ranges: ", factor_ranges
    print "Scopes: ",factor_scopes
    print "Values: ",factor_vals
    return [Factor(s, v, r) for (s, v, r) in zip(factor_scopes, factor_vals, factor_ranges)]


#
# MAIN PROGRAM
#

def main():
    factors = read_model()
    for f in factors:
        print f.ranges
        print f.scope
    # Compute Z by brute force
    #f = reduce(Factor.__mul__, factors)
    f = Factor.__mul__(factors[0], factors[1])
    print "values of f: ", f.values
    print "scope of f: ", f.scope
    z = sum(f.vals)
    print("Z = ", z)
    return


main()
