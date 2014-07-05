#! /usr/bin/python
# -*- coding: utf-8 -*-

# Hungarian Algorithm

from collections import defaultdict

def getMinAlignCost(a):
    a = subtractMinValue(a)
    a = maxMatch(a)
    print a

def subtractMinValue(a):
    for i, r in enumerate(a):
        min_cost = min(r)
        for j in xrange(len(r)):
            a[i][j] -= min_cost

    # i is length of row
    # j is length of column
    for i in xrange(len(a[0])):
        min_cost = 1000
        for j in xrange(len(a)):
            if min_cost > a[j][i]:
                min_cost = a[j][i]
        for j in xrange(len(a)):
            a[j][i] -= min_cost
        
    return a

def maxMatch(a):
    max_match = defaultdict(int)
    # zero in a row
    zero_r = defaultdict(list)
    # zero in a column
    zero_c = defaultdict(list)
    for i in xrange(len(a)):
        for j in xrange(len(a[i])):
            if a[i][j] == 0:
                zero_r[i].append(j)
    for i in xrange(len(a[0])):
        for j in xrange(len(a)):
            if a[j][i] == 0:
                zero_c[i].append(j)
#    print zero_r
#    print zero_c

    for i, v in sorted(zero_r.items(), key=lambda x: len(x[1])):
        cand = []
        for j, k in sorted(zero_r.items(), key=lambda x: len(x[1])):
            if i > j and len(v) > len(k):
                cand.extend(k)
        tmp = set(v)-set(cand)
        if len(tmp) > 0:
            for j in list(tmp):
                if j not in max_match.values():
                    max_match[i] = j
                    break

    if len(max_match.keys()) == len(a):
        return max_match

    # if max_match is not max, the following program continues
    # del_i is the index of the rows that should be deleted
    del_i = []
    # del_j is the index of the columns that should be deleted
    del_j = []
    del_i, del_j = changeCand(zero_r, zero_c, del_i, del_j)

    # cross is a crossing index of the deleted row and column
    cross = []
    not_del = []
    for i in del_i:
        for j in del_j:
            cross.append((i, j))

    for i in xrange(len(a)):
        for j in xrange(len(a[i])):
            if i not in del_i and j not in del_j:
                not_del.append((i,j))
#    print cross
#    print not_del
    tmp_min = 10000
    for k in not_del:
        if tmp_min > a[k[0]][k[1]]:
            tmp_min = a[k[0]][k[1]]

    for k in not_del:
        a[k[0]][k[1]] -= tmp_min
    for k in cross:
        a[k[0]][k[1]] += tmp_min
#    print "A: " + str(a)
#    print max_match
#    print
#    return a
    return maxMatch(a)
        
def changeCand(zero_r, zero_c, del_i, del_j):
    end = True
    # v is List type
    for v in zero_r.values():
        if len(v) > 0:
            end = False
    for v in zero_c.values():
        if len(v) > 0:
            end = False
    if end:
        return del_i, del_j

    # max_r = [(index, [indices of 0]), (2, [1,3,6])]
    max_r = sorted(zero_r.items(), key=lambda x: len(x[1]), reverse=True)
    max_c = sorted(zero_c.items(), key=lambda x: len(x[1]), reverse=True)

    if len(max_r[0][1]) >= len(max_c[0][1]):
        del_i.append(max_r[0][0])
        del zero_r[max_r[0][0]]
        for k, v in zero_c.items():
            row = del_i[-1]
            if row in zero_c[k]:
                zero_c[k].remove(row)
    else:
        del_j.append(max_c[0][0])
        del zero_c[max_c[0][0]]
        for k, v in zero_r.items():
            column = del_j[-1]
            if column in zero_r[k]:
                zero_r[k].remove(column)

#    print "MAX: " + str(max_r) + "\n\t" + str(max_c)
#    print "ZERO: " + str(zero_r) + "\n\t" + str(zero_c)
    return changeCand(zero_r, zero_c, del_i, del_j)

if __name__ == "__main__":
    a0 = [25,30,100,100,100]
    a1 = [20,100,70,35,100]
    a2 = [80,75,90,65,100]
    a3 = [100,100,100,55,40]
    a4 = [100,100,100,60,50]

    a = [a0, a1, a2, a3, a4]

    c = getMinAlignCost(a)

