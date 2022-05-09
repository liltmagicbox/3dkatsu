#ui layer item
#layer  holds items, layer blocks collision test. first in checked last.

"""
plate
  layer
    item
  layer
    item
    item

===containers:
list=[]
destroyer destroys inner-object.
empty

shared methods:
hit
update
destroy

push
pop
remove


"""



class UIPlate:
	def __init__(self):
		self.layers = []
	def __getitem__(self, idx):
		return self.layers[idx]
	def __repr__(self):
		rstr = f"class {self.__class__.__name__} ({len(self.layers)})"
		for layer in self.layers:
			rstr+='\n'
			rstr+=str(layer)
		rstr+='\n-----'
		return rstr
	def hit(self,x,y):
		for layer in reversed(self.layers):
			hitter = layer.hit(x,y)
			if not hitter == []:#since layer returns list.
				self.on_hit(self)
				return hitter
	def push_layer(self, layer):
		self.layers.append(layer)
	def pop_layer(self, idx=-1):
		return self.layers.pop(idx)
	def empty(self):
		if len(self.layers)==0:
			return True
		else:
			return False
	#===========
	def push(self,item):
		"""item through layer"""
		self.layers[-1].push(item)
	def pop(self):
		"""item through layer"""
		if len(self.layers)==0:return None#EMPTY
		return self.layers[-1].pop()
	def remove(self,layer):
		self.layers.remove(layer)
	# def brute_pop(self):
	# 	if len(self.layers)==0:
	# 		return None
	# 	item = self.layers[-1].pop()
	# 	if item==None:
	# 		self.layers.pop()
	# 		return self.pop()
	# 	else:
	# 		return item
	#====================
	def destroyer(self):#better name than destroy_check(seems checking itself destroyed)
		"""if contains sub-object"""
		remove_list = []
		for layer in reversed(self.layers):
			if layer.destroyed:
				remove_list.append(layer)
		for layer in remove_list:
			self.remove(layer)
	#def destroy(self):#plate not destroyed.
		#self.destroyed=True
		#self.on_destroy()
	#====================
	def on_hit(self, on_self):
		"""replace with def on_hit(self):"""
		1
	def update(self, dt):
		self.destroyer()
		self.on_update(self, dt)
	def on_update(self, on_self,dt):
		"""replace with def on_update(self,dt):"""
		1


def newfunc(self):
	print(self.name)
	print(1)

class Updater:
	def __init__(self):
		self.name = 'yeah'
	def __repr__(self):		
		return "[self_bound]"
	def destroy(self):
		print('destroy',self)
		self.on_destroy(self)
	def update(self,dt):
		print('update',self, dt)
		self.on_update(self, dt)
	def on_destroy(self, on_self):
		print('on-destroy',self)#ref_self will be used if replaced.
	def on_update(self, on_self,dt):
		print('on-update',on_self, dt)
	def uu(self):
		newfunc(self)

u=Updater()
u.uu()

#we cant just attach new method.
#u.newfunc = newfunc
#u.newfunc()


def test1():
	u=Updater()

	u.update(1)
	u.destroy()

	print('================replace destroy')
	print('')
	def new_on_destroy(ref_self):
		print('replcaed destroy', ref_self)
	u.on_destroy = new_on_destroy
	u.update(2)
	u.destroy()

	print('================replace update')
	print('')
	def new_on_update(ref_self,dt):
		print('replcaed update', ref_self,dt)
	u.on_update = new_on_update
	u.update(3)
	u.destroy()


	p = UIPlate()
	p.update(0.1)

	#@p.on_update# we cannot do this.but:
	def newnew(self,dt):
		print(dt,'xxx',self)
	p.on_update = newnew#do like this.
	p.update(9.9)


