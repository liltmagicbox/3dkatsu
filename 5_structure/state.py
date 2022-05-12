# #statemachine2

# class State:
# 	def __init__(self, state, to_trans_list):
# 		self.state = state
# 		self.to_trans_list = to_trans_list

# #s= State(0, [1,2])
# #s1= State(1, [0,2])
# #s2= State(2, [1,3])
# #s3= State(3, [0])

# s= State(0, [1,2])
# s1= State(1, [0,2])
# s2= State(2, [1,3])
# s3= State(3, [0])


# class State_machine:
# 	def __init__(self):
# 		self._state = 0
# 		self.dict = []
# 	def set_state(self,state):
# 		if stater.available(state):


# sm.state = 3#if not, not.


# available = {
# 	0:[1,2],
# 	1:[0,2],
# 	2:[1,3],
# 	3:[0],
# }

class SM:
	def __init__(self):
		self._state = 0
		self._available = {}
	def set(self, state, statelist):
		self._available[state] = statelist
	@property
	def state(self):
		return self._state
	@state.setter
	def state(self, state):
		if state in self._available[self._state]:
			print(f"state change: {self._state} >> {state}")
			self._state = state
		else:
			print(f"state change impossible: {self._state} >> {state}")

sm = SM()
sm.set(0,[1,2])
sm.set(1,[0,2])
sm.set(2,[1,3])
sm.set(3,[0])
sm.state = 3
sm.state = 1


sm.state=0


#State('fly', N, [1,3])
#State('fly', ['landing','fall'])

State('idle', ['sleep', 'flying', 'dead'] )
State('sleep', ['idle'] )
State('dead', [] )#outer func.

State('flying', ['landing','falling'] )#landing /falling only from here.

State('falling', ['dead'] )
State('landing', ['idle'] )

#Jap is an English abbreviation of the word "Japanese". Today, it is generally regarded as an ethnic slur.
State('mix', ['standard', 'japanese', 'ainu'] )
State('tripleMIX', ['enMIX', 'jpMIX', 'ainuMIX'] )



# play 'tiger'
# state of tigar

State('enMIX', ['tiger','fire','cyber','fiber','diver','viber','jya-jya'] )


#version 1
#assume tigar is the state.
#this seems good: actgually enmix is also state.
State('enMIX', ['tiger','fire','cyber','fiber','diver','viber','jya-jya'] )
#state tiger: init is play. after play, stop.
#tick, if play-ing, do nothing.
#if stop, parent state becomes tiger >> fire.
State('tiger', ['play','stop'])

def play():
	print('tiger')
State('play', ['play','stop'])

#version 2
#assume tigar is not state, but what to say.
#['tiger','fire','cyber','fiber','diver','viber','jya-jya'] 

#version3:
#enMIX is also not state, but combi of action(script)s.


#===============
#taking ver1, simulate
#i...m starting tripleMIX.
#...first..is..enMIX.. load..
#current idx=0, play( enMIX[0] ) #:tigar , idx+=1
#current idx=1, play( enMIX[1] ) #:fire , idx+=1
#---->>> enMIX_list = ['tigar','fire',] play( enMIX_list[0] ) #this is the one!
#... if idx== len(list): change state | engMIX >>> jpnMIX |

#player, plays,
#SM
#State
#Player music player. has state of playing / stopped / paused.
#idxplayer has list of loaded wavs, or on-play-load? current idx added.
#Mixman
#tiger-fire is one-way, but we can also run by idx. more simple way! and it's fixed!
#or if you var_MIX? then we need state, not fixed dict or list.
#see if tora - fire- jinjo-  .
#but, we cannot do thisway. this is another new MIX.
#mixman_state=[#list assumes idx. but cannot take over.

mixman_state_dict = {
	'init':[]
	'wait':[]
	'tripleMIX':['engMIX','jpnMIX','ainuMIX']
	#'engMIX' :[] not here! yeah.
}


#it's just data ref. not that class.
#use play() kinds. no tiger.play() kinds. player plays tiger.
#use idx here. no need to state.
engMIX_list = ['tiger','fire','cyber','fiber','diver','viber','jya-jya']

#wedonotuse like this
engMIX_state_dict = {
	''
	'init':[]
	'wait':[]
}

#names skip -ings. too long.
#fly inherits takeoff,landing. ..? state chagned instantly..

mixman_state_dict = {
	'init':[]
	'wait':['play']
	'play':['wait']	
}


'tripleMIX':['engMIX','jpnMIX','ainuMIX']
	#'engMIX' :[] not here! yeah.

def mixfunc():
	
State('play', mixfunc)
#-in mixman
if self.state == 'play':





def playmix():
	wordlist = ['tiger','fire','cyber','fiber','diver','viber','jya-jya']
	print(word)

State('enMIX', ['play'] )
State('play', ['playing'] )
State('playing', ['stop'] )
State('stop', ['play'] )

#not this
#State('enMIX', mix, 0)
#State('enMIX', mix, 1)


class Leveler:
	def __init__(self):
		self.level = 0
		self.exp = 0
		self.expmax = 10

	#def update(self):
	def levelcheck(self):
		if self.expmax <= self.exp:
			self.levelup()
			return True
		return False
	def levelup(self):
		self.level+=1
		self.exp -= self.expmax
		print(f'levelup: {self.level-1} >> {self.level}')
	def gain(self, exp):
		self.exp += exp
	#def update(self,dt):
	#	self.levelcheck()


class Player:
	def __init__(self):
		self.time = 0		
		self.sm = self.sm_init()
		self.leveler = Leveler()#property level.

	def sm_init(self):
		sm = SM()
		sm.set(0,[1,2])
		sm.set(1,[0,2])
		sm.set(2,[1,3])
		sm.set(3,[0])
		return sm
	
	def tick(self,dt):
		self.time+=dt
		state = int(self.time)%4
		if self.sm.state != state:
			self.sm.state = state			
		
		if self.sm.state == 0:
			print('0',end='')
		elif self.sm.state == 1:
			print('1',end='')
		elif self.sm.state == 2:
			print('2',end='')
		elif self.sm.state == 3:
			print('3',end='')
		#print(f"state now:{self.sm.state}")
		# if sm.state==0:
		# 	sm.state = 1
		# elif sm.state == 1:
		# 	sm.state = 2
		# elif sm.state == 2:
		# 	sm.state = 3
		# elif sm.state == 3:
		# 	sm.state = 0

print('-----------------')
player = Player()

import time

time_before = time.time()

for i in range(60*3):
	time.sleep(0.01)
	t = time.time()
	dt = t-time_before
	time_before = t
	player.tick(dt)
