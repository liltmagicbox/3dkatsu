from vector import Vec3
from general import UUID,Name
UUID = UUID()
NAME = Name()


#self.active = True#skip update(not only physics). it acts like destroyed.
#self.physics = False#skip physics		
#self.visible = True#skip draw
#what if:
# state0: 'void': no active,no visible

# state0: 'ethereal': active, no visible
# state0: 'material': active, visible

# state1: notactive, visible
# state2: active, visible

# state3: 

#binary flags.
VISIBLE = 1
UPDATE 	= 2
PHYSICS = 4# not 3=1+2

STATE_BASIC = VISIBLE+UPDATE+PHYSICS
GHOST	= PHYSICS+UPDATE
FROZEN	= VISIBLE
NORMAL	= VISIBLE+UPDATE+PHYSICS

#1.global attrs. and combi of attrs => states
# each applications see attr board, do what they want.



#============================== get overwrite happens
class Get:
	#__slots__=['ham','attr']#whether do or not.
	def __init__(self):
		self.attr = 11
	def __getattr__(self,name):#do if failed to find key in self.__dict__
		return 555
	def __getattribute__(self,name):#do anyway.
		return 999999#if you enable this, you see 999999 x4 only.
g=Get()
print( g.ham )#555
g.ham = 99
print( g.ham )#99
print( getattr(g,'ham'))
print( g.__dict__ )#{'attr': 11, 'ham': 99} #since setattr is not overwritten.
#============================== get overwrite happens

oldSTATE_DICT = {
1:'visible',
2:'update',
4:'physics'
}

class bad_attr_StateMachine:
	__slots__ = ['_state']#+list(STATE_DICT.values())
	def __init__(self):
		self._state = 0b111
		#self.visible = True
		#self.physics = True
		#for name in STATE_DICT:
		#setattr(self,name,True)



#==========donno i wanna not useit..
class Setter:
	__slots__ = ['state',]#use even tuple!
	def __init__(self):
		self.state = 0b111
	def __set__(self, instance, value):
		instance.state = value
		print(value)
s=Setter()
s.state=4
print(s.state)
#==========donno i wanna not useit..

STATE_DICT = {
'visible':1,
'update':2,
'physics':4
}

class StateMachine:
	__slots__ = ['state',]#use even tuple!
	def __init__(self):
		self.state = 0b111
	def __getattribute__(self,name):#override all get.
		if name=='state':#except state.
			return super().__getattribute__(name)#hope it fast enough. i think so.
		return self.state & STATE_DICT[name]

	def __setattr__(self,name,value):
		if name=='state':#except state.
			return super().__getattribute__(name)#hope it fast enough. i think so.
		return self.state & STATE_DICT[name]

	
	def __repr__(self):
		print(dir(self))		
		self_state = self._state
		strs = []
		for i,name in STATE_DICT.items():
			if self_state & i:
				strs.append(name)
		return '|'.join(strs)
	


['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
 '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
  '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_state']


#s = StateMachine()
#print(s.state)

#print(s.update)
#s.physics = True
#print(help(s.__slots__))
#print(s)

#=========================================
STATE_DICT = {
'visible':1,
'update':2,
'physics':4
}
#state on the local ground:
visible =1
update = 2
physics =4


class StateMachine:
	__slots__ = ['state',]#use even tuple!
	def __init__(self):
		self.state = 0b101
	def __getattribute__(self,name):#override all get.
		if name=='state':#except state.
			return super().__getattribute__(name)#hope it fast enough. i think so.
		return self.state & STATE_DICT[name]

s=StateMachine()
import timeit




t1 = timeit.timeit(lambda:s.update, number=1000000)
print(t1)

print(s.update)


STATE_LIST = [
'visible',
'update',
'physics',
]
#use idx, first one be first.

#idx = state_list.find(key)
#return self.state[idx]

