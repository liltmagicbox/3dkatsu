from PIL import Image
from os.path import join, split, splitext
import os

#smdreader. now tris only. smd has:[ vertex-mtl ..]. same mtl, same vert.


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

	@classmethod
	def save_obj(cls, meshes, fdir):
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
	
	@classmethod
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





	@classmethod
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

	@classmethod
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

	
	def __init__(self):
		self.modelname = ''#is from modelname.obj
		self.path = '' #atlas, merge, only same path.
		self.name = '' #name = part of modelname.obj

		#attributes can be vary.
		self.vert_dict = {}
		self.vert_dict['position'] = []
		self.vert_dict['normal'] = []
		self.vert_dict['uv'] = []
		
		self.indices = []

		self.texture = {}# starting diffuse
		self.shader = {}#both loaded while GL running
		







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
	files = os.listdir(path)

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
			mesh.vert_dict['position'].extend([x,y,z])
			mesh.vert_dict['normal'].extend([nx,ny,nz])
			mesh.vert_dict['uv'].extend([u,v])			

		mesh.indices = indices
		#smd single png assume.fine.
		# for file in files:
		# 	fonly = splitext(file)[0]
		# 	meshname = fonly.split('_')[0] #body_diffuse.jpg or body.png . not model_body_dif
		# 	if mtl == meshname:
		# 		print('yeah',mtl)			
		#print( mtl+'.png' in files, mtl)
		mesh.texture['diffuse'] = mtl+'.png'
		
		head, ext = splitext(file)
		mesh.modelname = head
		mesh.name = mtl #we have only this clue.
		mesh.path = path
		meshes.append(mesh)		

	return_tuple = {}
	return_tuple['meshes'] = meshes
	return return_tuple



dirname = 'tutuL_Cool_00'

#fname = 'ST_FA_03_CU01_conv.smd'
fname = 'L_Cool_00_bg.smd'
#fname = 'ST_FA_03_CU01_base.smd'
#fname = 'CH_HYUM.smd'
#fname = 'DR_DEF_YUM_A.smd'

#fname = 'DR_H02_SEP01_B.smd'
fdir = join(dirname,fname)

meshes = Mesh.from_smd(fdir)
#for m in meshes:print(m.texture)
#print(meshes[:5])
meshes = Mesh.sort_bysize(meshes)
#print(meshes[:5])

#Mesh.save_obj([meshes[0]], 'test\\harrr.obj')
#Mesh.save_obj(meshes, 'test\\harrr.obj')

#for i in meshes:
#	print(i.name)

#meshes = Mesh.atlas(meshes)# mesh UV offset,resized.
#Mesh.save_obj(meshes, f'test\\xxxxx.obj')

#mesh = Mesh.merge(meshes)#atlas ed -> single mesh, finally.
#Mesh.save_obj([mesh], f'test\\{mesh.name}.obj')


#we merge only atlased. fine. and after save input is list!
ated,noted = Mesh.atlas(meshes)# mesh UV offset,resized.
mesh_ated = Mesh.merge(ated)

#--------if you want atlasted and left
wanna_save_all = True

if wanna_save_all:
	noted.append(mesh_ated)
	Mesh.save_obj(noted, f'{dirname}\\{mesh_ated.name}.obj')
else:	
	Mesh.save_obj([mesh_ated], f'{dirname}\\{mesh_ated.name}.obj')


print('saved : ',f'test\\{mesh_ated.name}.obj')



# print(dir(mesh))
# print(mesh.vert_dict)
# print(mesh.indices)
# print(mesh.name)
# print(mesh.modelname)
# print(mesh.path)
# print(mesh.shader)
# print(mesh.texture)