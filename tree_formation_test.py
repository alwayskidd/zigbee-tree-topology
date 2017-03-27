from topology import Topology
from tree import Tree

## the parameter settings of PHY topology ##
width,height=200,200
transmission_range=25
number_of_routers,number_of_end_devices=500,0
coordinator_locations=[width/2,height/2]

## read the topology from disk ##
phy_topology=Topology()
filename="./Data/area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
    "_endDevices="+str(number_of_end_devices)+".pkl"
phy_topology.read_topology_from_disk(filename)


total_round=500
Cm,Rm,Lm=3,3,10
tree=Tree(Cm,Rm,Lm,phy_topology)
recorder=[] # record if a all nodes can be attached on a tree
for i in range(total_round):
    fp=open("./result/Cm="+str(Cm)+"_Rm="+str(Rm)+"_Lm="+str(Lm)+"/round="+str(i)+".dat","w")
    print("round:"+str(i))
    flag,counter=tree.tree_construction()
    while flag==False: # record this event (some nodes cannot attached) and rebuild a tree:
        recorder.append(counter)
        tree.tree_destruction() # destruct this tree 
        flag,counter=tree.tree_construction() # rebuild it
    hops=[]
    for source in tree.STAs:
        for destination in tree.STAs: # route packet from source to destination
            if source==destination: # skip the path discovery
                continue
            current_node=source
            path=[source]
            while current_node!=destination: # route the packet according to short cut tree routing
                next_node=current_node.find_next_hop(destination,short_cut=True)
                assert next_node in current_node.neighbours, "next hop is out of reach"
                path.append(next_node)
                current_node=next_node
            hops.append(path.__len__())
    fp.write(str(hops))
    fp.close()
    tree.tree_destruction()
fp=open("./result/Cm="+str(Cm)+"_Rm="+str(Rm)+"_Lm="+str(Lm)+"/Constuction_failure.dat","w")
fp.write(str(recorder))
fp.close()