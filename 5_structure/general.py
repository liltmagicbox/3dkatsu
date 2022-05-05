#1.make here
#2. if too big, split.

from yamldict import YAML


import uuid
class Uuid:
    """use UUID = Uuid(). since it holds data.."""
    def __init__(self):
        self.dict = {}
    def get(self, key):
        return self.dict.get(key, None)
    def set(self,item):
        key = str(uuid.uuid4())
        self.dict[key] = item
        return key
    def delete(self,key):
        if key in self.dict:
            self.dict.pop(key)

class Name:
    """name by class. use NAME=Name()
    maxN. but when _2max, del _2 new is _2 not _3."""
    def __init__(self):
        self.dict = {}# key clsname.
    def get(self, key):
        clsname, _ = key.split('_')
        return self.dict[clsname].get(key)
    def set(self,item):
        SELFDICT = self.dict
        clsname = item.__class__.__name__.lower()
        if not clsname in SELFDICT:
            SELFDICT[clsname] = {}        
        key = clsname+'_0'
        if key in SELFDICT[clsname]:
            nums = [int(key.split('_')[1]) for key in SELFDICT[clsname].keys()]
            newnum = max(nums)+1
            key = clsname+'_'+str(newnum)

        self.dict[clsname][key] = item
        return key
    def delete(self,key):
        clsname, _ = key.split('_')
        if key in self.dict[clsname]:
            self.dict.pop(key)


from matplotlib import pyplot as plt

class Plotter:
    def __init__(self):
        1
    def plot(self, X,Y=None,Z=None):
        if Y==None:
            Y = X
            X = [i for i in range(len(Y))]
        #plt.plot(X,Y, 'r-o')
        plt.plot(X,Y, 'ro')
    def show(self):
        plt.show()
    def save(self, fdir):
        plt.savefig(fdir, dpi=96)#96bad
        #plt.savefig('Customed Plot.pdf', dpi=300, bbox_inches='tight')
    def title(self,text):
        plt.title(text)
    def xlabel(self,text):
        plt.xlabel(text)
    def ylabel(self,text):
        plt.ylabel(text)
        
    @classmethod
    def sample(cls):
        X = [0,1,2,3,4,5]
        Y = [0,1,2,3,4,9]
        return cls.__init__(X,Y)


# matplotlib.pyplot.savefig(fname, 
#         dpi=None, 
#         facecolor='w', 
#         edgecolor='w',
#         orientation='portrait', 
#         papertype=None, 
#         format=None,
#         transparent=False, 
#         bbox_inches=None, 
#         pad_inches=0.1,
#         frameon=None, 
#         metadata=None)

from time import perf_counter
def timef():
    return perf_counter()

class Clock:
    def __init__(self):
        self.timewas = perf_counter()
    def dt():
        timenow = perf_counter()
        dt = timenow-self.timewas
        self.timewas = timenow
        return dt

#import datetime
import time
#time.strftime('%c', time.localtime(time.time()))
#localt = time.localtime()
#tm_year=2022, tm_mon=5, tm_mday=3, tm_hour=19, tm_min=52, tm_sec=9,
#tm_wday=1, tm_yday=123, tm_isdst=0)
# year = localt.tm_year
# mon = localt.tm_mon
# mday = localt.tm_mday
# hour = localt.tm_hour
# min = localt.tm_min
# sec = localt.tm_sec

def get_tstr():    
    return time.strftime('%p %I:%M:%S 20%y-%m-%d', time.localtime())
    #'PM 08:12:55 / 2022-05-03'

class Logger:
    def __init__(self,print=False):
        self.logs=[]
        self.print_log = print
    def log(self, *text):
        """general log"""
        head = 'LOG'
        self.add(head, text)
    def Exception(self, *text):
        head = 'Exception'
        self.add(head, text)
        print('$$$$$$$$$Exception$$$$$$$$')
        for log in self.logs:
            print(log)
        raise Exception('logger got Exception')

    def warning(self, *text):
        """some important."""
        head = 'WARNING'
        self.add(head,text)
    def warn(self, *text):
        self.warning(text)
    
    def error(self,*text):
        """clear err"""
        head = 'ERROR'
        self.add(head,text)
    def err(self,*text):
        self.error(text)
    def print(self, *text):
        head = 'print'
        print(text)#whatever
        self.add(head,text)

    #_-for compatibility

    def add(self, head,body):
        strbody = ''
        if isinstance(body,list) or isinstance(body,tuple):
            #body = ' '.join(body)
            for strs in body:
                strbody += strs
        body = strbody

        head = (head+':').ljust(10)
        body = body.ljust(40)#'xx'.rjust(5,'3')
        tstr = get_tstr()

        text = f"{head} {body} --{tstr}"
        self.logs.append(text)
        if self.print_log:print(text)    

    def __repr__(self):
        return '\n'.join(self.logs)

def logtest():
    log = Logger()
    log.log('tt')
    log.error('eEE')
    log.warn('isthiesiwidfj')
    print(log)
#logtest()

def clamp(n, smallest, largest): return max(smallest, min(n, largest))
def clamp(target, a,b):
    X = min(target,b)
    return max(X,a)
def clamp(target, minv, maxv):
    if target<minv:
        return minv
    if target>maxv:
        return maxv
    return target
#min/max 1ms while if < 700us.

def ctest():
    x = clamp(5,1,10)
    y = clamp(5,6,15)
    z = clamp(5,-5,3)
    print(x,y,z)

