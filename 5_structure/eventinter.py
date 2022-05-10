from general import timef, UUID
UUID = UUID()

#eventinter
#input->event.fine.
#..what if polling? let them create E also.

class Event:
	"""
		ver0.3 by >>> fromm . i want use it!
		+ key 0 or 'key' samespeed. 1Ms, 220ms. hope 1ms 1000s.. it will take 200ms..?
		ver0.2 just single data. changed attrs >>> by,to. UUID. or CURRENTPLAYER kinds?
		ver0.1 write somewhere dict of type:data. type:'key',data={'key':'A','mods':"CTRL',}
	"""
	__slots__ = ["_fromm","_to", "_type", "_data"]
	def __init__(self, type, data, fromm=None, to=None):
		"""type str,free name.(or key,idx of table) data single value, or dictkinds?
		fromm is since from cant. created by. to is target. both UUID.
		"""
		self._fromm = fromm
		self._to = to
		self._type = type
		self._data = data
	def __repr__(self):
		return f"Event {self.type}, data: {self.data}, fromm:{self.fromm}, to:{self.to}"
	@property
	def fromm(self):return self._fromm
	@property
	def to(self):return self._to
	@property
	def type(self):return self._type
	@property
	def data(self):return self._data

#=========abort new class.
#__slots__ = [""].extend(super().__slots__)
#instead new class, just set type diffent name, and dict has new type's key-value.
#class Key_event(Event):
#	@property
#	def key(self):return self._data['key']

def etest():
	#hope, all events has single data, not dict.
	e=Event('key','A')
	e=Event('key','CTRL+A')#this requires split alltime. bad. -we dont need split. just compare.
	#e=Event('key', {'key':'A','mods':'CTRL'})#this looks bad-est, however!
	e=Event('key','CTRL+A', by='ham', to='sandwitch')
	print(e)

	#=======================================
	class EE:
		__slots__=['i']
		def __init__(self, i):
			self.i = i

	class E4:
		__slots__=['i']
		def __init__(self, a,b,c=None,d=None):
			self.i = i

	t = timef()
	for i in range(1000_000):
		#e=EE()#70ms
		#e=EE('')#160ms >> 140ms if slots. single attrs.
		e=E4(5,4)#380ms,4attrs.
		e=Event('key','CTRL+A')#0.23 whether 0 or 'key'.
	print(timef()-t)

	#1s 1000_000
	#1ms 1000
	#0.23s 1000_000
	#0.23ms 1000
	#if you create 1000s, it will take 0.23ms. fine.


#each event, so-called world.target, will be directly changed current target's UUID.
# t = world.target
# if isinstance(t,list):
# 	for target in t:
#       sender = world.UUID#self.UUID
# 		e = Event(target = target.UUID, )


#ei.add(e)#deliver push



#1 target . not targets. become complex. (for in for.)
# E E E instead.! ..comfirmed. for i, occor event()
#target= lockon_UUID
#whatif, world's actor uuid?: target=world.UUID(hopely all UUID.), type destroyer {'actorUUID':}
#what if 100's destroy: you will get E,E,E,,,,100s. ..if that happens, that happened.


keymap = {
	'CTRL+A':'F',	
	'A':'-0.5*fire',
	'F': 'fire'
}

#Event( type = "key", data = (key, value) )


def key_event_parser(data):
	key, value = data
	for i in range(20):#safe while loop.
		if key in keymap:
			key = keymap[key]
		else:
			break
	#================
	key_mapped = key
	#we got mapped_key, value	
	if '*' in key_mapped:
		mul,funcstr = key_mapped.split('*')#costs x20 of cls.atr
	else:
		mul,funcstr = 1.0, key_mapped
	mul = float(mul)
	value = mul * float(value)
	return funcstr,mul

def destroy_event_parser(data):
	uuid = data
	target = UUID.get(uuid)
	target.destroy()

event_type_dict={
	'key': key_event_parser,
	'destroy': destroy_event_parser,
}

class EventInter:
	"""E interpreter or inter-object distributer.
	it's for singleton, use it as EI = E..()"""
	def __init__(self):
		self.list = []
		self.targets = []#{}#target UUID		
	def add(self, event):
		self.list.append(event)
	def add_target(self, target):
		self.targets.append(target)


	#==================================
	def broadcast(self):
		"""broad cast, casting events to target get from to(targetUUID)"""
		for event in self.list:
			target = event.to
			if target ==None:
				self.cast(self,event)
			else:
				target = UUID.get(target)
				#target.cast(event)
				self.cast(target,event)
		self.list = []
	#===============
	#@classmethod
	def cast(cls, self, event):
		"""will be used here only. cls, and realself."""
		#print(event,'from EI.')
		if event.type in event_type_dict:
			#===1 parse data
			event_data_parser = event_type_dict[event.type]
			funcs,value = event_data_parser(event.data)#value even kwargs
			#===2 actual process. value already completely parsed.
			if hasattr(self, funcs):
				func = getattr(self, funcs)
				func(value)
			else:
				return
		#this is!we done. ignore below..		
		#what if key, A? do we have A or shouldnt have 'A'?
		#no, we need key_map. thats the key. if event is key.
		#etype, evalue = event.type, event.value
		#if self.hasattr(etype):
			#func = self.getattr(etype)
			#func()
	#==================================	
	#=========custom
	def fire(self,value):
		print('fire', value*1000)

