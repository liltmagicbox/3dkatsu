from PIL import Image
from os.path import join, split, splitext
import os

from math import cos,sin
#smdreader. now tris only. smd has:[ vertex-mtl ..]. same mtl, same vert.

Mesh([0,0,0, 1,0,0, 0,1,0]) #fineest!
Mesh(position = [0,0,0, 1,0,0, 0,1,0])
Mesh([0,0,0, 1,0,0, 0,1,0], draw='point') #point line triangle only 3way.fine.
Mesh([0,0,0, 1,0,0, 0,1,0, 1,1,0], [0,1,2, 1,2,3])
Mesh([0,0,0, 1,0,0, 0,1,0, 1,1,0], indices = [0,1,2, 1,2,3])

Mesh([0,0,0, 1,0,0, 0,1,0], texture = ) #by name.fine.
Mesh([0,0,0, 1,0,0, 0,1,0], shader = )
Mesh([0,0,0, 1,0,0, 0,1,0], material = )

material = Material(shader = 'default', texture ={'diffuse_0': tex1 } )

sha = Shader.load('sha.vs','sha.fs')
sha = Shader.get('default')
tex = Texture.get('checker')

material = Material(shader = 'default', texture ={'diffuse_0': tex1 } )

#better use material.
#Mesh([0,0,0, 1,0,0, 0,1,0], texture = tex )
#Mesh([0,0,0, 1,0,0, 0,1,0], texture = 'checker' )

mat = Material( {'shader':sha, 'texture':{'diffuse_0':tex1} } )
mat = Material(shader=, texture={'diffuse_0':tex1} )
mat = Material( texture={'diffuse_0':tex1} )

mat = Material(tex1)
mat = Material(shader = 'default', texture = tex1)
mat = Material(shader = 'default', texture = 'default')
#mat.tick(dt)

Mesh([0,0,0, 1,0,0, 0,1,0], material = mat)


texture.bind()# for channel0
texture.bind(channel =0)# for channel0 default??
texture.bind(channel) #specific chennel. channel=int


class Material:
	def __init__(self, shader, texture):
		self.shader = ''
		self.textures = {}		
	#def copy(self):
	def from_json(self, jsonpath):#too complexed.
		shadername = material_dict['shader']
		shader = Shader.load('shadername')#fs,vs..?
	def from_dict(self, material_dict):
		shadername = material_dict['shader']
		shader = Shader.get('shadername')
		self.shader = shader		
		textures = material_dict['texture']
		for channel , texname in textures.items():
			texture = Texture.get(texname)
			self.textures[channel] = texture
	def bind(self):
		shader = self.shader
		shader.bind()
		textures = self.textures
		for i, key in textures:
			texture = textures[key]
			shader.set(key,i)
			texture.bind(i)

			#diffuse, tex1
			#specular, tex2
			#1. loc = shader.get_loc('diffuse')
			#2. gluint(loc, N)
			#1,2-> shader, get loc, and returns N, assigned number.
			
			#3. active N
			#4. bind(tex)
			#3,4-> texture.bind(N)

			#channel diffuse
			#1. get location of channel
			#2. set gl i of location
			#3. active texture i
			#4. bind texture id.

			#N iterated
			# loc = shader.getloc('diffuse')
			# shader.set_uniform(loc,N)
			# glUniformi(loc,0)
			
			# texchannel = texture.gltexdict[0]
			# glActiveTexture(texchannel)
			# texture.bind(0)

			

			#channelN = shader.getchannel('diffuse')#if actully from shader, yeah.
			#texture.bind(0) #is for texture.

			#texture.bind('diffuse')
			
	#def tick(self,dt): for mat_anim only
		#self.time+=dt
		#self.update()





