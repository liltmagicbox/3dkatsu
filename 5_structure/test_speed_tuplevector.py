from general import timef, Name


t = timef()

class Tup:
    def __init__(self,x,y,z):
        self.pos = (x,y,z)
    def move(self):
        x,y,z = self.pos
        self.pos = (x+5,y,z)


class Lis:
    def __init__(self,x,y,z):
        self.pos = [x,y,z]
    def move(self):
        x,y,z = self.pos
        self.pos = (x+5,y,z)

t=timef()
for i in range(1000000):
    s = Lis(1,2,3)
    s.move()
print(timef()-t)

class Sss:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def move(self):
        self.x = self.x+5

t=timef()
for i in range(1000000):
    s = Sss(1,2,3)
    s.move()
print(timef()-t)
#0.34121409999999996
#0.3395418# little win of x.y.z/fine.





class Sss:
    __slots__ = ['x','y','z','_name']
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self._name = NAME.set(self)
    def move(self):
        self.x = self.x+5
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,newname):
        NAME.delete(self._name)
        self._name = NAME.set(self,newname)
        print('del')

#we already got answer. x,y,z raw stored. since AXIS.
#it affected from pos. who says!

#NAME = Name()
#==================20ms, almost no delay without print.
# t=timef()
# for i in range(10000):
#     s = Sss(1,2,3)
#     print(s.name)
#     if i==3:
#         s.name = 'max'
#         print(s.name,'new')
#     if i>5:
#         s.name = 'tree'
#         print(s.name,'new')
# print(timef()-t)
