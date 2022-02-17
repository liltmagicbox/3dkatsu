from PIL import Image
from os.path import join, split

#smdreader. now tris only. smd has:[ vertex-mtl ..]. same mtl, same vert.


#mesh = SMD.load(fdir)

#mesh.save_obj(fname)


#mesh.to_atlas()
#mesh.merge()
#mesh.save_atlas()


#meshes = []

class Mesh:
	""" python object for internal usage ..and little to glTF"""
	@classmethod
	def from_smd(cls, fdir):
		resultdict = load_smd(fdir)
		return resultdict['meshes'] #of Mesh.

	@classmethod
	def from_obj(cls, fdir):
		1
		#resultdict = load_smd(fdir)
		#return resultdict['meshes'] #of Mesh.

	def save_obj(self, fdir):
		sevasu
	
	@classmethod
	def atlas(cls, meshes):
				

	@classmethod
	def sort_bysize(cls, meshes):				
		fdir_dict = {}
		def img_height(mesh):
			mtl = mesh.material
			fname = f"{mtl}.png"

			fdir = join(mesh.path,fname)
			img = Image.open(fdir)
			#print(mtl, img.size)
			w,h = img.size
			#fdir_dict[mtl] = h
			img.close()
			return h
		sorted_meshes = sorted(meshes, key=img_height )
		return sorted_meshes
		#sorted_meshes = sorted(meshes, key=lambda mesh: mesh.height )
		#sorted_mtl = sorted(fdir_dict, key=lambda k: fdir_dict[k] )

	
	def __init__(self):
		self.vert_dict = {}		
		self.vert_dict['parent_bone'] = []
		self.vert_dict['position'] = []
		self.vert_dict['normal'] = []
		self.vert_dict['uv'] = []
		self.vert_dict['weights'] = []
		self.indices = []
		self.material = None
		self.path = ''







def add_vertex(line, vert_dict, idxlist ):
	"""if new, add dict, append idx. if old, get idx, append idx. """
	#x,y, *a = (1,2,3,4) works!
	pbone, x,y,z, nx,ny,nz, u,v, links, *args = line.split()
	assert pbone == '0' #or xyz+=pxyz
	vert_data = [pbone, x,y,z,nx,ny,nz,u,v, links]
	
	iters = len(args)//2
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



def triangles_load(lines, pointer, END = 'end'):
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






def load_smd(fdir, END = 'end'):
	path,file = split(fdir)

	with open(fdir,encoding='utf-8') as f:
		lines = f.readlines()	

	data_dict = {
	'nodes':None,
	'skeleton':None,
	'triangles':[],
	}
	#parentbone, x,y,z,nx,ny,nz,u,v, links, boneID,weight,

	pointer = 0
	while pointer<len(lines):
		line = lines[pointer].strip()

		#if line == 'nodes':
		#if line == 'skeleton':
		if line == 'triangles':
			pointer+=1
			tris, pointer = triangles_load(lines,pointer)
			data_dict[line] = tris
		pointer+=1


	#---------------tri to mesh
	tris = data_dict['triangles']
	meshes = []
	for tri in tris:
		mtl = tri['mtl']
		vertices = tri['vertices'] # is (p,x,y,z,a,b,c,u,v,link):0 tuple.
		indices = tri['indices']

		mesh = Mesh()

		for vtuple in vertices:
			pbone, x,y,z, nx,ny,nz, u,v, *args = vtuple #args links, bId-w
			mesh.vert_dict['parent_bone'].append(pbone)
			mesh.vert_dict['position'].extend([x,y,z])
			mesh.vert_dict['normal'].extend([nx,ny,nz])
			mesh.vert_dict['uv'].extend([u,v])
			mesh.vert_dict['weights'].append(args)#remain thisway.

		mesh.indices = indices
		mesh.material = mtl
		mesh.path = path
		meshes.append(mesh)

	return_tuple = {}
	return_tuple['meshes'] = meshes
	return return_tuple



dirname = 'test'
fname = 'ST_FA_03_CU01_conv.smd'
#fname = 'CH_HYUM.smd'

fdir = join(dirname,fname)

meshes = Mesh.from_smd(fdir)
#print(meshes[:5])
meshes = Mesh.sort_bysize(meshes)
#print(meshes[:5])

Mesh.atlas(meshes)

exit()


#----------------------------------------------atlasing

