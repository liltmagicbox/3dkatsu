

#https://docs.python.org/ko/3.7/library/operator.html
from general import detailMaker
import numpy as np


def parseV3(value):
    if len(value)==3:
        x,y,z = value
    elif value == ():#(())=>()  but ([],)
        x,y,z = 0,0,0
    else:
        value = value[0]
        if isinstance(value,tuple) or\
            isinstance(value,list) or\
            isinstance(value,Vec3) or\
            isinstance(value, np.ndarray):
            x,y,z = value
        else:
            if value==None:
                value = 0
            x,y,z = value,value,value
    return x,y,z

class Vec3:
    __slots__ = ['_x', '_y', '_z']
    def __init__(self, *value):
        x,y,z = parseV3(value)
        self._x = x
        self._y = y
        self._z = z
    def __repr__(self):
        return f"class {self.__class__.__name__} x:{self._x:.6f} y:{self._y:.6f} z:{self._z:.6f}"
    #def __getitem__(self, value):#__getitem__ legacy
    #it = iter(lambda : random.randint(0, 5), 2) stops at 2/ next(it) set def, can iter over
    def __iter__(self):#use this. most advanced.
        return iter( (self.x,self.y,self.z) )

    def __add__(self, *value):
        x,y,z = parseV3(value)
        x = self._x+x
        y = self._y+y
        z = self._z+z
        return self.__class__(x,y,z)
    def __sub__(self, *value):
        x,y,z = parseV3(value)
        x = self._x-x
        y = self._y-y
        z = self._z-z
        return self.__class__(x,y,z)
    def __mul__(self, *value):
        x,y,z = parseV3(value)
        x = self._x*x
        y = self._y*y
        z = self._z*z
        return self.__class__(x,y,z)
    def __pow__(self, *value):
        x,y,z = parseV3(value)
        x = self._x**x
        y = self._y**y
        z = self._z**z
        return self.__class__(x,y,z)

    def __truediv__(self, *value):
        x,y,z = parseV3(value)
        x = self._x/x
        y = self._y/y
        z = self._z/z
        return self.__class__(x,y,z)
    def __floordiv__(self, *value):
        x,y,z = parseV3(value)
        x = self._x//x
        y = self._y//y
        z = self._z//z
        return self.__class__(x,y,z)
    



    def __iadd__(self, *value):
        x,y,z = parseV3(value)
        self._x+=x
        self._y+=y
        self._z+=z
        return self
    def __isub__(self, *value):
        x,y,z = parseV3(value)
        self._x-=x
        self._y-=y
        self._z-=z
        return self
    def __imul__(self, *value):
        x,y,z = parseV3(value)
        self._x*=x
        self._y*=y
        self._z*=z
        return self
    def __ipow__(self, *value):
        x,y,z = parseV3(value)
        self._x**=x
        self._y**=y
        self._z**=z        
        return self

    def __itruediv__(self, *value):
        x,y,z = parseV3(value)
        self._x/=x
        self._y/=y
        self._z/=z
        return self
    def __ifloordiv__(self, *value):
        x,y,z = parseV3(value)
        self._x//=x
        self._y//=y
        self._z//=z
        return self

    @property
    def detail(self):
        return detailMaker(self)
    @property
    def x(self):
        return self._x  
    @x.setter
    def x(self,value):
        self._x = value
    @property
    def y(self):
        return self._y  
    @y.setter
    def y(self,value):
        self._y = value
    @property
    def z(self):
        return self._z  
    @z.setter
    def z(self,value):
        self._z = value


Vectuple = (list,tuple,Vec3, np.ndarray)


def vectortset():
    print('vvvvvvvvv')
    a = Vec3(2,2,2)
    x,y,z = a

    #a = a+3
    d = a+3
    print(d,'ddddddd is <555 but a 2>',a)
    print(a)
    a=Vec3([1,1,1])
    print(a)
    a+=(-1,-0.9,5)
    a-=(5,0,5)
    print(a)
    a+=5
    a**2
    print(a)
    #a = (3,3,3)
    print(a.detail)
    a.x+=5
    print(a)
    print('vvvvvvvvv')
    a+3
    a-3
    a*3    
    a/3
    a//2

    a+=3
    a-=3
    a*=3
    a/=3
    a//=2
    print(a.detail)
    n = np.array([1,2,3])
    a**=n
    print(a.detail)
    Vec3(n)
    x,y,z = Vec3(n)
    Vec3()
    #Vec3([])i dont want do this!

#whatif,,
#xyzxyzxyz... arrays ram continuos.
#xxxx
#yyyy
#zzzz
#...we hope not that axis -> oop trans.


if __name__ == '__main__':
    vectortset()