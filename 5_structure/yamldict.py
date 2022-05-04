import yaml

class YAML:
    """in-out dict converter."""
    @classmethod
    def load(cls, fdir):
        with open(fdir, 'r', encoding='utf-8') as f:
            ddict = yaml.load(f, Loader=yaml.FullLoader)
        return ddict
    @classmethod
    def save(cls, ddict, fdir):        
        with open(fdir, 'w', encoding='utf-8') as f:
            yaml.dump(ddict, f)

#fdir = 'data/actor/tree1.yml'
#datadict = YAML.load(fdir)
#Actor.from_dict(datadict)

#ddict = Actor.to_dict()
#fdir = 'saved_actor.yml'
#YAML.save(ddict, fdir)

if __name__ == '__main__':
    ffff = r'C:\Users\liltm\Desktop\config.yml'

    d = YAML.load(ffff)
    print(d)
    fdir = r'C:\Users\liltm\Desktop\saver.yml'
    YAML.save(d,fdir)
