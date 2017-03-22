from node import Node
from topology import Topology

class Tree:
    """docstring for Tree"""
    def __init__(self,Cm,Rm,Lm,phy_Topology):
        self.Cm,self.Rm,self.Lm=Cm,Rm,Lm
        self.phy_Topology=phy_Topology
        self.STAs=self.phy_Topology.STAs
        self.coordinator=self.phy_Topology.coordinator
        self.coordinator.set_address(address=0,level=0)
        for each in self.STAs:
            each.set_tree_parameters(self.Cm,self.Rm,self.Lm)

    def tree_construction(self):
    # Description: Construct a tree according to the tree parameters
        bfs_list=[] # construction follows a breadth first searching
        bfs_list.append(self.coordinator)
        import random
        while not bfs_list==[]:
            parent=bfs_list.pop(0)
            if parent.level>=self.Lm: # skip the current node
                continue
            children_candidates_r=[] #candidate children with type of router
            children_candidates_d=[] #candidate children with type of devices

            for each_neighbour in parent.neighbours: # choose the candidate of router child and end device child
                if not each_neighbour.has_parent():
                    if each_neighbour.type=="router": 
                        children_candidates_r.append(each_neighbour)
                    if each_neighbour.type=="end device":
                        children_candidates_d.append(each_neighbour)
            random.shuffle(children_candidates_r)
            random.shuffle(children_candidates_d)

            while not children_candidates_r==[] and parent.children_r.__len__()<Rm: # add a router candidate to this subtree
                child=children_candidates_r.pop()
                address=parent.add_children(child)
                assert address!=False, "cannot add a child"
                child.set_address(address,parent.level+1)
                child.add_parent(parent)
                bfs_list.append(child)

            while not children_candidates_d==[] and parent.children_d.__len__()<Cm-Rm: # add a end device candidate to this subtree
                child=children_candidates_d.pop()
                address=parent.add_children(child)
                assert address!=False, "cannot add a child"
                child.set_address(address,parent.level+1)
                child.add_parent(parent)

    def create_node_table_for_gephi(self,filename):
    # Description: Create the node table to help illustrate the topology in gephi
    # Input: filename--the cvs file
        colors=["#000000","#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff","#ff6666","#66ff66","#6666ff"]
        fp=open(filename,"w")
        fp.write("ID,x,y,ColorOfNode\n")
        for each in self.STAs:
            line=str(each.ID)+","+str(each.x/10)+","+str(each.y/10)+","+colors[each.level]+"\n"
            fp.write(line)
        fp.close()

    def create_edge_table_for_gephi(self,filename):
    # Description: Create the edge table (for the edges on the tree) to help illustrate the topology in gephi
    # Input: filename--the cvs file
        fp=open(filename,"w")
        fp.write("Source,Target,Type,Weight\n")
        for each in self.STAs:
            # print(each.children)
            for each_child in each.children_r:
                line=str(each.ID)+","+str(each_child.ID)+",Directed,1.2\n"
                fp.write(line)
            for each_child in each.children_d:
                line=str(each.ID)+","+str(each_child.ID)+",Directed,1.2\n"
                fp.write(line)
        fp.close()




# bfs_list=[]
# bfs_list.append(STAs[0])
# STAs[0].parents=None
# counter=0
# STAs[0].set_address(0,0)
# import random
# while not bfs_list==[]:
#     parent=bfs_list.pop(0)
#     if parent.level==Lm: # skip this node
#         continue
#     children_candidates_r=[] #candidate children with type of router
#     children_candidates_d=[] #candidate children with type of devices
#     for each_neighbour in parent.neighbours: # choose the candidate of router child and end device child
#         if not each_neighbour.has_parent():
#             if each_neighbour.type=="router": 
#                 children_candidates_r.append(each_neighbour)
#             if each_neighbour.type=="end device":
#                 children_candidates_d.append(each_neighbour)
#     random.shuffle(children_candidates_r)
#     random.shuffle(children_candidates_d)

#     while not children_candidates_r==[] and parent.children_r.__len__()<Rm: # add a router candidate to this subtree
#         child=children_candidates_r.pop()
#         address=parent.add_children(child)
#         assert address!=False, "cannot add a child"
#         child.set_address(address,parent.level+1)
#         child.add_parent(parent)
#         bfs_list.append(child)

#     while not children_candidates_d==[] and parent.children_d.__len__()<Cm-Rm: # add a end device candidate to this subtree
#         child=children_candidates_d.pop()
#         address=parent.add_children(child)
#         assert address!=False, "cannot add a child"
#         child.set_address(address,parent.level+1)
#         child.add_parent(parent)

# # initialize the phy topology
# Cm,Rm,Lm=5,5,9
# # read the node location from pkl file
# fp=open("node_record.pkl",'rb')
# import pickle
# number_of_nodes=pickle.load(fp)
# transmission_range=pickle.load(fp)
# STAs=[]
# for i in range(number_of_nodes):
#     x=pickle.load(fp)
#     y=pickle.load(fp)
#     node_type=pickle.load(fp)
#     STAs.append(node([x,y],i,node_type))
#     STAs[-1].set_tree_parameters(Cm,Rm,Lm)

# #### building the neighship of STAs #######
# for i in STAs:
#     for j in STAs:
#         if i.if_can_hear(j,transmission_range) and not i==j:
#             i.add_neighbour(j)
#             j.add_neighbour(i)


# fp=open("../tree_Cm="+str(Cm)+"_Lm="+str(Lm)+".csv","w")
# fp.write("Source,Target,Type,Weight\n")
# for each in STAs:
#     # print(each.children)
#     for each_child in each.children_r:
#         line=str(each.ID)+","+str(each_child.ID)+",Directed,1.2\n"
#         fp.write(line)
#     for each_child in each.children_d:
#         line=str(each.ID)+","+str(each_child.ID)+",Directed,1.2\n"
#         fp.write(line)
# fp.close()

# colors=["#000000","#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff","#ff6666","#66ff66","#6666ff"]
# fp=open("../node_"+str(number_of_nodes)+".csv","w")
# fp.write("ID,x,y,ColorOfNode\n")
# for each in STAs:
#     line=str(each.ID)+","+str(each.x/10)+","+str(each.y/10)+","+colors[each.level]+"\n"
#     fp.write(line)
# fp.close()
