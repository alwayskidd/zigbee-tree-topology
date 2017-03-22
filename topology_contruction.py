from node import Node

class Topology(object):
    """docstring for Topology"""
    def __init__(self, width=0, height=0, transmission_range=0, number_of_routers=0,\
     number_of_end_devices=0, coordinator_locations=0):
        self.width,self.height,self.transmission_range=width,height,transmission_range
        self.number_of_routers,self.number_of_end_devices=number_of_routers,number_of_end_devices
        self.coordinator=Node(coordinator_locations,0,"coordinator")
        self.STAs=[self.coordinator]

    def generate_topology(self,node_distribution="uniform"):
    # Description: generate a topology with given parameters
    # Input:  node_distribution--indicate how the nodes are distributed on the area
        if node_distribution=="uniform":# generate nodes which is allocated uniformly in the area
            import random
            for i in range(number_of_routers):
                x,y=random.uniform(0,width),random.uniform(0,height)
                self.STAs.append(Node([x,y],self.STAs.__len__(),"router"))
            for i in range(number_of_end_devices):
                x,y=random.uniform(0,width),random.uniform(0,height)
                self.STAs.append(Node([x,y],self.STAs.__len__(),"end device"))
        
        for i in STAs: # create the neighbourship according to the transmission range
            for j in STAs:
                if i.if_can_hear(j,transmission_range) and not i==j:
                    i.add_neighbour(j)
                    j.add_neighbour(i)

    def write_topology_on_disk(self,filename):
    # Description: record the topology on the disk for later use (multiple simulations on the same topology)
    # Input: filename--the file name of the target binary file
        fp=open(filename,"wb")
        import pickle
        pickle.dump(self.width,fp)
        pickle.dump(self.height,fp)
        pickle.dump(self.transmission_range,fp)
        pickle.dump(self.number_of_routers,fp)
        pickle.dump(self.number_of_end_devices,fp)
        pickle.dump(self.coordinator,fp)
        for each in self.STAs:
            pickle.dump(each.x,fp)
            pickle.dump(each.y,fp)
            pickle.dump(each.type,fp)
        fp.close()

    def read_topology_from_disk(self,filename):
    # Desctiption: read a topology from the disk
    # Input: filename--the file name of the binary file to read from
        fp=open(filename,"rb")
        self.width,self.height,self.transmission_range=pickle.load(fp),pickle.load(fp),pickle.load(fp)
        self.number_of_routers,self.number_of_end_devices=pickle.load(fp),pickle.load(fp)
        self.coordinator=pickle.load(fp)
        self.STAs=[self.coordinator]
        for i in range(self.number_of_routers+self.number_of_end_devices):
            x=pickle.dump(fp)
            y=pickle.dump(fp)
            node_type=pickle.dump(fp)
            self.STAs.append(Node([x,y],self.STAs.__len__(),node_type))
        fp.close()