# fdir_dict = {}
# #print(data_dict)
# for pri in data_dict['triangles']:
# 	mtl = pri['mtl']
# 	fname = f"{mtl}.png"
# 	fdir = join(dirname,fname)
# 	img = Image.open(fdir)
# 	print(mtl, img.size)
# 	w,h = img.size
# 	fdir_dict[mtl] = h
# 	img.close()

# sorted_mtl = sorted(fdir_dict, key=lambda k: fdir_dict[k] )


SIZE = 2048
w_before =0
h_before =0
cc=0
atlas = Image.new('RGBA', (SIZE,SIZE) )

coord_dict = {}

for mtl in sorted_mtl:
	fname = f"{mtl}.png"
	fdir = join(dirname,fname)
	img = Image.open(fdir)
	w,h = img.size	
	if w_before + w <= SIZE:
		#atlas.paste(img, (w_before,h_before ) )
		imgxa,imgya, imgxb,imgyb = (w_before,SIZE-h_before-h, w_before+w, SIZE-h_before)
		atlas.paste(img, (imgxa,imgya, imgxb,imgyb) )
		cc+=1

		offset_x,offset_y,width_x,width_y = w_before,h_before, w,h
		coord_dict[mtl] = (offset_x,offset_y,width_x,width_y)

		w_before+=w#note it's last line

	else:
		w_before=0
		h_before+=h
		if h_before + h <= SIZE:
			#atlas.paste(img, (w_before,h_before) )
			imgxa,imgya, imgxb,imgyb = (w_before,SIZE-h_before-h, w_before+w, SIZE-h_before)
			atlas.paste(img, (imgxa,imgya, imgxb,imgyb) )
			cc+=1
			
			offset_x,offset_y,width_x,width_y = w_before,h_before, w,h
			coord_dict[mtl] = (offset_x,offset_y,width_x,width_y)
		else:
			print('size over!')
	img.close()

print(cc,'of texture merged')

atlas.save('ham.png')

#----------------------------------------------atlasing



#================================coord uv mixmix

#{
#	mtlname : array, idx
#}

meshes = []

for pri in data_dict['triangles']:
	mtl = pri['mtl']
	ox,oy, w,h = coord_dict[mtl]
	aaaa=[]
	for vtuple in pri['vertices']: #hope idx ordered. 0 to n
		pbone, x,y,z, nx,ny,nz, u,v, *args = vtuple #args links,bId,w
		#aaaa.extend( [x,y,z, nx,ny,nz, u,v] )
		pbone = int(pbone)
		x = float(x)
		y = float(y)
		z = float(z)
		nx = float(nx)
		ny = float(ny)
		nz = float(nz)
		u = float(u)
		v = float(v)
		
		new_u = ox/SIZE+ u*w/SIZE
		new_v = oy/SIZE+ v*h/SIZE

		#aaaa.extend( [x,y,z, nx,ny,nz, new_u, new_v] )
		aaaa.extend( [x,y,z, new_u, new_v] )
	vertarr = aaaa
	idxarr = pri['indices']
	#vertarr = np.array( aaaa , dtype='float32')
	#idxarr = np.array( pri['indices'] , dtype='float32')

	meshes.append(  {'vertices':vertarr, 'indices':idxarr, 'material':mtl }  )

#('-18.88304', '-2.020091', '24.99999', '0', '0', '0', '7.00522', '0.00521559'): 0,
#('-18.88304', '7.586056', '12.19193', '0', '0', '0', '8.32871', '0.997821'): 1,
#('-18.88304', '7.58601', '25.00003', '0', '0', '0', '7.00522', '0.997821'): 2,

#'Stage_Fashion_03_cute_001_lampB_light02': {'vertices': [3.

#print(meshes)
#[{'vertices': [0.146], 'indices':idxarr, 'material':mtl]

vert_max = []
ind_max = []

for mesh in meshes:
	vertarr = mesh['vertices']
	indarr = mesh['indices']
	mat = mesh['material']

	vert_max.extend(vertarr)
	ind_max.extend(indarr)




#---------------for line iter way. we don't useit.
# mode = 'triangles'
# end = 'end'

# modestack = []
# mode = None

# if line == 'version':
# 	break
# elif line == 'end':
# 	modestack.pop()
# 	break
# elif line == 'nodes':
# 	modestack.append(line)
# 	break
# elif line == 'skeleton':
# 	modestack.append(line)
# 	break
# elif line == 'triangles':
# 	modestack.append(line)
# 	break

# if len(modestack)==0:
# 	break
# else:
# 	mode = modestack[-1]

# if mode = 'triangles':
# 	if len(line.split())==1:#assume mtl
# 		mtl = line
# 	else:
# 		add_vertex(line)
