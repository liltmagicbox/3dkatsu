import timeit

visible =0
update = 1
physics = 2

alist = [True,False,True]


import timeit




t1 = timeit.timeit(lambda: "-".join(map(str, range(100))), number=10000)
print(t1)