class W:
	def __init__(self):
		self.UUID = UUID.set(self)
	def fire(self,value):
		print('wwwwwwwwfire', value*1000)


#===at world,
def input(self, events):
	1

EI = EventInter()

w=W()
EI.add_target(w)

e=Event('key', ('A',1.0) )
EI.add(e)
e=Event('key', ('F',1.0) )
EI.add(e)
e=Event('key', ('CTRL+A',1.0) )
EI.add(e)


e=Event('key', ('A',1.0) ,to = w.UUID)
EI.add(e)
e=Event('key', ('F',1.0) ,to = w.UUID)
EI.add(e)
e=Event('key', ('CTRL+A',1.0) ,to = w.UUID)
EI.add(e)


EI.broadcast()

#EI.append()#not list

#way 1: 'key_A' 'destroy_UUUUIIIDD'
#way 2: 


#below we defined key-map , not all event-map. just key-map.
# SHIFT+CTRL+ALT+K is the key. thats all.
# if value in keys, value refs key. 'T': 'F'#like this.
# else just method name.. or multiplyer?? 0.1? fire(-0.1) ?? -seems not bad.
# '5*fire' or '-0.5*fire' or 'fire(-0.5)'...

#============================ value multiplyer.
def funcnamer(x):print(x)
#def *funcnamer():1
#def 1funcnamer():1
#def -1funcnamer():1
#def -1*funcnamer():1
#def 1*funcnamer():1
def fnametest():
	funname = "-0.5*funcnamer"
	idx = funname.find('*')#find returns -1, remember.
	value,func = funname.split('*')#find returns -1, remember.
	print(value,func)
	globals()[func](value)
	#works great!

#print('*' in funname)#strange but accept it..

	print(func_split(funname))

def func_split(string):
	if '*' in string:
		value,funcstr = string.split('*')#costs x20 of cls.atr
	else:
		value,funcstr = 1.0, string
	value = float(value)
	return funcstr,value


exit()

#for check both type and data.
"key_A"
"key_CTRL+F"
"destroy_UUIDUUIDUUIDUUIDUUIDUUIDUUID"
#each requires split. quite bad.! class.attr is better!
#DONT: type, value = edata.split('_') (split 100ms for 1M)
#do: t = event.type / v=event.value (event.value 5ms for 1M)

#at keymapper: (since it's key mapper. not event mapper.!)
#mods ordered SHIFT+CTRL+ALT /1st,2nd,3rd. both physical and logically better.
{
'F': 'fire',#functions already bound, defined.
'CTRL+S': 'shield',
"J_A": 'F',#key can be mapped to key.
'T': 'F',#like this.

#skill name not actually function, but state. if one can trans to fire(state), one do so.

#at magic scripter:
#'FireArrow' : 'stateA','stateB','stateC'#lovely.!
'FireArrow' : 'stateA-stateB-stateC',#lovely.!
'A':'stateA',#inner-mapping for easy to write. this time, we not use key so we can do so.
'C':'stateC',
'FireArrow' : 'A-A-C',#lovely.!
'Dshot': 'FireArrow-Granade!',
"Granade!":'getGranade-setSpeed(20)-getFront-fire',#getGranade is func.
#get gets, set sets what get got...or all funcs works to get.
#if you need N,
'G':'getGranade',
'G10' : 'G-G-G-G-G-G-G-G-G-G',
'G100' : 'G10-G10-G10-G10-G10-G10-G10-G10',
"Granade_mass": 'G100-splatter-setSpeed(20)-getFront-fire',#bad setDirection(1,0,0)
"GW": 'Granade!-wait(0.5)',
"Granade_launch5x": 'GW-GW-GW-GW-GW', #'GW[5]'#seems too naive, we not use it. not use [],good.
#X"Granade_launcher": 'GW[launch_times]'# try to find local ref launch_times , fail: this is args.
#NO we cant do thisway. python loads GW and do for i in range(N).

#len is cost. simple.or you can map.

'fireArrow' : 'getArrow-setFire-setFront-fire' #if arrows allows fire, fire only for tip. allow list.
}