class Mesh:
	""" python object for internal usage ..and little to glTF"""
	def __init__(self, position, uv, indices, material):
		self.attributes = {}#position normal uv
		self.indices = None #just list? ..or ndarray?
		#self.material = None # {shader:, texture:{diffuse_0:} }
		#self.name = None not native. it's too artificial.
		# material{
		# 'name':name,
		# 'shader':'default',
		# 'texture':{
		# 'diffuse_0':texturepngname
		# }
		# }

		attributes = {}
		attributes['position'] = position
		if uv:
			attributes['uv'] = uv
		
		#vao
		indexed = True
		if not indices:
			indexed = False

		if not material:
			material = Material.get('default')
		self.material = material

	@classmethod
	def load_smd(cls, fdir):
		resultdict = smd_load(fdir)
		return resultdict
		#return resultdict['meshes'] #of Mesh.
	@classmethod
	def load_obj(cls, fdir):
		1
	@classmethod
	def save_obj(cls, meshes, fdir):
		obj_save(meshes,fdir)
	def draw(self):
		if not self.isdrawready:
			self.draw_ready()
	@classmethod
	def load_json(cls, fdir):
		json = loadxxx
	@classmethod
	def from_dict(cls, mesh_dict):
		1
	def draw_ready(self):
		self.shader
		#self.texture
		self.vao



