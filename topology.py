from node import Node

class Topology:
    """docstring for Topology"""
    def __init__(self, width=0, height=0, transmission_range=0, number_of_routers=0,\
     number_of_end_devices=0, coordinator_locations=0):
        self.width,self.height,self.transmission_range=width,height,transmission_range
        self.number_of_routers,self.number_of_end_devices=number_of_routers,number_of_end_devices
        if coordinator_locations!=0:
            self.coordinator=Node(coordinator_locations,0,"coordinator")
        else:
            self.coordinator=None
        self.STAs=[self.coordinator]

    def generate_topology(self,node_distribution="uniform"):
    # Description: generate a topology with given parameters
    # Input:  node_distribution--indicate how the nodes are distributed on the area
        if node_distribution=="uniform":# generate nodes which is allocated uniformly in the area
            import random
            for i in range(self.number_of_routers):
                x,y=random.uniform(0,self.width),random.uniform(0,self.height)
                self.STAs.append(Node([x,y],self.STAs.__len__(),"router"))
            for i in range(self.number_of_end_devices):
                x,y=random.uniform(0,self.width),random.uniform(0,self.height)
                self.STAs.append(Node([x,y],self.STAs.__len__(),"end device"))
        
        for i in self.STAs: # create the neighbourship according to the transmission range
            for j in self.STAs:
                if i.if_can_hear(j,self.transmission_range) and not i==j:
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
        pickle.dump(self.coordinator.x,fp)
        pickle.dump(self.coordinator.y,fp)
        pickle.dump(self.coordinator.type,fp)
        for each in self.STAs:
            pickle.dump(each.x,fp)
            pickle.dump(each.y,fp)
            pickle.dump(each.type,fp)
        fp.close()

    def read_topology_from_disk(self,filename):
    # Desctiption: read a topology from the disk
    # Input: filename--the file name of the binary file to read from
        import pickle
        fp=open(filename,"rb")
        self.width,self.height,self.transmission_range=pickle.load(fp),pickle.load(fp),pickle.load(fp)
        self.number_of_routers,self.number_of_end_devices=pickle.load(fp),pickle.load(fp)
        self.coordinator=Node([pickle.load(fp),pickle.load(fp)],0,pickle.load(fp))
        self.STAs=[self.coordinator]
        for i in range(self.number_of_routers+self.number_of_end_devices):
            x=pickle.load(fp)
            y=pickle.load(fp)
            node_type=pickle.load(fp)
            self.STAs.append(Node([x,y],self.STAs.__len__(),node_type))
        fp.close()

    def create_edge_table_for_gephi(self,filename):
    # Description: Create the edge table to help illustrate the topology in gephi
    # Input: filename--the csv file
        fp=open(filename,"w")
        fp.write("Source,Target,Type,Weight\n")
        for each in self.STAs:
            if each.type=="end device":
                continue
            for each_neighbour in each.neighbours:
                if each_neighbour.ID> each.ID:
                    line=str(each.ID)+","+str(each_neighbour.ID)+",Undirected,1\n"
                    fp.write(line)
        fp.close()