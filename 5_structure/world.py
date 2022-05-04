class World:
    """3d world, holding actors."""
    def __init__(self):
        self.actors = []
        self.cameras = []
        #a[0],a[3]=a[3],a[0]    

    #def __getattr__(self,name):
        #cam = self.get_camera(name)
        #if cam != None:return cam        
        #return super().__getattr__()    
    # def get_camera(self,0):
    #     """get cam0-camN"""
    #     if 'cam' in name:
    #         N = name[3:]#cam,N = name.split('cam')            
    #         if N.isdecimal:
    #             if N<len(self.cameras):
    #                 return self.cameras[int(N)]
    #             else:
    #                 return None
    def get_camera(self,N):
        if N<len(self.cameras):
            return self.cameras[N]
        return None
    
    def bind(self, window):
        """get dt from window"""
        window.update = self.update

    def input(self, inputs):
        """process input"""
        for actor in self.actors:
            1
    def update(self, dt):
        """physics simulation
        now, bypass pause_menu. we may proceed better way..
        with including pause_menu as plane actor.
        if you stop by for: freeze, too many actor..
        we also need block input all. but pause_menu. how?"""
        for actor in self.actors:
            1
w=World()

