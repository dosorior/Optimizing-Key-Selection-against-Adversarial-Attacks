from multiprocessing import Pool

import numpy as np

def add_two_numbers(x,y):
     print("Value x {} and y {}".format(x,y))
     sum = x + y
     print("Sum is {}".format(sum))
     return x+y

def process_row(x):
    output = np.empty_like(values)
    for i, y in enumerate(values):
        output[i] = add_two_numbers(x, y)
        print("See output {}".format(output[i]))
    return output

# use a large number of values so processing takes some measurable amount of time
values = np.arange(3001)

with Pool() as pool:
    result = np.array(pool.map(process_row, values))

x, y = np.meshgrid(values, values)

result = add_two_numbers(x, y)