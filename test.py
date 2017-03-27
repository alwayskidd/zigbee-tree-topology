from topology import Topology
from node import Node
from tree import Tree

def path_print(path,notes):
    #print a path from source to the destination
    for each in path:
        notes+=str(each.ID)
        if each!=path[-1]:
            notes+="->"
    return notes

## the parameter settings of PHY topology ##
width,height=200,200
transmission_range=25
number_of_routers,number_of_end_devices=1000,0
coordinator_locations=[width/2,height/2]

phy_topology=Topology(width,height,transmission_range,number_of_routers,number_of_end_devices,coordinator_locations)
phy_topology.generate_topology(node_distribution="uniform")
filename="./Data/area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
    "_endDevices="+str(number_of_end_devices)+".pkl"
phy_topology.write_topology_on_disk(filename)

# filename=filename="area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
#     "_endDevices="+str(number_of_end_devices)+".csv"
# phy_topology.create_edge_table_for_gephi(filename)

# phy_topology=Topology()
# filename="./Data/area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
#     "_endDevices="+str(number_of_end_devices)+".pkl"
# phy_topology.read_topology_from_disk(filename)
# print(phy_topology.width,phy_topology.height,phy_topology.coordinator.x,phy_topology.coordinator.y)

# # tree create test
# Cm,Rm,Lm=5,5,9
# tree=Tree(Cm,Rm,Lm,phy_topology)
# tree.tree_construction()

# filename="./Data/TreeEdges_area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
#      "_endDevices="+str(number_of_end_devices)+"_[Cm,Rm,Lm]=["+str(Cm)+","+str(Rm)+","+str(Lm)+"].csv"
# tree.create_edge_table_for_gephi(filename)

# filename="./Data/Nodes_area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
#      "_endDevices="+str(number_of_end_devices)+"_[Cm,Rm,Lm]=["+str(Cm)+","+str(Rm)+","+str(Lm)+"].csv"
# tree.create_node_table_for_gephi(filename)

# ### test the tree routing algorithm ####
# import random
# # node_1=tree.STAs[random.randint(0,tree.STAs.__len__()-1)]
# # node_2=tree.STAs[random.randint(0,tree.STAs.__len__()-1)]
# # print("source node address:"+str(node_1.address)+"\nsource node level:"+str(node_1.level))
# # print("destination address:"+str(node_2.address)+"\ndestination level:"+str(node_2.level))
# # hops,ancestor=node_1.hops_to_destination(node_2)
# # # print(node_1.hops_to_destination(node_2))
# # print("needed hops:"+str(hops))
# # print("ancestor address:"+str(ancestor.address)+"\nancestor level:"+str(ancestor.level))
# # for each in ancestor.children_r:
# #     lower_bound=each.address
# #     upper_boud=each.address+each.Cskip*each.Rm+each.Cm-each.Rm
# #     if node_1.address>=lower_bound and node_1.address<=upper_boud:
# #         print("node 1 in range "+str([lower_bound,upper_boud]))
# #     if node_2.address>=lower_bound and node_2.address<=upper_boud:
# #         print("node 2 in range "+str([lower_bound,upper_boud]))

# ### test if a packet can use short cut to reach the destination ###
# while True:
#     source=tree.STAs[random.randint(0,tree.STAs.__len__()-1)]
#     destination=tree.STAs[random.randint(0,tree.STAs.__len__()-1)]
#     short_cut=False
#     path_tree=[source]
#     current_node=source
#     while current_node!=destination: #route the packet through tree routing
#         next_node=current_node.find_next_hop(destination,short_cut)
#         assert next_node in current_node.neighbours, "next hop is out of reach"
#         path_tree.append(next_node)
#         current_node=next_node
#     print("hops needed in tree routing:"+str(path_tree.__len__()-1))

#     current_node=source
#     path_shortcut=[source]
#     short_cut=True
#     while current_node!=destination: #route the packet through short cut tree routing
#         next_node=current_node.find_next_hop(destination,short_cut)
#         assert next_node in current_node.neighbours, "next hop is out of reach"
#         path_shortcut.append(next_node)
#         current_node=next_node
#     print("hops needed in shortcut tree routing: "+str(path_shortcut.__len__()-1))

#     if path_shortcut.__len__()<path_tree.__len__(): #print the routing path through each way
#         notes="the routing path without shortcut:\n"
#         print(path_print(path_tree,notes))
#         notes="the routing path with shorcut:\n"
#         print(path_print(path_shortcut,notes))
#         break