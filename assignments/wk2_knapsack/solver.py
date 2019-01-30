#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    value = 0
    weight = 0

    #Select the algorithm
    taken = greedy(items, capacity)

    for item in items:
        if taken[item.index] == 1:
            value += item.value
            weight += item.weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def dyn_prog(items, capacity):
    taken = [0]*len(items)
    #Nested dictionary. First level is length of list items, second level is capacities
    dp = {}
    
    def subproblem(items, capacity):
        #Base Case
        if capacity <= 0 or len(items) == 0:
            return 0
        
        #Recursive Case
        if len(items) in dp and capacity in dp[len(items)]:
            return dp[len(items)][capacity]
        else:
            if len(items) not in dp:
                dp[len(items)] = {}
            if subproblem(items[1:], capacity) > subproblem(items[1:], capacity - items[0].weight) + items[0].value:
                dp[len(items)][capacity] = (0, subproblem(items[1:], capacity))
            else:
                dp[len(items)][capacity] = (1, subproblem(items[1:], capacity - items[0].weight) + items[0].value)
        return dp[len(items)][capacity][1]
    subproblem(items, capacity)
    
    #Extract indices of items taken
    return taken


def greedy(items, capacity):
    taken = [0]*len(items)
    value = 0
    weight = 0

    #Value Density
    def value_dens(item):
        return item.value / item.weight

    #Sort items in descending value density
    items.sort(reverse=True, key=value_dens)
    for item in items:
        if weight + item.weight <= capacity:
            weight += item.weight
            taken[item.index] = 1

    return taken

def trivial(items, capacity):
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    return taken


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