class StateMachine:
	__slots__ = ['_state',]#use even tuple!
	def __init__(self):
		self._state = [False for i in range(len(STATE_LIST))] #0b111		
	
	def __getattribute__(self,name):#override all get.
		if name=='_state':#except state.
			return super().__getattribute__(name)#hope it fast enough. i think so.
		idx = STATE_LIST.index(name) #vs DICT[name]
		return self._state[idx]

s=StateMachine()
print(s.update)
t1 = timeit.timeit(lambda:s.update, number=1000000)
print(t1)


exit(0)

class Actor_basic:
	def __init__(self):
		self.UUID = UUID.set(self)
		self.name = NAME.set(self)

		self._pos = Vec3(0,0,0)
		self._spd = Vec3(0,0,0)
		self._acc = Vec3(0,0,0)
		
		self.state = 0b111#this is the way, if new option added old-compatibility.
		
		self._on_dict= {
			'init':lambda self,args: print(f'here new born name is {self.name} !')
		}#2 then,init funcs here. whynot?
		self.on_run('init')#1 this,requires on_dict of class. what if init,after 1st tick?

	#==============================
	@property
	def pos(self):return self._pos
	@property
	def speed(self):return self._spd
	@property
	def acc(self):return self._acc
	
	@property
	def pos_angle(self):return self._pos_angle
	@property
	def speed_angle(self):return self._spd_angle
	@property
	def acc_angle(self):return self._acc_angle
	#==============================
	@pos.setter
	def pos(self,vec3):
		self._pos = vec3
		#no physics check.
	@speed.setter
	def speed(self,vec3):
		self._spd = vec3
		self.physics_check()
	@acc.setter
	def acc(self,vec3):
		self._acc = vec3
		self.physics_check()

	@pos_angle.setter
	def pos_angle(self,vec3):
		self._pos_angle = vec3
		#no physics check.
	@speed_angle.setter
	def speed_angle(self,vec3):
		self._spd_angle = vec3
		self.physics_check()
	@acc_angle.setter
	def acc_angle(self,vec3):
		self._acc_angle = vec3
		self.physics_check()
	#==============================

	def physics_check(self):
		"""it will have angular velocity.."""
		#if self._spd.magnitude==0 and self.acc.magnitude==0:
		if self._spd.magnitude==0 and self._acc.magnitude==0\
		and self._spd_angle.magnitude==0 and self._acc_angle.magnitude==0:
			self.physics=False
			self.state.physics=False#maybe best way!
			#self.state -= PHYSICS#0b010
			#self.state = 
		else:
			self.physics=True
		#if vec3.x==0:
		#Norm??? ????????? ?????? ?????? ????????? ???????????? ??????(??????)?????????.
		#Norm??? ????????? ????????? ????????? ???????????? ?????? ??????????????? ?????? ?????? Magnitude?????? ?????????.
		#vec3.norm


#direct push class, firm. (isit inherits all child's?)
#instance, is also working.
#what if instance.copy() and generator(of world)?

