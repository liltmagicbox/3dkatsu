#position too long , we use pos all. acc of accelection. speed not spd however.
#mat matrix, so material. sad.
#bind binds. update(dt),simulates. not tick.
#list xxxs dict xxx_dict.
#most class has ..of that trackable
#make uuid for class..? class has type: 3dobjects light actor world camera kinds. all lower()




#from general import log, time, clamp
#time.time 0.8ms err, while time_ns 0.3ms, perf_counter 100ns. 10MHz!

#we write down all things.0

class World:
    """3d world, holding actors."""
    def __init__(self):
        self.actors = []# or dict by class?? we don't need that list but class dict better,yeah.
        
        #class ,what about custom actor or various lights?
        #or just fixed types: actor, light, camera kinds..
        #i think.. class name is just name, but type is the man.
        #or classname, which is fixed.
        #i want.. just use type. that we can group what things are, mostly. class too sensitive.

        #but whatabout camera or light actor shall be updated? or bound like cube..?
        #for 1000. we iter camera, we have dict.
        self.dict = {}#what name is??        

    def add(self, actor):
    	"""only actor can be added"""
    	#assert isinstance(actor, Actor)
    	#what if class.type?? type:"Actor" seems good. like type: Pointlight or Light_point kinds.
    	#self.actors.append(actor)
    	key = actor.type# camera light actor kinds. not classname, vulunable. whatif SpringCamera.?
    	if key in self.dict:
    		self.dict[key].append(actor)
    	else:
    		self.dict[key] = [actor]
    	#i love this simplity.


    def bind(self, window):
        """get dt from window"""
        window.update = self.update
    def update(self, dt):
    	"""dt shall be <16ms for physics accuracy. 100m/s, 10cm difference."""
    	for actor in self.actors:
    		#if actor.frozen
    		#if actor.simulated
    		#if actor.active
    		#all cares in actor, we just give them dt..?
    		actor.update(dt)
    	
    	for actor in self.dict['actor']:
    		actor.update(dt)
    	#what if camera?
    	#lets assume all by add is actor, movable kinds. self knows what to do.
    	for typeobjs in self.dict:
    		for actor in typeobjs:
    			actor.update(dt)
    	#done


class Actor:
	ext_img = ['png','jpg','jpeg','bmp','gif']
	ext_mesh = ['obj','smd']#gltf not yet.
	@classmethod
	def from_file(cls, fdir):
		"""file 3d obj kinds or 2d img"""
		_,ext = os.path.splitext(fdir)
		ext = ext.lower().replace('_','')
		if ext in ext_img:
			img = load(fdir)
			mat = Material(img)
			mesh = Mesh.rect()
			#Mesh.cube() Mesh.plate() Mesh.rect()
			mesh.material = mat
			#we got mesh now. -1~1 generalized. or 0-1.
		elif ext in ext_mesh:
			mesh = load(fdir)
		#_-we get mesh
		return self.__init__(mesh)

	def from_data(cls, data):
		"""data text: 'this shall be shown'
		or list of mesh_pos: [0,0,0, 1,0,0, 0,1,0]  NOT of : [[0,0,0], [1,0,0], [0,1,0] ]
		or plot XY or XYZ list. [ [1,2,3,4],[1,4,9,16],] #z [1,1,1,1] ]
		"""
		if isinstance(data,str):
			#str.. we.. make empty mat, texture, write str, we get rendered text tex, mat.
			return self.__init__(mesh)		
		
		if isinstance(data[0],list):#assume plot data
			1#we make plot 2d img.. how? plt? if course yeah!
			plot = plt.plot(X,Y,'r-o')
			plot_img = plot.to_img()
			mat = Material(plot_img)
			mesh = Mesh.rect()
			mesh.material = mat
			return self.__init__(mesh)
		#---try mesh.
		mesh = Mesh(data)
		if not mesh ==None:
			return self.__init__(mesh)
		#depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
		#https://stackoverflow.com/questions/6039103/counting-depth-or-the-deepest-level-a-nested-list-goes-to
		#_____		
		#elif isinstance(data,list):#what about ndarray?
		#isinstance(a,np.ndarray)
		#'ndarray' in str(type(a))
		#...or just give them to make mesh, and if fail, thats all..? not that bad. anyway mesh and vao requires finally , np.
		#..what? does vao requires np??? ..we do not use kivy, but three.js yeah.
		#if not depth(data):
		#we can: 1.check np type 2.check depth 3.just give, and fail,fine.
	def __init__(self, mesh_es):
		if not isinstance(mesh_es, list):
			mesh_es = [mesh_es]
		self.meshes = mesh_es

	def save(self):
		1
	def update(self, dt):
		"""simulates physical movements"""
		#if self.frozen or self.broken or self.notupdated or self....
		if self.movable:#what if it frozen? shall it be moved..?
			self.speed+=self.acc*dt
			self.pos+=self.speed*dt
		#...seems not that bad,anyway. isthat all?
		#ai of actor. ah. we need.. yeah.
		#and anything that input dt, system simulated, goes forward.
		#we also want, ai oop, but axis physics.? old-concept.
		#if we add ai, keep physics safe... we need ..
	def draw(self):
		"""full draw. actor stores multiple mesh.. of actor may be instanced"""
		self.meshes#should it be named so?
		for mesh in self.meshes:
			#mesh.bind()#Mesh knows what to do.fine. its internal thing.
			mesh.draw()

#is instanced actor or mesh?
#actor physics simulated with AXIS? NO! ~1000, we do py.
# AXIS actor is simulated, own way.



#type camera, SpringCamera


