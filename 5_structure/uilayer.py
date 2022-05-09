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
		self._list = []
		self.consume = False
		self.hitable = True
		self.name = NAME.set(self)
		#===for internal state
		self._root = True
		self._hit = False#hit-hit-hit
		self._destroyed = False

	@property
	def detail(self):
		return detailMaker(self)

	def __len__(self):
		return len(self._list)
	def __getitem__(self, idx):
		return self._list[idx]
	def __repr__(self):
		if self.empty:
			return f"layer {self.coords}"
		if self.name:
			return str(self.name)

		rstr = f"{self.__class__.__name__} {self.name} ({len(self._list)})["
		for item in self._list:
			rstr+='\n----'
			rstr+=str(item)
			rstr+=', '
		rstr+='\n]'		
		return rstr
	#==========================	
	@property
	def root(self):return self._root
	@property
	def destroyed(self):return self._destroyed
	#==========================
	def add(self,item):self.push(item)
	def append(self,item):self.push(item)
	def push(self,item):
		"""use this not _list."""
		self._root = False
		self._list.append(item)
	def pop(self,idx=-1):
		return self._list.pop(idx)# not len check here. let caller know what happens
	def remove(self,item):
		self._list.remove(item)
	@property
	def empty(self):#better tech:   isEmpty(self) #good namerule
		return len(self._list)==0

	#==========================
	def update(self,dt):
		if self.destroy_check():#destroy first,later update.
			return#skip update.
		#if self._destroyed:return True #else False
		#if self.destroyer():#destroy first!
			#return True#to upper object.
		self.on_update(self, dt)#this first before for.
		for item in reversed(self._list):
			item.update(dt)

	def hit(self,x,y):		
		#===clever! check itself.
		#hitCheckList = [self].extend(self._list)#recursive
		self_hit = hitTest(self.coords, x,y)

		hit_list = []
		for item in reversed(self._list):
			hits = item.hit(x,y)
			if len(hits) != 0:
				hit_list.extend(hits)#local hit
				if item.consume:
					break
		if self_hit and self.hitable and self._root:#root.
			self._hit = True
			hit_list.append(self)
		
		if len(hit_list)!=0:
			self.on_hit(self)#global self
		return hit_list

	def destroy_check(self):
		if self.empty:
			return self._destroyed

		remove_list = []
		for item in self._list:#blow bottom to up.
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
	def from_abcd_ccw(cls, a,b,c,d):
		"""
		ccw 0,0-1,0-1,1-0,1 for gl sake.
		d c
		a b
		"""
		raise Exception("not implemented!")


class Layer_size(Layer):
	def move(self, x,y):
		"""center point x,y"""
		x1,y1,x2,y2 = self.coords
		x1+=x
		x2+=x
		y1+=y
		y2+=y
		self.coords = (x1,y1,x2,y2)
	def moveto(self, x,y):
		"""center point x,y"""
		x1,y1,x2,y2 = self.coords
		__,__,w,h = self.to_xywh(x1,y1,x2,y2)
		x1,y1,x2,y2 = self.to_x1y1(x,y,w,h)
		self.coords = (x1,y1,x2,y2)
	def resize(self, w,h):
		"""keep the center"""
		x1,y1,x2,y2 = self.coords
		ww = (x2-x1)/2
		hh = (y2-y1)/2
		x1=ww
		x2=ww
		y1-=hh
		y2+=hh
		self.coords = (x1,y1,x2,y2)

	@classmethod
	def p1p2(cls, p1,p2):
		x1,y1 = p1
		x2,y2 = p2
		if x1>x2: x1,x2 = x2,x1
		if y1>y2: y1,y2 = y2,y1
		return cls(x1,y1,x2,y2)
	@classmethod
	def xywh(cls, x,y,w,h):
		x1,y1,x2,y2 = cls.to_x1y1(x,y,w,h)
		return cls(x1,y1,x2,y2)
	
	@classmethod
	def to_x1y1(cls, x,y,w,h):
		ww,hh = (w/2 , h/2) #not int. what if 0-1.0 world?
		x1,x2 = (x-ww),(x+ww)
		y1,y2 = (y-hh),(y+hh)
		return (x1,y1,x2,y2)	
	@classmethod
	def to_xywh(cls, x1,y1,x2,y2):
		x = (x2+x1)/2
		y = (y2+y1)/2
		w = x2-x1
		h = y2-y1
		return x,y,w,h

	#==========
	@property
	def pos(self):
		(x1,y1,x2,y2) = self.coords
		x,y,w,h = self.to_xywh( x1,y1,x2,y2)
		return x,y
	@pos.setter
	def pos(self, xy):
		self.moveto(xy[0],xy[1])
	@property	
	def size(self):
		(x1,y1,x2,y2) = self.coords
		x,y,w,h = self.to_xywh( x1,y1,x2,y2)
		return w,h
	@size.setter
	def size(self, wh):
		self.resize(wh[0],wh[1])
	#==========








class Layer_bubble(Layer):	
	def on_hit(self):
		self.destroy()


#base = Layer(0,0, 800,800)

def brute_test():
	Layer = Layer_size
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
	print(layer)
	base.hitable=False#
	xx = base.hit(40,40)
	print(xx)
	layer.move(10,10)
	layer.moveto(10,10)
	layer.moveto(550,10)
	layer.size = (500,500)
	layer.pos = 50,50
	print(layer.pos)


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