class UILayer:
	def __init__(self):
		""" stack collision checker"""
		self.items = []
		self.destroyed = False
	def __getitem__(self, idx):
		return self.items[idx]
	def __repr__(self):
		rstr = f"  class {self.__class__.__name__} ({len(self.items)})"
		for item in self.items:
			rstr+='\n'
			rstr+=str(item)
		return rstr
	def hit(self, x,y) -> list:
		"""return list / check from last one"""
		hit_list = []
		for item in reversed(self.items):#clever py!
			if item.hit(x,y):
				self.on_hit(self)
				hit_list.append(item)
				if item.consume:
					return hit_list #[item]this is fine.
				# else:
				# 	hit_list.append(item)
		return hit_list
	#====================
	def push(self,item):
		self.items.append(item)
	def pop(self,idx=-1):
		if len(self.items)==0:
			return None
		return self.items.pop(idx)
	def empty(self):
		if len(self.layers)==0:
			return True
		else:
			return False
	def remove(self,item):
		self.items.remove(item)
	#====================
	def destroyer(self):
		"""if contains sub-object"""
		remove_list = []
		for item in reversed(self.items):
			if item.destroyed:
				remove_list.append(item)
		for item in remove_list:
			self.remove(item)
	#=================
	def on_hit(self, on_self):
		"""replace with def on_hit(self):"""
		1
	def update(self, dt):
		self.destroyer()
		self.on_update(self, dt)
	def on_update(self, on_self,dt):
		"""replace with def on_update(self,dt):"""
		1
	def destroy(self):
		self.destroyed=True
		self.on_destroy(self)
	def on_destroy(self, on_self):
		"""replace with def on_destroy(self):"""
		1


class UIItem:
	@classmethod
	def xywh(cls, x,y,w,h):
		"""
		====w====
		|
		h (x,y)
		|
		====w====
		"""
		ww = w/2#not int. what if 0-1.0 world?
		hh = h/2
		x1 = x-ww
		x2 = x+ww
		y1 = y-hh
		y2 = y+hh
		return cls(x1,y1,x2,y2)
	
	@classmethod
	def p1p2(cls, p1,p2):
		x1,y1 = p1
		x2,y2 = p2
		return cls(x1,y1,x2,y2)
	
	@classmethod
	def from_abcd_ccw(cls, a,b,c,d):
		"""
		ccw 0,0-1,0-1,1-0,1 for gl sake.
		d c
		a b
		"""
		raise Exception("not implemented!")
	
	def __init__(self, x1,y1, x2,y2):#x0,x1 brings question about x2. but not x3.
		"""
		     y2
		x1    x2
		  y1
		(x1,y1,x2,y2)
		"""
		self.coords = (x1,y1,x2,y2)#fastest tuple.
		self.consume = True#for outer unit.
		self.destroyed = False#parent knows if destroyed, remove from itself.
	def __repr__(self):
		rstr = f"    class {self.__class__.__name__} {self.coords}"
		return rstr		

	def hit(self, x,y):
		"""not boundary, if x1<x<x2 and y1<y<y2:"""
		(x1,y1,x2,y2) = self.coords
		if x1<x<x2 and y1<y<y2:
			self.on_hit(self)#strange but through this, we can replace on_hit.
			return True
		else:
			return False
	#============live kinds.
	def on_hit(self, on_self):
		"""replace def on_hit(self)"""
		1
	def update(self, dt):
		self.on_update(self, dt)
	def on_update(self, on_self,dt):
		"""replace with def on_update(self,dt):"""
		1
	def destroy(self):
		self.destroyed=True
		self.on_destroy(self)
	def on_destroy(self, on_self):
		"""replace with def on_destroy(self,dt):"""
		1


class UIItem_bubble(UIItem):	
	def on_hit(self):
		self.destroy()


def brute_test():
	print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$sss')
	p = UIPlate()
	print(p)
	l1 = UILayer()
	l2 = UILayer()
	p.push_layer(l1)
	p.push_layer(l2)
	print(p)

	i1 = UIItem(0,0, 100,100)
	i2 = UIItem.xywh(400,400, 100,100)
	#p[1].push(i1)
	p[0].push(i2)
	p.push(i1)
	print(p)


	def broken(self):
		print(self)
		print('des$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$sss')

	#i1.on_destroy = lambda x: print('im done',x)
	#i1.on_hit = lambda x: x.destroy()

	def hitter(self):
		print('hhhhhh',self)
		self.destroy()
	i1.on_destroy = broken
	i1.on_hit = hitter

	x = p.hit(700,700)
	x = p.hit(70,70)
	x = p.hit(70,70)

	print(p)
	p.update(5)
	print(p)
	print(555555555555555)

	p.pop()
	p.pop()
	p.pop()
	p.pop()
	print(p)

if __name__ =='__main__':
	test1()
	brute_test()