class node():
    def __init__(self,locations,ID,node_type):
        self.neighbours=[] #record the STAs that can be heard
        self.parents=[] # record the STAs that are the parent of this STA
        self.children_r=[] # record the routers that are the children of current STA
        self.children_d=[] # record the end devices that are the children of current STA
        self.x,self.y=locations[0],locations[1]
        self.ID=ID
        self.level=0
        self.Cm,self.Rm,self.Lm=None,None,None
        self.address=None #initial address is not assigned here
        self.type=node_type # the type could be "coordinator", "router" or "end device"

    def set_tree_parameters(self,Cm,Rm,Lm): # when we start to construct tree topology
        self.Cm,self.Rm,self.Lm=Cm,Rm,Lm

    def set_address(self,address,level=0): #set the address of this node
    # if this node is attached to a tree, the level should be indicated
    # if this node is in mesh topology, then we set the level to 0 by default
        self.address=address
        self.level=level
        #calculate the Cskip
        assert self.Cm!=None and self.Lm!=None and self.Rm!=None, \
            "haven't set the parameter of the tree but doing the construction"
        if self.Rm=1:
            self.Cskip=1+self.Cm*(self.Lm-self.level-1)
        else:
            self.Cskip=(1+self.Cm-self.Rm-self.Cm*self.Rm**(self.Lm-self.level-1))

    def if_can_hear(self,STA,transmission_range): 
    # to see if a node is within its transmission range
    # args: STA--the STA being checked, transmission_range--the transmission range set in the sim
    # return: True--if it is within the transmission range, 
    #         False--if it is not
        import math 
        if math.sqrt((STA.x-self.x)**2+(STA.y-self.y)**2)<=transmission_range:
            return True
        return False

    def add_neighbour(self,STA): # add an neighbour to the neighbour list (when an node is within the transmission range)
        if not STA in self.neighbours:
            self.neighbours.append(STA)

    def delete_neighbour(self,STA): # delet an neighbour in the neighbout list
        assert STA in self.neighbours,\
            "delete an neighbour that is not in the neighbourlist"
        self.neighbours.remove(STA)

    def add_children(self,STA): # add a child to the children list (for end devices or for routers)
    # return the address of the child
        assert STA in self.neighbours, "add a child that is not one of the neighbours"
        if STA.type="router" and self.children_r.__len__() <= self.Rm:
            self.children_r.append(STA)
            return self.address+Cskip*(self.children_r.__len__()-1)+1

        if STA.type="end device" and  self.children_r.__len__()+self.children_d.__len__()<=self.Cm:
            self.children_d.append(STA)
            return self.address+Cskip*Rm+self.children_d.__len__()
        return False

    def find_ancestors(self,destination):
    # find the ancestor of current node and the destination
    # input: destination--the destination node
    # output: hops-- the expected hops to reach the destination according to tree routing
    #         ancestor-- the ancestor node
    ancestor=self
    while True: #find the ancestor that can reach the destination through a downlink path
        lower_bound=ancestor.address
        upper_bound=ancestor.address+ancestor.Cskip*ancestor.Rm+ancestor.Cm-ancestor.Rm # calculate the address coverage of this subtree
        if destination.address>=lower_bound and destination.address<=upper_bound:
            break
        else:
            ancestor=ancestor.parent
    # calculate the hop count to reach the ancestor and going down to the destination
    hops=self.level-ancestor.level+destination.level-ancestor.level
    return hops,ancestor

    def add_parent(self,STA): # add a parent to this node
        assert STA in self.neighbours, "add a parent which is not one of the neighbours"
        assert self.parents==[], "this node has alreay get a parent"
        self.parents.append(STA)

    def has_parent(self): # check whether this node has been assigned a parent
        # return: True--if this node has a parent
        #         False--if this node has no parent
        if self.parents==[]:
            return False
        else:
            return True