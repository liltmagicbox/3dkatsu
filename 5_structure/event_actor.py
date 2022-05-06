from general import Name, UUID, ID, detailMaker
NAME = Name()
UUID = UUID()
ID = ID()


class Event:
	__slots__ = ['_from','_to']#for fast30% and prevent set attr.
	def __init__(self):
		self._from = 1
		self._to = 1

class Event_key(Event):
	def __init__(self, key,state,mods):
		super().__init__()#so this shall be one time only. max depth=2.
		self.key = key
		self.state = state
		self.mods = mods
	#what about not overwrite init but ..how? we cant.
	#just init with no init.





#actor may have multi many parent. Actor_another_version.
#Actor is also an type. same for: world, light, camera...

#func name: [1st low camel] detailMaker
#class name: [1st cap with _ ] Actor_double_head_dragon

#root class can not add any attr.
class Actor:#Actor_another_version. keep the type Actor_ first.
	__slots__ = ['_name','_UUID','_ID']
	def __init__(self):
		self._ID = ID.set(self)
		self._UUID = UUID.set(self)
		self._name = NAME.set(self)
	def __repr__(self):
		return f"{self.name} of ID:{self.ID}" #this includes its type!
	@property
	def ID(self):
		return self._ID
	@property
	def UUID(self):
		return self._UUID
	@property
	def name(self):
		return self._name
	@property
	def type(self):
		return self.__class__.__name__
	#================================
	@property
	def detail(self):
		return detailMaker(self)
	#================================

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

actorCheck()