class Actor:
	on_dict = {}
	def __init__(self):
		self._pos = Vec3(0,0,0)
		self._spd = Vec3(0,0,0)
		self._acc = Vec3(0,0,0)
		self._pos_angle = Vec3(0,0,0)
		self._spd_angle = Vec3(0,0,0)
		self._acc_angle = Vec3(0,0,0)
		
		self.UUID = UUID.set(self)
		self.name = NAME.set(self)
		self.active = True#skip update(not only physics). it acts like destroyed.
		self.physics = False
		self.visible = True#skip draw

		self._on_dict= self.__class__.on_dict.copy() #{}
		self.on_run('init')

	#==============================
	@property
	def pos(self):return self._pos
	@property
	def speed(self):return self._spd
	@property
	def acc(self):return self._acc
	
	@property
	def pos_angle(self):return self._pos_angle
	@property
	def speed_angle(self):return self._spd_angle
	@property
	def acc_angle(self):return self._acc_angle
	#==============================
	@pos.setter
	def pos(self,vec3):
		self._pos = vec3
		#no physics check.
	@speed.setter
	def speed(self,vec3):
		self._spd = vec3
		self.physics_check()
	@acc.setter
	def acc(self,vec3):
		self._acc = vec3
		self.physics_check()

	@pos_angle.setter
	def pos_angle(self,vec3):
		self._pos_angle = vec3
		#no physics check.
	@speed_angle.setter
	def speed_angle(self,vec3):
		self._spd_angle = vec3
		self.physics_check()
	@acc_angle.setter
	def acc_angle(self,vec3):
		self._acc_angle = vec3
		self.physics_check()
	#==============================

	def physics_check(self):
		"""it will have angular velocity.."""
		#if self._spd.magnitude==0 and self.acc.magnitude==0:
		if self._spd.magnitude==0 and self._acc.magnitude==0\
		and self._spd_angle.magnitude==0 and self._acc_angle.magnitude==0:
			self.physics=False
		else:
			self.physics=True
		#if vec3.x==0:
		#Norm??? ????????? ?????? ?????? ????????? ???????????? ??????(??????)?????????.
		#Norm??? ????????? ????????? ????????? ???????????? ?????? ??????????????? ?????? ?????? Magnitude?????? ?????????.
		#vec3.norm
	#===================on methods
	def on_run(self, funcname, *args):#not _on_run to easy code.
		funcs = self._on_dict.get(funcname,[])
		for func in funcs:
			func(self, args)	
	def on_push(self, funcname, pushfunc):
		if not funcname in self._on_dict:
			self._on_dict[funcname] = []
		self._on_dict[funcname].append(pushfunc)
	def on_remove(self, funcname, pushfunc):
		self._on_dict[funcname].remove(pushfunc)#pop requires idx.
	def on_pop(self, funcname, idx=-1):
		funcs = self._on_dict[funcname]
		return funcs.pop(idx)
		#return funcs.pop(idx) if len(funcs) < abs(idx) else None
	def on_view(self):
		return self._on_dict.copy()
	#===================on methods

	#===================
	def update_pre(self,dt):
		"""exception on functions:
		tick_prePhysics
		tick_postPhysics
		tick_postUpdate
		"""
		#https://docs.unrealengine.com/4.27/ko/ProgrammingAndScripting/ProgrammingWithCPP/UnrealArchitecture/Actors/Ticking/
		self.on_run('update_pre',dt)#anim here	
	def update_physics(self, dt):
		if self.physics and (not self._AXIS):
			self._spd += self._acc*dt
			self._pos += self._spd*dt
			self._spd_angle += self._acc_angle*dt
			self._pos_angle += self._spd_angle*dt
		#===physics
		#self.on_update()
		#self.on_run('update',dt)
		#self.on_run('update',dt,2)		
		self.on_run('update_physics',dt)#after all positions fixed. imagine laser from gun.
		#setup particle
	def update_post(self,dt):
		self.on_run('update_post',dt)#judge
		#simulate particle
	#===================
	def update(self,dt):
		self.on_run('update_pre',dt)#anim here
		if self.physics and (not self._AXIS):
			self._spd += self._acc*dt
			self._pos += self._spd*dt
			self._spd_angle += self._acc_angle*dt
			self._pos_angle += self._spd_angle*dt
		self.on_run('update_physics',dt)#after all positions fixed. imagine laser from gun.
		self.on_run('update_post',dt)#judge
	#=========================

	def destroy(self):
		self.on_run('destroy')



