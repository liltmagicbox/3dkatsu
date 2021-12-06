#the problem: classify: (1,0,0) vs 1,0,0.
#or just use if if if .

def solver(*args):
    #*args is tuple, at start.    
    #case:
    #1 means a value or a tuple
    #2 means 2 value
    #3 means 3 value...
    
    #typeint = type(1) define it outside of def..
    if len(args) == 1:
        if type(args[0]) == type(1):#means a int.
            x = args[0]
            print(f'one,x:{x}')
            return x

        else:#means tuple,, i think we can use actions below ..
            args = args[0]

    if len(args) == 2:
        x,y = args
        print(f'two,x:{x},y:{y}')
    elif len(args) == 3:
        x,y,z = args
        print(f'three,x:{x},y:{y},z:{z}')

    #----original action. haha.
    # elif len(args) == 2:
    #     x,y = args
    #     print(f'two,x:{x},y:{y}')
    # elif len(args) == 3:
    #     x,y,z = args
    #     print(f'three,x:{x},y:{y},z:{z}')

if __name__ == '__main__':
    solver(1)
    solver(1,2)
    solver(1,2,3)
    solver((1,2,3))

    solver((1,2))
    solver((9))
    #great!



def argsparse(*args):
    if len(args) == 1:
        if type(args[0]) == type(1):#means a int.
            x = args[0]            
            return x
        else:#means tuple,, i think we can use actions below ..
            args = args[0]

    if len(args) == 2:
        x,y = args
        return x,y
    elif len(args) == 3:
        x,y,z = args
        return x,y,z

def argsparse3(tup):
    if len(tup) == 0:
        return 0,0,0
    
    if len(tup) == 1:
        if type(tup[0]) == type(1):#means a int.
            x = tup[0]            
            return x,0,0
        else:#means tuple,, i think we can use actions below ..
            tup = tup[0]

    if len(tup) == 2:
        x,y = tup
        return x,y,0
    elif len(tup) == 3:
        x,y,z = tup
        return x,y,z


#-----------SPEED TEST.
# import time
# a= time.time()
# for i in range(1000000):
#     argsparse((1,1))
# print(time.time()-a)

#1 for 0.2
#1,1 for 0.17
#1,1,3 for 0.22

#((1,1,3)) for 0.31
#((1,2)) for 0.27.
#re-define var adds time.gotit.

#wow.. 10000 for 2ms. if rotmat 10000times per frame, we just consumed 2ms!
#maybe, it only 100 times, so, 2/100 ms. very fine.


#70ms for 1M. anyway time takes. so just do as you like, like wind flows.
# import time
# a= time.time()
# ham = 0
# for i in range(1000000):
#     ham+=(i+3)
# print(time.time()-a)