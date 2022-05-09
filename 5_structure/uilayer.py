#ui layer item
#layer holds items, layer blocks collision test. first-in last-checked.

from general import Name,detailMaker
NAME = Name()

def hitTest(coords, x,y):
	"""not boundary, if x1<x<x2 and y1<y<y2:"""
	(x1,y1,x2,y2) = coords
	return x1<x<x2 and y1<y<y2

class Layer:
	def __init__(self, x1,y1,x2,y2):#x0,x1 brings question about x2. but not x3.
		self.coords = (x1,y1,x2,y2)#fastest tuple.
		self.list = []
		self.consume = False
		self.hitable = True
		self.name = NAME.set(self)
		#===for internal state
		self._hit = False#hit-hit-hit
		self._destroyed = False

	@property
	def detail(self):
		return detailMaker(self)

	def __len__(self):
		return len(self.list)
	def __getitem__(self, idx):
		return self.list[idx]
	def __repr__(self):
		if self.empty:
			return f"layer {self.coords}"
		if self.name:
			return str(self.name)

		rstr = f"{self.__class__.__name__} {self.name} ({len(self.list)})["
		for item in self.list:
			rstr+='\n----'
			rstr+=str(item)
			rstr+=', '
		rstr+='\n]'		
		return rstr
	#==========================	
	@property
	def destroyed(self):return self._destroyed
	#==========================
	def add(self,item):self.push(item)
	def append(self,item):self.push(item)
	def push(self,item):
		self.list.append(item)
	def pop(self,idx=-1):
		return self.list.pop(idx)# not len check here. let caller know what happens
	def remove(self,item):
		self.list.remove(item)
	@property
	def empty(self):#better tech:   isEmpty(self) #good namerule
		return len(self.list)==0

	#==========================
	def update(self,dt):
		if self.destroy_check():#destroy first,later update.
			return#skip update.
		#if self._destroyed:return True #else False
		#if self.destroyer():#destroy first!
			#return True#to upper object.
		self.on_update(self, dt)#this first before for.
		for item in reversed(self.list):
			item.update(dt)

	def hit(self,x,y):		
		#===clever! check itself.
		#hitCheckList = [self].extend(self.list)#recursive
		self_hit = hitTest(self.coords, x,y)

		hit_list = []
		for item in reversed(self.list):
			hits = item.hit(x,y)
			if len(hits) != 0:
				hit_list.extend(hits)#local hit
				if item.consume:
					break				
		#above checks if self.empty:
		if self_hit and self.hitable:
			self._hit = True
			hit_list.append(self)
		
		if len(hit_list)!=0:
			self.on_hit(self)#global self
		return hit_list

	def destroy_check(self):
		if self.empty:
			return self._destroyed

		remove_list = []
		for item in self.list:#blow bottom to up.
			if item._destroyed:
				remove_list.append(item)
		if len(remove_list)!=0:
			self.on_destroy(self)#global self

		for item in remove_list:
			self.remove(item)
	#====================
	def on_update(self, on_self,dt):
		"""replace with def on_update(self,dt):"""
		1
	def on_hit(self, on_self):
		"""replace with def on_hit(self):"""
		1
	def on_destroy(self, on_self):
		"""replace with def on_destroy(self):"""
		1

	#==========================
	@classmethod
	def xywh(cls, x,y,w,h):
		ww,hh = (w/2 , h/2) #not int. what if 0-1.0 world?			
		x1,x2 = (x-ww),(x+ww)
		y1,y2 = (y-hh),(y+hh)
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


class Layer_bubble(Layer):	
	def on_hit(self):
		self.destroy()


#base = Layer(0,0, 800,800)

def brute_test():
	base = Layer(0,0, 800,800)
	base.name = 'base'

	layer = Layer(0,0, 200,200)
	#item = Layer.xywh(400,400,100,100)
	#layer.append(item)
	#item = Layer(0,0,100,100)
	layer.name = 'layer200'
	
	layer.append(Layer(0,0,50,50))	
	layer.append(Layer.xywh(50,50,100,100))
	
	base.append(layer)
	print(layer.detail)
	base.hitable=False#
	xx = base.hit(40,40)
	print(xx)
	#layer.click(x,y)
	#layer.touch(x,y)


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

# def newfunc(self):
# 	print(self.name,'newfunc')
# u=Updater()
# u.uu()

#we cant just attach new method like this:
#u.newfunc = newfunc
#u.newfunc()


if __name__ =='__main__':
	brute_test()