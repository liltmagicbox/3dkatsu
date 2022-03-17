def get_namekey(namedict, name):
	if name in namedict:
		baridx = name.rfind('_')
		if baridx == -1:
			name = name+'_0'
			name = get_namekey(namedict,name)
		else:
			front = name[:baridx]
			back = name[baridx+1:]
			if back.isdecimal():#digit 3^3, numeric 3.3E06
				i = int(back)+1
				name = f"{front}_{i}"
				name = get_namekey(namedict,name)
			else:
				name = name+'_0'
				name = get_namekey(namedict,name)
	return name

"""
#---namedict ver 0.2
    namedict = {}
    @classmethod
    def get(cls, name):
        if not 'default' in cls.namedict:            
            cls.default()
        return cls.namedict.get(name)
    @classmethod
    def set(cls, name: str, item) -> str:
        name = get_namekey(cls.namedict,name)
        cls.namedict[name]=item
        return name
    @classmethod
    def default(cls):
       cls('default')
"""