#we bind camera, since no camera, no renderer!!
class Renderer:
	"""def and replace draw using .render"""
	def __init__(self):
		#self.cam_2d = Camera()#size 0 to 1, orthogonal
		#self.cam_3d = Camera()#size -1 to 1 perspective..? or cool-ortho.
		self.camera = Camera_Ortho()

		1#self.window_dict = {}#main render combi holder window uuid. if we sort..
		#we just render as it defined. much better.!
	#def __getitem__(self,index):#hasattr(r,'__iter__')
	#	return 0
	#def add_render_target(self, window, target_world, camera=None):

	def render(self, window, target,camera=None):
		"""since this is in the loop.. we draw directly."""
		
		#_-full render path.
		#set window
		#set V,P

		#set M
		#draw
		
		#=======================
		window.bind()#set context.

		#if world, just let it do. see below.

		#else, we draw actor with camera.
		if camera == None:
			camera = self.camera
			#camera set size by target(actor). fits viewport.
			#let mesh has volume for collision. ..thats the vertex-accurate one!
			#either actor. actor has naive volume. cube or ball or humanball kinds.
			actor.collision.get_aabbcc()
			r = actor.collision.get_radius()
			d = r*2
			#camera.zoom()
			camera.set_width()#seems too width only.
			w,h = (aa[1]-aa[0]),(bb[1]-bb[0])#what if not centered..?
			ox,oy = (aa[0]+aa[1])/2, (bb[0]+bb[1])/2#we got offset, than slip just? move cam.pos?
			camera.set_size(w,h)
		camera.bind()#sets V,P. great. size in NDC.

		
		#strange but fine.
		if not isinstance(target, list):
			target = [target]
		for actor in target:
			M = actor.get_Model()
			actor.meshes
		#or simply,
		actor.draw()# binds sha,tex, set Model, bind vao, draw vao. or instanced.


		#if world, let them do.
		
		#we ..1000 or 2000.
		#and if 1000, we AXIS, instanced. very clear!
		#..or just draw slow
		for actor in world:
			#actor.mesh.material.bind()#let them do their own. #hope mesh has multi materials. imagine glowing-part of cloth..
			#M = actor.get_Model() #or of AXIS.
			#...who binds Model to shader..?
			#shader.set_uniform('Model',Model)
			
			#actor.set_Model()
			#actor.bind()#self knows if Model update needed.
			actor.draw()#if so, do we need just this?

			#mat.sha.bind()
			#mat.sha.set_uniform4x4('Model',M)#or instanced. thats why it shall not written here.
		#or means just world draws own. not that bad. world knows what light cam kinds is.
		if isinstance(target, World):
			world.draw()#binds cam,,all..



#mesh1, mesh2, of actor1. actor of hat+body, or cloth+LED. 
#mesh has vao, mat. matof shader,tex. fine.




	def bind(self, window):
		"""replace window.draw"""
		window.draw = self.draw
	def draw(self):
		"""replace func containing renderer.render()"""
		1

r=Renderer()

#render renders, as meaning. since we have world or actor, draw-ready, we can keep the meaning. not add_render.

#note: for this is manual order, window shall be same after. 1122 not 1212
r.render(window,world,camera)#general form.
r.render(window,actor)#for fast-view. cam from renderer. fits -1~1 space. course you can zoom.
r.render(window,[a1,a2])#quite list. fine. we NEED this too. yeah.
r.render(window,[a1,a2],cam)#this not auto cam, but used cam.


#=== at window draw
def drawer():
	#you can customize actor here, like animation, if wanted. not that world kinds.
	renderer.render(window,actor1)
	#or just full form.
	renderer.render(window,world,world.maincam)		

#renderer.bind(window)
#renderer.draw = drawer
window.draw = drawer#..yeah. we donot like bind.
window.update = world.update
window.input = inputman.input
#...was bad: we need to remember internal attr names.

#do this way.. not bad.!
inputman.bind(window)#seems fair
world.bind(window)#not that bad
renderer.draw = drawer#looks bad!
renderer.bind(window)#as we need this..









target_FPS = 60
target_dt = 1000/target_FPS
update_precision = 2#1ms hope we just keep less than 10ms..or16ms. its fine in this rough tough world.. 100m/s, 10cm err.

#in the window..loop..
#while not glfwWindowShouldClose

#dt=00 #dt means time passed from last loop. we need to update from it, mainly.
#input.. parsed ,, gethered to events. general form. sent to the controller.. i donno what to do next. fine.

#update..ifso. maybe if world stored, sent dt.




#=============================== various time simulator
#-loop1
ut=time()
self.update(2)
#world = self.world# we cannot since no world,ha!
updatetime = time()-ut

if update took 3ms:
dt = 16ms
16ms - 1ms(process_input) - 2ms(lastrender) -3ms(updatetime)= 10ms remained.
10ms// 3ms = 3times. we cannot 4 times.
for i in range(N)
	self.update(2)

if N==0:
	range0 is fine. yeah. simple code!
#=============================== various time simulator





#render, if you skip above, simply render (and updates!)

rt=time()#not that familier, but we not use time.time()-0.8ms accuracy.
self.render()
last_rendertime = time()-rt#used next loop sequence.


#actor = Actor.from_obj('xxx.obj')
#actor = Actor.from_img('xxx.png')

#actor = Actor.from_str('text')
#actor = Actor.from_XY(X=[0,1,2,3],Y=[0,1,4,9])

#_-what if?
#actor = Actor.from('xxx.png')
#actor = Actor.from([0,1,2,3],[0,1,4,9])
#actor = Actor.from([0,0,0, 1,0,0, 0,1,0] )#hope not that slow, we can update it brutely.



