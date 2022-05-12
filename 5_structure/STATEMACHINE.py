#STATE MACHINE

class StateMachine:
	def __init__(self):
		self.state = 0
		self.reserved = []
		self.state_dict = {}
		self.key_dict = {}	

		self.hp = 30
	def set(self, state):
		#state = self.state_dict.get(state,None)
		if state in self.state_dict:
			state_before = self.state
			self.state = state
			print('state changed: ', state_before,'> to >',state)
	def tick(self):
		print('tick', self.state_dict[self.state])
	def input(self):
		key = input('input key:')
	
	#============instant
	def destroy(self):
		print('im die!')
		self.state = -1#clever!
	def damage(self, value):#i want protector, that reduces damage 1/2. ..it covers before damage.
		self.hp-=value
		print('owww')
		if self.hp<0:
			self.destroy()

	#===================
	#animation.

	def run(self):
		while self.state != -1:#after destroyed! destoy anim can be played yet.


	def interpreter(self,key):
		if key in self.key_dict:




state_dict = {
	0:'default',
	1:'move',
	2:'attack',
	3:'attracted',
	4:'sleep',
	5:'sleepy'
}

cat = StateMachine()
cat.state_dict = state_dict

print(cat.state)
