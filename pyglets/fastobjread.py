#objreader my simply

filename = 'objs/cubemap/cubemap.obj'

stack = []

#https://github.com/yarolig/OBJFileLoader/blob/master/OBJFileLoader/objloader.py

class Obj:
    def __init__(self,filename):
        
        self.vertices = []
        self.uvs = []
        self.normals = []
        
        self.faces = []
        #for each face
        self.materials = []
        self.mtllib = ''
        self.objects = []

    for line in open(filename, 'r', encoding = 'utf-8'):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        
        if values[0] == 'mtllib':
            matname = values[1]
            self.mtllib = matname

        elif values[0] == 'o':
            objectname = values[1]
            self.objects.append(objectname)
        
        elif values[0] == 'v':
            v = list(map(float, values[1:]))
            self.vertices.append(v)
        elif values[0] == 'vt':
            uv = list(map(float, values[1:]))
            self.uvs.append(uv)
        elif values[0] == 'vn':
            normal = list(map(float, values[1:]))
            self.normals.append(normal)


        elif values[0] == 'g':
            group = values[1]
        elif values[0] == 'usemtl':
            material = values[1]
        elif values[0] == 's':
            smoothing = values[1]

        elif values[0] == 'f':
            vert = []
            tex = []
            norm = []
            for v in values[1:]:#usually 3 items.
                #vertex, vertex/texture, vertex/texture/normal, vertex/normal
                w = v.split('/')
                if len(w)==1:#vertex only
                    vert.append(w[0])
                elif len(w)==2:
                    vert.append(w[0])
                    norm.append(w[1])
                elif len(w)==3:
                    vert.append(w[0])
                    tex.append(w[1])
                    norm.append(w[2])
            
            vert = list(map(float, vert))
            tex = list(map(float, tex))
            norm = list(map(float, norm))
                        # face = {
            # 'material':material,
            # 'smoothing':smoothing,
            # 'vert':vert,
            # 'tex':tex,
            # 'norm':norm,
            # }
            face = [group, material, smoothing, vert,tex,norm]
            self.faces.append(face)
    
    #---for line end.
    