class Actor:
	def __init__(self):
		self._pos = Vec3(0,0,0)
		self._spd = Vec3(0,0,0)
		self._acc = Vec3(0,0,0)
		self._pos_angle = Vec3(0,0,0)
		self._spd_angle = Vec3(0,0,0)
		self._acc_angle = Vec3(0,0,0)
		
		self.UUID = UUID.set(self)
		self.physics = False
		self._AXIS = False
		#self._axis = None#no need to store it?

		self._on_dict={}
		self.on_run('init')

		self.visible = True#skip draw
		self.active = True#skip update(not only physics). it acts like destroyed.


	#auto axis! for physics. this ensures just using .update(dt)
	#@property
	#def AXIS(self):return self._AXIS
	#@AXIS.setter
	def AXIS_set(self, axis):
		self._AXIS=True
		#self._axis = axis#no need to store it?
		idx = axis.set(self.UUID)#axis has UUID_dict, returns idx of AXIS.
		self._pos = axis[idx].pos
		self._spd = axis[idx].speed
		self._acc = axis[idx].acc
		self._pos_angle = axis[idx].pos_angle
		self._spd_angle = axis[idx].speed_angle
		self._acc_angle = axis[idx].acc_angle
	def AXIS_unset(self):
		self._AXIS=False
		#self._axis = None#hope this not useful..
		idx = axis.get(self.UUID)
		self._pos = Vec3(axis[idx].pos)
		self._spd = Vec3(axis[idx].speed)
		self._acc = Vec3(axis[idx].acc)
		self._pos_angle = Vec3(axis[idx].pos_angle)
		self._spd_angle = Vec3(axis[idx].speed_angle)
		self._acc_angle = Vec3(axis[idx].acc_angle)
		axis.unset(self.UUID)
	
	@property
	def pos(self):
		return self._pos
	@pos.setter
	def pos(self,vec3):self._pos = vec3

	@property
	def speed(self):return self._spd
	@property
	def acc(self):return self._acc
	@property
	def speed_angle(self):return self._spd_angle
	@property
	def acc_angle(self):return self._acc_angle
	@speed.setter
	def speed(self,vec3):
		self._spd = vec3
		self.physics_check()
	@acc.setter
	def acc(self,vec3):
		self._acc = vec3
		self.physics_check()
	@speed_angle.setter
	def speed_angle(self,vec3):
		self._spd_angle = vec3
		self.physics_check()
	@acc_angle.setter
	def acc_angle(self,vec3):
		self._acc_angle = vec3
		self.physics_check()

	def physics_check(self):
		"""it will have angular velocity.."""
		#if self._spd.magnitude==0 and self.acc.magnitude==0:
		if self._spd.magnitude==0 and self._acc.magnitude==0\
		and self._spd_angle.magnitude==0 and self._acc_angle.magnitude==0:
			self.physics=False
		else:
			self.physics=True
		#if vec3.x==0:
		#Norm??? ????????? ?????? ?????? ????????? ???????????? ??????(??????)?????????.
		#Norm??? ????????? ????????? ????????? ???????????? ?????? ??????????????? ?????? ?????? Magnitude?????? ?????????.
		#vec3.norm
	#===================on methods
	def on_run(self, funcname, *args):#not _on_run to easy code.
		funcs = self._on_dict.get(funcname,[])
		for func in funcs:
			func(self, args)	
	def on_push(self, funcname, pushfunc):
		if not funcname in self._on_dict:
			self._on_dict[funcname] = []
		self._on_dict[funcname].append(pushfunc)
	def on_remove(self, funcname, pushfunc):
		self._on_dict[funcname].remove(pushfunc)#pop requires idx.
	def on_pop(self, funcname, idx=-1):
		funcs = self._on_dict[funcname]
		return funcs.pop(idx)
		#return funcs.pop(idx) if len(funcs) < abs(idx) else None
	def on_view(self):
		return self._on_dict.copy()
	#===================on methods

	#===================
	def update_pre(self,dt):
		"""exception on functions:
		tick_prePhysics
		tick_postPhysics
		tick_postUpdate
		"""
		#https://docs.unrealengine.com/4.27/ko/ProgrammingAndScripting/ProgrammingWithCPP/UnrealArchitecture/Actors/Ticking/
		self.on_run('update_pre',dt)#anim here	
	def update_physics(self, dt):
		if self.physics and (not self._AXIS):
			self._spd += self._acc*dt
			self._pos += self._spd*dt
			self._spd_angle += self._acc_angle*dt
			self._pos_angle += self._spd_angle*dt
		#===physics
		#self.on_update()
		#self.on_run('update',dt)
		#self.on_run('update',dt,2)		
		self.on_run('update_physics',dt)#after all positions fixed. imagine laser from gun.
		#setup particle
	def update_post(self,dt):
		self.on_run('update_post',dt)#judge
		#simulate particle
	#===================
	def update(self,dt):
		self.on_run('update_pre',dt)#anim here
		if self.physics and (not self._AXIS):
			self._spd += self._acc*dt
			self._pos += self._spd*dt
			self._spd_angle += self._acc_angle*dt
			self._pos_angle += self._spd_angle*dt
		self.on_run('update_physics',dt)#after all positions fixed. imagine laser from gun.
		self.on_run('update_post',dt)#judge
	#=========================

	def destroy(self):
		self.on_run('destroy')