#============================================================
def obj_save(meshes,fdir):
		lines = []
		header = "# obj created from meshes"
		lines.append(header)
		#o meshname
		#v x y z
		#vt u v
		#vn a b c
		#usemtl mtlname
		#f v/vt/vn v/vt/vn v/vt/vn
		mesh1 = meshes[0]
		objname = mesh1.modelname

		def get_mtlname(mesh):
			texname = mesh.texture.get('diffuse')
			mtlname = splitext(texname)[0]
			if 'diffuse' in mtlname:
				mtlname = mtlname.split('diffuse')[0]
			elif 'albedo' in mtlname:
				mtlname = mtlname.split('albedo')[0]
			return mtlname
		
		def parse_mesh(mesh, lastlen):
			write_method = 123 #123 or 111

			lines = []

			mtllib_ = f"mtllib {mesh.modelname}.mtl"
			lines.append(mtllib_)

			texname = mesh.texture.get('diffuse')
			if not texname:
				texname = mesh.texture.get('albedo')#maybe?
			#---vertex
			o_ = f"o {mesh.name}"
			lines.append(o_)
			#if 'kaidan' in texname:
			#	print(mesh.vert_dict['uv'])

			#for no diffuse now.
			mtlname = get_mtlname(mesh)
			usemtl_ = f"usemtl {mtlname}"
			lines.append(usemtl_)

			s_ = f"s 1"#off, ue4 errs no smoo..
			lines.append(s_)


			if write_method == 123:
				vs = mesh.vert_dict['position']
				vns = mesh.vert_dict['normal']
				vts = mesh.vert_dict['uv']
				for i in range( len(vs)//3 ):
					x = vs[0+i*3]
					y = vs[1+i*3]
					z = vs[2+i*3]
					v_ = f"v {x} {y} {z}"
					lines.append(v_)

					x = vns[0+i*3]
					y = vns[1+i*3]
					z = vns[2+i*3]
					v_ = f"vn {x} {y} {z}"
					lines.append(v_)

					x = vts[0+i*2]
					y = vts[1+i*2]
					v_ = f"vt {x} {y}"
					lines.append(v_)

			elif write_method == 111:
				vs = mesh.vert_dict['position']
				for i in range( len(vs)//3 ):
					x = vs[0+i*3]
					y = vs[1+i*3]
					z = vs[2+i*3]
					v_ = f"v {x} {y} {z}"
					lines.append(v_)

				vts = mesh.vert_dict['uv']
				for i in range( len(vts)//2 ):
					u = vts[0+i*2]
					v = vts[1+i*2]
					vt_ = f"vt {u} {v}"
					lines.append(vt_)

				vns = mesh.vert_dict['normal']
				for i in range( len(vns)//3 ):
					x = vns[0+i*3]
					y = vns[1+i*3]
					z = vns[2+i*3]
					vn_ = f"vn {x} {y} {z}"
					lines.append(vn_)


			#---faces

			idx = mesh.indices
			for i in range( len(idx)//3 ):
				v1 = idx[0+i*3]+1+lastlen
				v2 = idx[1+i*3]+1+lastlen
				v3 = idx[2+i*3]+1+lastlen
				f_ = f"f {v1}/{v1}/{v1} {v2}/{v2}/{v2} {v3}/{v3}/{v3}"
				lines.append(f_)

			lastlen = len(vs)//3
			#print(lastlen)see 1306 406 45, we need to add.
			return lines, lastlen

		lastlen = 0
		for mesh in meshes:
			meshline, verylastlen = parse_mesh(mesh,lastlen)
			lastlen+=verylastlen
			lines.extend(meshline)
		fullline = '\n'.join(lines)
		with open(fdir, 'w', encoding = 'utf-8') as f:
			f.write(fullline)

		mtlline = []
		for mesh in meshes:
			mtlname = get_mtlname(mesh)		
			
			mtlline.append( f"newmtl {mtlname}" )
			mtlline.append( f"Ns 333.0" )
			mtlline.append( f"Ka 1.0 1.0 1.0" )
			mtlline.append( f"Kd 0.8 0.8 0.8" )
			mtlline.append( f"Ks 0.5 0.5 0.5" )
			mtlline.append( f"Ke 0.0 0.0 0.0" )
			mtlline.append( f"Ni 1.45" )
			mtlline.append( f"d 1.0" )
			mtlline.append( f"illum 2" )
			dfile = mesh.texture['diffuse']
			if not dfile:
				dfile = mesh.texture['albedo']
			mtlline.append( f"map_Kd {dfile}" )
			mtlline.append( "" )

		fullline = '\n'.join(mtlline)

		if '.obj' in fdir:
			mtldir = splitext(fdir)[0]+'.mtl'
		else:
			mtldir = fdir+'.mtl'
		with open(mtldir, 'w', encoding = 'utf-8') as f:
			f.write(fullline)



#hopely we dont alas, its for .. big building..
def atlas(cls, meshes, SIZE = 2048):
		"""we assume all channels same size. we have 4096 over problem, too!"""
		def save_atlas(channel, onlyonetexture = False):
			cc=0
			mesh1 = meshes[0]
			w_before =0
			h_before =0
			atlas = Image.new('RGBA', (SIZE,SIZE) )
			coord_dict = {}
			#----------------phase1, eachmesh, texture merge
			for mesh in meshes:
				meshname = mesh.name
				
				fname = mesh.texture[channel]
				fdir = join(mesh.path,fname)
				try:
					#------------open img
					img = Image.open(fdir)
					w,h = img.size
					if w_before + w <= SIZE:
						#atlas.paste(img, (w_before,h_before ) )
						imgxa,imgya, imgxb,imgyb = (w_before,SIZE-h_before-h, w_before+w, SIZE-h_before)
						atlas.paste(img, (imgxa,imgya, imgxb,imgyb) )
						cc+=1

						offset_x,offset_y,width_x,width_y = w_before,h_before, w,h
						coord_dict[meshname] = (offset_x,offset_y,width_x,width_y)

						w_before+=w#note it's last line
						

					else:
						w_before=0
						h_before+=h
						#print(w_before,w, w+w_before,meshname)					
						#img.show()
						if h_before + h <= SIZE:
							imgxa,imgya, imgxb,imgyb = (w_before,SIZE-h_before-h, w_before+w, SIZE-h_before)
							atlas.paste(img, (imgxa,imgya, imgxb,imgyb) )
							cc+=1
							
							offset_x,offset_y,width_x,width_y = w_before,h_before, w,h
							coord_dict[meshname] = (offset_x,offset_y,width_x,width_y)
							w_before+=w#need here too!
						else:
							print('size over!')
					#print( (imgxa,imgya, imgxb,imgyb),mesh.name)
					img.close()
					#------------open img
				except:
					print('no texture:',mesh.name)
					pass#only corrd_dict has no key of mesh.

			print(cc,'of texture merged')			
			atlasname = f'{mesh1.modelname}_atlas___{channel}.png'
			if onlyonetexture: atlasname = f'{mesh1.modelname}_atlas.png'
			path = mesh1.path
				
			atlas.save( join(path,atlasname) )#or running dir?
			print(f'atlas of channel:{channel} saved at {path}')
			return coord_dict,atlasname
		
		mesh1 = meshes[0]
		
		

		for channel in mesh1.texture:
			if len(mesh1.texture)==1: #only a channel , no need to name it.
				coord_dict,atlasname = save_atlas(channel, True)
			else:
				coord_dict,atlasname = save_atlas(channel)			

			#-very rough way. fine. we get from last done textture
			meshes_atlas = []
			meshes_left = []
			#------------phase2, uv slide
			# we have offset, w,h, we load uv array, add , and replace.
			# ..is that all? nomatter texture N, we do once. fine.
			#----each mesh, change UV each.			
			for mesh in meshes:
				meshname = mesh.name
				uvoffs = coord_dict.get(meshname)
				if not uvoffs:
					meshes_left.append(mesh)#we do before continue
					continue#skip below. break breaks, pass just goes after line.
				ox,oy, w,h = uvoffs
				uvlist = mesh.vert_dict['uv']
				#print(max(uvlist), mesh.name) if max(uvlist)>1.0 else 1

				#---big size uv, skip atlasing
				uvabsmax = max( max(uvlist), -min(uvlist) )
				#print(uvabsmax,mesh.name)
				if uvabsmax>1.01:
					meshes_left.append(mesh)#we do before continue
					continue
				#---prevent clip for uv 1.001
				elif uvabsmax>1.0 and uvabsmax<1.01:
					#print(mesh.name)
					uvlist_div = []
					for uvi in uvlist:						
						uvlist_div.append( uvi/uvabsmax )
					uvlist = uvlist_div					

				new_uvlist = []
				for i in range( len(uvlist)//2 ):
					u = uvlist[2*i+0]
					v = uvlist[2*i+1]				
					new_u = ox/SIZE+ u*w/SIZE
					new_v = oy/SIZE+ v*h/SIZE
					new_uvlist.append(new_u)
					new_uvlist.append(new_v)
				mesh.vert_dict['uv'] = new_uvlist

				meshes_atlas.append(mesh)
				#----and replace texture. we now all same texture!
				mesh.texture[channel] = atlasname		
		#return meshes
		return meshes_atlas, meshes_left

def merge(cls, meshes):
	new_mesh = Mesh()
	mesh1 = meshes[0]
	# 1,2,3, 4,5,6 is vert
	# 0,1,2, 0,1,2 is ind
	# 0,1,2, 3,4,5 is ind_fixed
	# 0,1,2, len(before)+..
	#we need to add: before points number.
	points_before = 0
	for mesh in meshes:
		for key, value in mesh.vert_dict.items():
			new_mesh.vert_dict[key].extend(value)

		#brute way
		for idx in mesh.indices:
			new_mesh.indices.append(idx+points_before)			
		points_before += len(mesh.vert_dict['position'])//3
	
	new_mesh.texture = mesh1.texture #since atlas, we do so.fine.
	new_mesh.shader = mesh1.shader
	new_mesh.path = mesh1.path #same, ofcourse.fine.
	new_mesh.modelname = mesh1.modelname #if from filename, same all. fine.
	new_mesh.name = mesh1.modelname #..is ..what? ..is no more useful. overwrite it.
	#self.modelname = ''#is from modelname.obj
	#self.path = '' #atlas, merge, only same path.
	#self.name = '' #name = part of modelname.obj
	#self.texture = {}# starting diffuse
	#self.shader = {}#both loaded while GL runnin
	return new_mesh

def sort_bysize(cls, meshes):				
	fdir_dict = {}
	def img_height(mesh):
		fname = mesh.texture['diffuse']
		fdir = join(mesh.path,fname)

		try:
			#--------img
			img = Image.open(fdir)
			#print( img.size)
			w,h = img.size
			#fdir_dict[mtl] = h
			img.close()
			#--------img
		except:
			h=123

		return h
	sorted_meshes = sorted(meshes, key=img_height )
	return sorted_meshes
	#sorted_meshes = sorted(meshes, key=lambda mesh: mesh.height )
	#sorted_mtl = sorted(fdir_dict, key=lambda k: fdir_dict[k] )
#============================================================




def add_vertex(line, vert_dict, idxlist ):
	"""if new, add dict, append idx. if old, get idx, append idx. """
	#x,y, *a = (1,2,3,4) works!
	pbone, x,y,z, nx,ny,nz, u,v, links, *args = line.split()
	assert pbone == '0' #or xyz+=pxyz
	vert_data = [pbone, x,y,z,nx,ny,nz,u,v, links]
	
	iters = len(args)//2 #0 if [0]
	for i in range(iters):
		boneID, weight = args[0+i], args[1+i]
		vert_data.append(boneID)
		vert_data.append(weight)

	key = tuple(vert_data)#one vert, one stored.
	if key in vert_dict:
		idx = vert_dict[key]
	else:
		#idx = len(idxlist) #if [0,1,2], now 3. ..  [0, 1, 2, 0, 2, 5]!huh.
		if len(idxlist) != 0:
			idx = max(idxlist)+1
		else:
			idx=0
		vert_dict[key] = idx
	
	idxlist.append(idx)#its stride =3.fine.



def triangles_load(lines, pointer, END):
	pp = 0
	tris = {}
	while True:
		line = lines[pointer].strip()
		if line == END:
			break
		mtl = lines[0+pointer].strip()
		a = lines[1+pointer].strip()
		b = lines[2+pointer].strip()
		c = lines[3+pointer].strip()

		if not mtl in tris:
			tris[mtl] = {'vertices':{}, 'indices':[] }
		vert_dict = tris[mtl]['vertices']
		idxlist = tris[mtl]['indices']
		add_vertex(a, vert_dict, idxlist)
		add_vertex(b, vert_dict, idxlist)
		add_vertex(c, vert_dict, idxlist)
		pointer+=4
		pp+=1

	tris_list = []
	for mtl, xxx in tris.items():
		vgroup = {
		'vertices': xxx['vertices'],
		'indices': xxx['indices'],
		'mtl': mtl
		}
		tris_list.append(vgroup)
	#print(pp,'pointsssssss')
	return tris_list, pointer



def sk_load(lines, pointer, END):
	#{ id:{name,parent} }
	skeleton = {}
	while True:
		line = lines[pointer].strip()
		if line == END:
			break
		#0 "L_Cool_00_rousoku" -1
		#boneID, bonename, parent
		boneID, bonename, parent = line.split()
		ID = int(boneID)
		name = bonename.replace('"','')# '"name"'
		parentID = int(parent)
		skeleton[ID]= {'name':name,'parent':parentID}#least info rule.		
		pointer+=1
	return skeleton,pointer#now it became very clear!


def euler_to_quat(roll,pitch,yaw):#rpy xyz
	cy = cos(yaw * 0.5)
	sy = sin(yaw * 0.5)
	cp = cos(pitch * 0.5)
	sp = sin(pitch * 0.5)
	cr = cos(roll * 0.5)
	sr = sin(roll * 0.5)

	qw = cr * cp * cy + sr * sp * sy
	qx = sr * cp * cy - cr * sp * sy
	qy = cr * sp * cy + sr * cp * sy
	qz = cr * cp * sy - sr * sp * cy
	return [qx,qy,qz,qw]#not tuple. for json


def skam_load(lines, pointer, END):	
	skam = {}
	bonedict = {}
	frame_now = 0
	while True:
		line = lines[pointer].strip()
		if line == END:
			skam[frame_now] = bonedict
			break
		if line.startswith('time'):
			nah,frame = line.split()
			frame = int(frame)
			frame_now = frame
			if not bonedict == {}:
				skam[frame] = bonedict
				bonedict = {}
			pointer+=1
			continue
		#time 0
		#0 0 0 0 0 0 0
		#id x y z a b c
		boneID, x,y,z,a,b,c = line.split()
		ID = int(boneID)
		x,y,z, a,b,c = map(float, (x,y,z,a,b,c) )
		rx,ry,rz,rw = euler_to_quat(x,y,z)
		posedata = {'trans':[x,y,z], 'rot':[rx,ry,rz,rw]}
		bonedict[ID] = posedata
		pointer+=1	
	return skam,pointer


def smd_load(fdir, END = 'end'):
	return_tuple = {}
	

	path,file = split(fdir)
	files = os.listdir(path)

	with open(fdir,encoding='utf-8') as f:
		lines = f.readlines()	

	data_dict = {
	'sk':None,
	'skam':None,
	'triangles':None,
	}
	#parentbone, x,y,z,nx,ny,nz,u,v, links, boneID,weight,

	pointer = 0
	while pointer<len(lines):
		line = lines[pointer].strip()

		if line == 'nodes':
			pointer+=1
			data, pointer = sk_load(lines,pointer, END=END)
			data_dict[line] = data
		if line == 'skeleton':
			pointer+=1
			data, pointer = skam_load(lines,pointer, END=END)
			data_dict[line] = data
		if line == 'triangles':
			pointer+=1
			data, pointer = triangles_load(lines,pointer, END=END)
			data_dict[line] = data
		pointer+=1

	#================parse data.
	#--------bone
	nodes = data_dict['nodes']
	return_tuple['sk'] = nodes
	
	#--------skam
	skeletons = data_dict['skeleton']
	return_tuple['skam'] = skeletons	

	#---------------tri to mesh
	tris = data_dict['triangles']
	meshes = []
	for tri in tris:
		mtl = tri['mtl']
		vertices = tri['vertices'] # is (p,x,y,z,a,b,c,u,v,link):0 tuple.
		indices = tri['indices']

		mesh={}
		mesh['attributes']={}
		#mesh of {attributes:{position:,normal:,uv:,bones:,weights:}, indices:[], material:{ shader:,diffuse_0:,}}
		mesh['attributes']['position'] = []
		mesh['attributes']['normal'] = []
		mesh['attributes']['uv'] = []
		mesh['attributes']['bones'] = []
		mesh['attributes']['weights'] = []

		for vtuple in vertices:
			pbone, x,y,z, nx,ny,nz, u,v, *args = vtuple #args links, bId-w
			pbone = int(pbone)
			x = float(x)
			y = float(y)
			z = float(z)
			nx = float(nx)
			ny = float(ny)
			nz = float(nz)
			u = float(u)
			v = float(v)

			#----write data to mesh.

			mesh['attributes']['position'].extend([x,y,z])
			mesh['attributes']['normal'].extend([nx,ny,nz])
			mesh['attributes']['uv'].extend([u,v])

			iters = len(args)//2
			bones =[]
			weights = []
			for i in range(iters):
				boneID, weight = args[0+i], args[1+i]
				bones.append(boneID)
				weights.append(weight)
			if iters>0:
				mesh['attributes']['bones'].extend( bones )
				mesh['attributes']['weights'].extend( weights )

		mesh['indices'] = indices

		#virtual material. with texture..
		texture = {}
		texture['diffuse_0'] = mtl+'.png'
		#texture['diffuse'] = join(path, mtl+'.png' )
		#texture['diffuse'] = mtl+'.png' wrap kinds. all blank now.
		
		material = {}
		material['name'] = mtl
		material['shader'] = 'default'
		material['texture'] = texture
		mesh['material'] = material
		
		head, ext = splitext(file)
		#mesh.modelname = head
		#mesh.name = mtl #we have only this clue. ..smd assume mat.name is name..
		#mesh.path = path
		meshes.append(mesh)
	return_tuple['meshes'] = meshes
	
	return return_tuple


dirname = 'tutuL_Cool_00'
fname = 'L_Cool_00_bg.smd'
fname = 'L_Cool_00_rousoku.smd'
#fname = 'L_Cool_00_rousoku_skam.smd'


dirname = 'summers'
fname = 'DR_P00_CUN01_T.smd'

fdir = join(dirname,fname)
loaded = Mesh.load_smd(fdir)

print('----------meshes--------')
meshes = loaded['meshes']
for i in meshes:
	print(i)
	#print(i.attributes)
	position = i['attributes']['position']
	normal = i['attributes']['normal']
	uv = i['attributes']['uv']
	#print(i.attributes)
	print(len(i['indices']),'i')

	print(i['material'],'m')

	#print(i.)

print('----------bones--------')
sk = loaded['sk']#list
print(sk)

print('----------skams--------')
skam = loaded['skam']# { frame: [bones] ,}
print(skam)
skam = skam[0]

class Bone:
	def __init__(self, ID,name,parent, x,y,z,a,b,c):
		#note if AXIS, bone nomore. bones ==axis. fine.
		self.ID = ID
		self.name = name
		self.parent = parent #not ID. oop.

		self.pos = (x,y,z)
		self.rot = (a,b,c)
		#self.scale = None
	def get_pos(self):
		return self.pos
	def set_pos(self, pos):
		self.pos = pos#quite oop..
	def get_pos_abs(self,absdict=None):#automatically updates all..
		# 1. if alreadydone, return that
		# 2. if parent, get and addit.
		# 3. when add, if dict,add. and return.
		if absdict:
			value = absdict.get(self.ID)
			if value:
				return value
		pos = self.pos
		if self.parent:
			pos += parent.get_pos_abs(absdict) #chain works!			
		if absdict:
			absdict[self.ID] = pos
		return pos

class Skeleton:
	def __init__(self):
		self.bonedict = {}# for ID contact.
	#def draw(self, shader=shader_default):
	#def update(self,data) it shall not parse data.
	def xxxget_pos_abs(self):
		absposdict={}
		for ID ,bone in self.bonedict.items():
			bone.get_pos_abs(absposdict)
	def xxxupdate_abs(self):#not here. since if sk is AXIS.. skam need to know it.
		absposdict={}
		for ID ,bone in self.bonedict.items():
			bone.update_pos_abs(absposdict)
	def draw(self):#finally! it treated like mesh.
		1#get_pos_abs
	def __repr__(self):
		return f"Skeleton bones: {len(self.bonedict)}"
	def add_bone(self,ID,name,parentID, trans, rot, scale=[1,1,1] ):
		"""trans [0,0,0] rot[0,0,0,1]"""
		self.bonedict[ID] = {
		'name':name,
		'parent':parentID,
		'trans':trans,
		'rot':rot,
		'scale':scale,
		'trans_init':trans,
		'rot_init':rot,
		'scale_init':scale,
		}
	def add_sk(self, sk_dict):
		"""sk_dict {id:{name:,parent:,trans:,rot:}}"""
		for id, data in sk_dict:
			name = data['name']
			parent = data['parent']
			trans = data.get('trans',[0,0,0])
			rot = data.get('rot',[0,0,0,1])
			scale = data.get('scale',None)
			self.add_bone(id, name,parent,trans,rot,scale)
	def pose_reset(self):
		for ID in self.bonedict:
			self.bonedict['trans'] = self.bonedict['trans_init']
			self.bonedict['rot'] = self.bonedict['rot_init']
			self.bonedict['scale'] = self.bonedict['scale_init']
	def pose_bone(self,id, trans,rot,scale=[1,1,1] ):
		bone = self.bonedict.get(id)
		if bone:
			bone['trans'] = trans
			bone['rot'] = rot
			bone['scale'] = scale
	def pose_sk(self,pose_dict):
		for id, data in pose_dict:
			trans = data.get('trans',[0,0,0])
			rot = data.get('rot',[0,0,0,1])
			scale = data.get('scale',None)
			self.pose_bone(id,trans,rot,scale)

s=Skeleton()


class Animator:
	def __init__(self):
		self.targets = []
	def tick(self,dt):
		for target in self.targets:
			self.update(target, dt)#target don't know what data type is.
	def add_target(self,target):
		self.targets.append(target)
	def update(self,target,dt):#can be redefine and bond out of class.
		pass

class Animator_skam(Animator):
	def __init__(self):
		super().__init__()
		self.time = 0
		self.data = {}#of {id:{trans:,rot:}}

	def set_data(self,data):
		self.data = data
	def tick(self,dt):
		self.time+=dt
		frame = self.time//1000# 1000ms changes int++
		pose_dict = self.data.get(frame)
		if not pose_dict:#no frame.
			return
		for target in self.targets:
			target.pose_sk(pose_dict)
		# for ID ,data in pose_dict.items():
		# 	trans = data.get('trans',[0,0,0])
		# 	rot = data.get('rot',[0,0,0,1])
		# 	target.pose_bone(ID,trans,rot)
	#def update(self,dt):



#---3rd day
ss=Skeleton()

for ID in sk:
	bone = sk[ID]
	name, parentID = bone
	posedict = skam[ID]
	trans = posedict['trans']
	rot = posedict['rot']
	ss.add_bone(ID,name,parentID, trans, rot)
	#ss.add_sk(ID,name,parentID, trans, rot)

print(ss)
exit()

#---3rd day, done sk, skam.

#--------after 2 days.
#animator
#def update, knows data, what to do, target. target-specific func.
#hopely it expends to actor animator, cam animator..fine.
#just it's for bone, now.
#AND tict(dt), internally update. fine.


#===============dict cache way. quite hard to understand. deprecate.
# abspos = {}
# absrot = {}

# def get_abs_pos(ID):
# 	pos = abspos.get(ID)
# 	if not pos:	
# 		set_abs_pos(ID)
# 		pos = abspos.get(ID)
# 	return pos

# def set_abs_pos(ID):
# 	bone = dict[ID]
# 	parentID = bone.parentID
# 	if parentID:
# 		parent_pos = get_abs_pos(parentID)
# 		if parent_pos:
# 			bone.pos += parent_pos
# 	abspos[ID] = bone.pos



actor = Actor()

meshes = loaded['meshes']
for i in meshes:	
	actor.meshes.append(i)

skeleton = Skeleton()
skeleton.add_bone(id,name,parent,trans,rot)
#skeleton.draw()no, actor only has 3d position.

#=--Actor
#draw in actor
modelmat = actor.get_modelmat()
for mesh in actor.meshes:
	1
	#mesh.draw(),actor has only 3d position.

#actor.sk.draw() a skeleton may be drawn, but requires modelmat..

skam = Animator_skam()
skam.set_data(parsed_sk_dict)
skam.add_target(sk)
skam.tick(dt)


#world.render
#or world.draw() ..draw fine.. but may mixed. yeah.

#world.renderer
#renderer.render() #full gpu things..?


"""
world.update(dt)
-> input, simulate, draw
world.input_process() - via event? or stack..?
world.simulate()
world.draw()

def draw
world.level
world.actor
world.actorlist

for actor in world.actors
    actor.draw()
-oldway.
texture, modelmat, shader, vao..
actor binds all to gpu, and drawcall.

for actor in world.actors
    #renderer.append(actor) #we do every time?? ..yeah. we give list of actor. ..ormesh.
    for mesh in actor.meshes:
    	renderer.append(mesh) #thisway, rendererrenders mesh.
renderer.render()
-newway, but too complex.? ..not that!

renderer all draws, mesh. 3dmesh. it's fixed. fine.
whatabout 2d gui?? or called.. hud.

hud drawn before world. since world is 3dworld. fine.

renderer only renders mesh?? it seems fine, since all actor is drawn. actor has mesh..
we not allow another type of , 3dobject, which requires modelmat, means actor..

yeah.
mesh drawn.

mesh and just drawn.
mesh updated before draw phase.

renderer sorts all meshs list,
mesh has it's shader, texture, vao,
we can sort, and draw.

whatabout instanced..?
actually instanced requires another shader, uniform value.

if mesh.isinstanced:
	parentid = mesh.instanceID


..we did,instanced..draw...
..rememder.. actor_instanced.draw()...
it also automatically shaders..?

..we need actor.draw() also.
for: if instanced, draw first.
see , actor_instanced.draw() how simple it is.
actor has it's own shader, vao, texture,, all oneshot process.

and left actor(s) drawn sorted. fine.  ..or one-each.

renderer became too smaller.. just sort-draw-er.


anyway,backto bone anim.

draw draws which requires drawn.

--actor.draw()
actor.shader.bind()
modelmat = actor.get_modelmat()
actor.shader.set_modelmat(modelmat)
actor.shader.set_uniform("modelmat", modelmat) #thats the form! we can keep understanding.

actor.texture.bind()-old 1texture way. we cannot do this. however it's so fancy, fastest, easy to understanding.

#--- also actor may store lots of vao.. mesh actually.
actor.vao.bind()
actor.vao.draw()

so we need to draw mesh, which stores vao,texture, mat.. yeah.

we need Material.

and shader, there was shader for gpu.
shader.bind()

GL_shader
GL_texture
GL_Texture
GLTexture

shader, vao, texture
..isit all?
yeah.

texture requires complex export, or import, or,.. 
...means texture is texture. not much.

shader, also.

what if..
sha = Shader_uvanim()

sha.set_uniform('uvoffset',xxx)

if shader is ..for instanced -yeah
shader for uvanim
shader for skam
shader for color RGB changer! neon! ..possible.

...maybe, mesh dose not calls material, shader..? no!
even mesh has it's own mat, we override, thats why seen trans-effect kinds situation.

..yeah we can expend shader, fine.


------------------- back to skam again(2)

---
renderer:
for mesh in meshes:
	if mesh.isinstanced:
		id = mesh.instanceID
		instanced[id].append(mesh)
NO! mesh not stores modelmat. it's clear.
..or stores modelmat.

----
for actor in world.actors:	
	modelmat = actor.get_modelmat()

whatif, instanced actor? actor,, has a, A position. yeah.

AND, if we use AXIS, .. it shall be draw by:
actor_axis.draw()
.fine. it shall be drawn it's own way.

id = actor.instanceof

#==== if axis, draw.  notvisible, not draw. isskipdraw?? too long..
# if , instanced, we gether, and draw once. how??

instanced={}
id = actor.instanceID
instanced[id] = actor #actgually we nmeed mesh_instanced. not actor.

else:
	renderer.append(actor)

for actor in world.actors:
	if actor.isAXIS:
		actor.draw()
	elif not actor.isvisible:
		continue#skip, next!
	elif actor.


"""