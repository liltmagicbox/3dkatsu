
'move_right'
'jump'
'custom_function'

keymap_man ={
	'type':'man',
	'jump':[
		'SPACE',
		'W',
		'UP'
	],
	'move_right':[
		'RIGHT*1.0',
		'LEFT*-1'
		'D*1',
		'A*-1',
	],
	'custom_function':[
		'C'
	],
	
}

keymap_archer={
	'type':'archer',
	'release_arrow':[
		'F_RELEASE',
		'F_UNPRESS',
		'F_OFF',
		'F_UP',
	]
}.update(keymap_man)



class Man:
	keymap={
		0:keymap_man.update({'state_change':'S'}),
		1:keymap_archer
		}
	def state_change(self):
		self.state=1-self.state
	def __init__(self):
		self.x = 0
		self.xspeed = 0
		self.y = 0
		self.state=0
		
	def get_keymap(self):
		self.keymap[self.state]

	def update(self,dt):
		self.x+=self.xspeed
		self.on_update()
	def on_update(self):
		1
	def hp_check(self):
		if self.hp<0:
			self.destroy()
	def destroy(self):
		print('boom')
	def jump(self):
		prit('im jumping')
	def move_right(self, value):
		self.x== 10 * value
	def custom_function(self):
		self.move_right(0.5)
		self.jump()
		print('customized!')
	def release_arrow(self):
		print('arrow fired')

m = Man()