Actor.on_push('init',lambda self,args:print('guaaaaaaaaaaaaaaaaa') )
actor = Actor()

def main():
	import time

	def postupdate(self, args):
		dt = args[0]
		print('update', dt)
	actor.on_push('tick_postUpdate',postupdate)

	print(actor.on_view())
	for i in range(5):
		dt = i
		actor.update(dt)
		time.sleep(1)
		print('ho')

		if i==2:
			actor.on_push('destroy', lambda self,args:print('destroydestroy'))
		if i==3:
			actor.destroy()





if __name__=='__main__':
	main()

#============================

# class Actor:
# 	ll=[]
# 	@classmethod
# 	def add(cls, i):
# 		cls.ll.append(i)
# 	def __init__(self):
# 		self.age=0
# 		self.lll = self.__class__.ll.copy()
# 	def see(self):
# 		print(self.lll)


# Actor.add(13)
# a=Actor()
# a.see()

# Actor.add(44)
# a.see()

# class Bactor(Actor):
# 	ll=[]#if this exists, classmethod refs newer list. while older remained.
# 	#but this is dangerous, if single class miss this declare...

# b=Bactor()
# b.see()

# Bactor.add(555)
# b.see()

# b=Bactor()
# b.see()
# a=Actor()
# a.see()
# print(b.__class__.ll,'ll', Bactor.ll, Actor.ll)


# #avob,e i want..
# #1. class init, already built-in functions acts.
# #2. if alcss in class,  1-1 protect parent's function.
# #2-2 can modify.
# #...all this means, declare intentionally if you want .. inherit fuctions dict. or blank.fine.

# #next we move to state..  state input or state update.
# #state update maybe acts like .active ..?
# #after physics, ..idnondono

# #each class holds own's on_dict, not intererfere other's.

# #py has no CONSTANT, expected smart enough not to change those of..
# state_dict = {
	
# }
# #dict requires letters.. do this:
# #==============STATES

# # VOID = 0
# # ETHERIAL = 1
# # MATERIAL = 2
# # 0 1 2 4 6 7 .. 6 is 2+4 , while 7 is 1+2+4. 5 is 1+0+4.
# # FLAGS
# # 00000000
# # 00000001
# # 00000010
# # 00000011
# # too many.
# # 0000
# # 0001
# # 0010
# # 0011
# # 0100
# # 0101
# # 0110
# # 0111
# # #if you want more, just add bits.fine.
# # #reversed : active / physics / visible /

# VISIBLE = 1
# UPDATE 	= 2
# PHYSICS = 4# not 3=1+2

# GHOST	= PHYSICS+UPDATE
# FROZEN	= VISIBLE
# NORMAL	= VISIBLE+UPDATE+PHYSICS

# print( FROZEN & PHYSICS,'TTT')

# if actor.state & UPDATE:
# 	actor.update(dt)

# class State:
# 	def __init__(self,name,idx):
# 		self.name = name
# 		self.idx = idx

# #you have 2 way:
# actor.state.available(PHYSICS)
# actor.state % PHYSICS #not that bad. i love it!

# #AVOBE WITH ASSUMED WORLD UPDATE PROCESS IS FIXED.
# #RENDERER ALSO REQUIRES STATE, WHETHER WILL DRAW OR KINDS.
# #but its the  draw or update phase of them, so they will do they'r own thing!

# exit()