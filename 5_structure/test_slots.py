class exnamer:
    __slots__ = [ 'name','age']
    def __init(self):
        self.name = 'namer'
        self.age = 33
a = exnamer()
print(dir(a))
#print(a.age, a.name)
a.part= 3
print(dir(a))
exit()

class nMan:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Man:
    __slots__ = ['name', 'age']

    def __init__(self, name, age):
        self.name = name
        self.age = age

class nSuperMan:
    def __init__(self, name, age):
        self.name = name
        self.age1 = age**1251
        self.age2 = age**1251
        self.age3 = age**1251
        self.age4 = age**1251
        self.age5 = age**1251

class SuperMan:
    __slots__ = ['name', 'age1', 'age2', 'age3', 'age4', 'age5']

    def __init__(self, name, age):
        self.name = name
        self.age1 = age**1251
        self.age2 = age**1251
        self.age3 = age**1251
        self.age4 = age**1251
        self.age5 = age**1251

#NMan 199MB 1M
#Man 150->90MB 1seconds after.

#superman 5.7 GB
#Nsuman5.8
#slot prevents __dict__
#>>> a.__dict__
#{'name': 'ham', 'age': 22}
#with slots, not.

#>>> dir(a)
#['__class__', '__delattr__', '__dir__', '__doc__',
 
#>>> dir(a)
#['__class__', '__delattr__', '__dict__', '__dir__', '__doc__'


aa= []
for i in range(100000):#was 1M, too slow
    a = nMan('hans',86)
    aa.append(a)


print('halt for memory hold..')

import time
time.sleep(1230513)
x = input('wait')
print(x)
