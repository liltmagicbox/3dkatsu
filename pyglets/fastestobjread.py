#objreader my simply

filename = 'objs/cubemap/cubemap.obj'


#https://github.com/yarolig/OBJFileLoader/blob/master/OBJFileLoader/objloader.py

class OBJ:
    def __init__(self,filename):
        self.idxs = []
        self.multices = []

        #one model, one mat, one texture!
        #faces only contains index of vertices.
        # a point, created by vert,uv,norm is.
        #I named it multi-vertex, multex. and multices.        
        verts = []
        uvs = []
        norms = []

        counter = 0

        for line in open(filename, 'r', encoding = 'utf-8'):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            
            if values[0] == 'mtllib':
                matname = values[1]
                #self.mtllib = matname

            elif values[0] == 'o':
                objectname = values[1]
                #self.objects.append(objectname)
            
            elif values[0] == 'v':
                vert = list(map(float, values[1:]))
                verts.append(vert)
            elif values[0] == 'vt':
                uv = list(map(float, values[1:]))
                uvs.append(uv)
            elif values[0] == 'vn':
                norm = list(map(float, values[1:]))
                norms.append(norm)


            elif values[0] == 'g':
                group = values[1]
            elif values[0] == 'usemtl':
                material = values[1]
            elif values[0] == 's':
                smoothing = values[1]

            elif values[0] == 'f':
                for v in values[1:]:#usually 3 items.
                    #vertex, vertex/texture, vertex/texture/normal, vertex/normal
                    w = v.split('/')

                    if len(w)== 3:                        
                        vert_idx, uv_idx, norm_idx = map(int, w)                        
                        
                        vert = verts[vert_idx-1]
                        uv = uvs[uv_idx-1]
                        norm = norms[norm_idx-1]

                        multex = (vert,uv,norm)
                        if multex in self.multices:
                            pass
                        else:
                            self.multices.append(multex)
                        index = self.multices.index(multex)
                        self.idxs.append(index)
            counter+=1
            if counter%1000 == 1:
                print('l',end='')

                # face = {
                # 'material':material,
                # 'smoothing':smoothing,
                # 'vert':vert,
                # 'tex':tex,
                # 'norm':norm,
                # }
        
        #---for line end.

#smd format
#? vx vy vz / uu uv / nx ny nz / N b1 b2 b3 b4

def newmult(vert,uv,norm):
    return (vert,uv,norm)
    #or dict

if __name__ == '__main__':
    obj = OBJ(filename)
    print(obj.idxs)
    print(len(obj.multices))