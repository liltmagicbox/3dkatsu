
#this can d.clickable, copy paste, search-able, and looks like not py-native.
from glfw.GLFW import *
#not import glfw.

#this way,
#format of  func(attr1,attr2)
#of yml
"""
funcname:
  attr1:attr2
"""
#very specific, not general.

def gltest():
    glfwInit()
    for key, value in d.items():
        func = locals()[key]
        for target,value in value.items():
            target = locals()[target]
            #glfwWindowHint(GLFW_CENTER_CURSOR,1)
            func(target,value)



import configparser

class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
    def save(self, fdir):
        with open(fdir, 'w', encoding='utf-8') as f:
            self.write(f)
    def load(self, fdir):
        self.read(fdir)
    def to_dict(self):
        """{section:{key:value} }"""
        cdict={}
        sections = self.sections()#no DEFAULT!
        for section in sections:
            cdict[section] = {}
            keys = list(self[section])
            for key in keys:
                value = self[section][key]
                cdict[section][key]=value
                #x = self.getboolean(section,key)
                #getint()와 getfloat()
        return cdict
    def from_dict(self, cdict):
        for section in cdict:
            self[section] = {}
            for key in cdict[section]:
                value = cdict[section][key]
                self[section][key] = value

def configtest():
    c = Config()
    ff = r'C:\Users\liltm\Desktop\config.ini'
    c.load(ff)
    dd = c.to_dict()
    print(dd)

    cc = Config()
    cc.from_dict(dd)
    cc.save(r'C:\Users\liltm\Desktop\config2.ini')

#xx = c['glfwWindowHint']['GLFW_DECORATED']
#print(type(xx) )#str. not int
#we know sections, same sections, same data type...?
#or we know exactly, intentionally use.

#print(list(c))#.to_dict()['glfwWindowHint']))
#print(c.sections())
