class Node:
    def __init__(self,locations,ID,node_type):
        self.neighbours=[] #record the STAs that can be heard
        self.parent=None # record the STAs that are the parent of this STA
        self.children_r=[] # record the routers that are the children of current STA
        self.children_d=[] # record the end devices that are the children of current STA
        self.x,self.y=locations[0],locations[1]
        self.ID=ID
        self.level=0
        self.Cm,self.Rm,self.Lm,self.level,self.Cskip=None,None,None,None,None
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
        if self.Rm==1:
            self.Cskip=1+self.Cm*(self.Lm-self.level-1)
        else:
            self.Cskip=(1+self.Cm-self.Rm-self.Cm*self.Rm**(self.Lm-self.level-1))/(1-self.Rm)
        assert self.Cskip>=0, "Cskip is less than 0="+str(self.Cskip)


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
        if STA.type=="router" and self.children_r.__len__() <= self.Rm:
            self.children_r.append(STA)
            return self.address+self.Cskip*(self.children_r.__len__()-1)+1

        if STA.type=="end device" and  self.children_r.__len__()+self.children_d.__len__()<=self.Cm:
            self.children_d.append(STA)
            return self.address+self.Cskip*self.Rm+self.children_d.__len__()
        return False


    def hops_to_destination(self,destination):
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


    def find_next_hop(self,destination,short_cut):
    # Description: find the next hop to route current packet
    # Input: destination--the destination node of this packet
    #        short_cut -- if short_cut routing is enabled (True) or not (False)
    # Outpue: nexthop node
        assert destination!=self, "packet has arrived, no need to find next hop"
        for each_neighbour in self.neighbours: # check if the destiantion is a one hop neighbour
            if each_neighbour==destination: # directly send this packet to the neighbour
                return each_neighbour

        if short_cut==False: # route along the tree
            lower_bound=self.address
            upper_bound=self.address+self.Cskip*self.Rm+self.Cm-self.Rm
            if destination.address>upper_bound or destination.address<lower_bound:# go upstream
                return self.parent
            # go downstream
            for each_child in self.children_d: # check if it is one of the attached end devices
                if each_child==destination:
                    return each_child
            for each_child in self.children_r: # see the destination belongs to which subtree
                lower_bound=each_child.address
                upper_bound=each_child.address+each_child.Cskip*each_child.Rm+each_child.Cm-each_child.Rm
                if destination.address<=upper_bound and destination.address>=lower_bound: # go to this subtree
                    return each_child

        if short_cut==True: # short cut tree routing
            min_hops=self.Lm*5
            candidate=None
            for each_neighbour in self.neighbours:
                hops,ancestor=each_neighbour.hops_to_destination(destination)
                if min_hops>hops: # make this node as the candidate until some neighbours have less cost
                    min_hops=hops
                    candidate=each_neighbour
            return candidate # this operation is exact how the paper is implemented
                # if min_hops==hops: # add this neighbout as one of the candidate
                #     candidate.append(each_neighbour)

    def add_parent(self,STA): # add a parent to this node
        assert STA in self.neighbours, "add a parent which is not one of the neighbours"
        assert self.parent==None, "this node has alreay get a parent"
        self.parent=STA

    def  clear_children_parent(self):
    # Description: Clear all the children and the parent
        self.children_r=[]
        self.children_d=[]
        self.parent=None

    def has_parent(self): # check whether this node has been assigned a parent
        # return: True--if this node has a parent
        #         False--if this node has no parent
        if self.parent==None:
            return False
        else:
            return True
