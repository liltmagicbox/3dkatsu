from general import Name, UUID, ID, detailMaker, timef
NAME = Name()
UUID = UUID()
ID = ID()

#2nd way. we do not this.  reason 1:slow inherit parent __slot but son __dict??
#and hard to create class eachtime. but simply type, dict. we know 2 and got new event.
# class Event:
#     __slots__ = ['_from','_to', '_time' ]#for fast30% and prevent set attr.
#     def __init__(self):
#         self._from = 1
#         self._to = 1
#         self._time = 0

# class Event_key(Event):
#     def __init__(self, key,state,mods):
#         super().__init__()#so this shall be one time only. max depth=2. or put attrs.
#         self.key = key
#         self.state = state
#         self.mods = mods
    #what about not overwrite init but ..how? we cant.
    #just init with no init.

#1stway


class Event:
    __slots__ = ['to', 'time', 'etype', 'edata' ]#for fast30% and prevent set attr.
    def __init__(self, etype,edata):
        #self.from = 1
        self.to = 1
        self.time = 0
        self.etype = etype
        self.edata = edata
    def __repr__(self):
        return f"Event {self.etype}, {self.edata}"
    

edata = ('A',False,'CTRL')#better not split.
e = Event('key', edata)
print(e)


t = timef()
for i in range(1000000):
    e = Event('key', edata)
    if e.edata[0] == 'END':1
print(timef()-t)
#0.20971430000000002

class Event:
    __slots__ = ['to', 'time', 'etype', 'edata' ]#for fast30% and prevent set attr.
    def __init__(self, etype,edata):
        #self.from = 1
        self.to = 1
        self.time = 0
        self.etype = etype
        self.edata = edata
    def __repr__(self):
        return f"Event {self.etype}, {self.edata}"

edata = {'key':'A','state':False,'mod':'CTRL'}

t = timef()
for i in range(1000000):
    e = Event('key', edata)
    if e.edata['key'] == 'END':1
print(timef()-t)

#0.2531207
#0.2637472999999999
#use dict.


#final form
class Event:
    __slots__ = ['to', 'time', 'type', 'dict' ]#for fast30% and prevent set attr.
    def __init__(self, type,dict):
        #self.from = 1
        self.to = 1
        self.time = 0
        self.type = type
        self.dict = dict
    def __repr__(self):
        return f"Event {self.type}, {self.dict}"

print('____-')
e=Event('key',{'key':'A','state':False,'mods':'CTRL'})
print(e)
exit()


from vector import Vec3, parseV3, Vectuple#vec3 as vector

#actor may have multi many parent. Actor_another_version.
#Actor is also an type. same for: world, light, camera...

#func name: [1st low camel] detailMaker
#class name: [1st cap with _ ] Actor_double_head_dragon

#root class can not add any attr.
class Actor:#Actor_another_version. keep the type Actor_ first.
    __slots__ = ['_name','_UUID','_ID', '_x','_y','_z',]
    def __init__(self):
        self._ID = ID.set(self)
        self._UUID = UUID.set(self)
        self._name = NAME.set(self)
        
        #============
        #self.pos not good for axis. nor partial-change.
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
    #================================
    @property
    def detail(self):
        return detailMaker(self)
    def __repr__(self):
        return f"{self.name} of ID:{self.ID}" #this includes its type!
    #================================
    @property
    def ID(self):
        return self._ID
    @property
    def UUID(self):
        return self._UUID
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,newname):
        NAME.delete(self._name)#next cls_1 becomes cls_0 again.
        self._name = NAME.set(self,newname)#not auto clsname.
    
    @property
    def type(self):
        return self.__class__.__name__
    #================================
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
    @property
    def pos(self):
        return Vec3(self._x,self._y,self._z)
    @pos.setter
    def pos(self, value):
        if isinstance(value, Vectuple):
            x,y,z = value
            self._x,self._y,self._z = x,y,z


a= Actor()
a.pos = [1,2,3]
a.pos = Vec3(5,4,3)
a.pos+=5
print(a.x,a.y,a.z)
print(a.detail)
exit(0)

#@beartype
# def bear(name: str, age: int, win: (bool,float) ) -> list:
#     return [name,age,win]

# bear('hom',3,True)
# bear('hom',3,0)
# bear('hom',3,6)
# bear('hom',3,0.5)
# bear('hom',5.3,False)
# x = bear(3,5,False)
# print(x)


#son class can add new attr,(or whats meaning of subclass?) but not old root's attr.
class Actor_double_head_dragon(Actor):
    def __init__(self):
        super().__init__()
        self.head = 2
    def wecanaddmethod(self):
        for i in range(self.head):
            print(f"fire, {i+1}st")

def actorCheck():
    a=Actor()
    #print( str(type(a.bark)) )#<class 'method'>
    #print(type(a.bark).__qualname__)
    #print(type(a.bark).__name__)
    #print(a.bark.__qualname__)#Actor.bark
    # print(a.type)
    # print(a.name)
    # print(a)
    #a.bark = lambda x:print('xxx')#'Actor' object attribute 'bark' is read-only
    print(a.detail)
    #a.name = 'we cant'
    #a.xxxxxxname = 'we cant'

    print('======================\n')
    d = Actor_double_head_dragon()
    print(d.detail)
    d.wecanaddmethod()
    print('======================\n')

    d = Actor_double_head_dragon()
    def wecan_addfunc(not_self):
        print(not_self,'weeeeeeeeeee')
    d.wecanaddmethod = wecan_addfunc
    print(d.detail)
    d.wecanaddmethod(555)
    #d.name = 'we cant'
    #d.xxxxxxname = 'we can!!!!!!'  

if __name__ == '__main__':
    actorCheck()