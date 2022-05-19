from general import timef




#new test aborted.
# keym = 'CTRL+A'

# t = timef()
# for i in range(1000000): #1M 130ms #str 30ms, split100ms
#     if '+' in keym:
#         *mods,key = keym.split('+')
#     kkk = '{key}_{mod}'#30ms
#     #kkk = [key, mod]#60ms!
# print( timef()-t )
#..we compare 'CTRL+A'=='CTRL+A'. no even need to split!








#==================oldone
key = 'ham'
mod = 'rona'

t = timef()
for i in range(1000000): #1M 130ms #str 30ms, split100ms
    #k,b = '{key}_{mod}'.split('_')
    kkk = '{key}_{mod}'#30ms
    #kkk = [key, mod]#60ms!
print( timef()-t )

class EE:
    def __init__(self,key,mod):
        self.key = key
        self.mod = mod

t = timef()
for i in range(1000000): #1M 200ms.
    b = EE(key,mod)
print( timef()-t )


class SEE:
    __slots__ = ['key','mod']
    def __init__(self,key,mod):
        self.key = key
        self.mod = mod

t = timef()
for i in range(1000000): #1M 184ms.
    s = SEE(key,mod)
print( timef()-t )

0.029700299999999957
0.21048849999999997
0.18047440000000003
print('==================================')
0.12996240000000003 #100ms for split (3 items, 140ms)
0.2692823 #60ms for .
0.2286311000000001 #50ms. (3items, 150ms!)

#class.attr is 1M 4ms-2ms

t = timef()
for i in range(1000000): #1M 130ms #str 30ms, split100ms
    1 #20ms
    #a=1 #30ms
    #a='{key}_{mod}' #40ms
    #a,b = (key, mod) #tuple 50ms +70.
    ##list 70 + 90
    #a = {'key':key,'mod':mod} #100ms
    #class 200ms.
    
    #a=='ath'#20ms. seems we grab from list..
    #k = '{key}_{mod}'.split('_') #_.17 __20  ___24 #split 100ms,+40ms
    #if k == 'key':1
    #    1
    #elif k=='ham':k=5 #this 4ms?
    #if 1>5:34#this 1ms
    #mod=='haerthearthoijeroigjoi'  #15ms
print( timef()-t )

class EE:
    def __init__(self,key,mod):
        self.key = key
        self.mod = mod

t = timef()
for i in range(1000000): #1M 200ms.
    b = EE(key,mod)
    c = b.key
    c = b.mod
print( timef()-t )


class SEE:
    __slots__ = ['key','mod']
    def __init__(self,key,mod):
        self.key = key
        self.mod = mod

t = timef()
for i in range(1000000): #1M 184ms.
    s = SEE(key,mod)
    x = s.key
    x = s.mod
print( timef()-t )
