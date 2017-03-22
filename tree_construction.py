from node import node
# initialize the phy topology
Cm,Rm,Lm=5,5,9
# read the node location from pkl file
fp=open("node_record.pkl",'rb')
import pickle
number_of_nodes=pickle.load(fp)
transmission_range=pickle.load(fp)
STAs=[]
for i in range(number_of_nodes):
    x=pickle.load(fp)
    y=pickle.load(fp)
    node_type=pickle.load(fp)
    STAs.append(node([x,y],i,node_type))
    STAs[-1].set_tree_parameters(Cm,Rm,Lm)

#### building the neighship of STAs #######
for i in STAs:
    for j in STAs:
        if i.if_can_hear(j,transmission_range) and not i==j:
            i.add_neighbour(j)
            j.add_neighbour(i)

#### construct a tree ##########
bfs_list=[]
bfs_list.append(STAs[0])
STAs[0].parents=None
counter=0
print(bfs_list[0].parents)
import random
while not bfs_list==[]:
    temp=bfs_list.pop(0)
    children_candidates_r=[] #candidate children with type of router
    children_candidates_d=[] #candidate children with type of devices
    # temp=bfs_list.pop(0)
    # children_candidates=[]
    # for each in temp.neighbours:
    #     if each.parents==[]:
    #         children_candidates.append(each)
    # random.shuffle(children_candidates)
    # while not children_candidates==[] and temp.children.__len__()<Cm: # insert a candidate into childrens list
    #     child=children_candidates.pop()
    #     temp.add_children(child,Cm)
    #     child.add_parent(temp)
    #     child.level=temp.level+1
    #     bfs_list.append(child)


fp=open("../tree_Cm="+str(Cm)+"_Lm="+str(Lm)+".csv","w")
fp.write("Source,Target,Type,Weight\n")
for each in STAs:
    # print(each.children)
    for each_child in each.children:
        line=str(each.ID)+","+str(each_child.ID)+",Directed,1.2\n"
        fp.write(line)
fp.close()

colors=["#000000","#ff0000","#00ff00","#0000ff","#ffff00","#ff00ff","#00ffff","#ff6666","#66ff66","#6666ff"]
fp=open("../node_"+str(number_of_nodes)+".csv","w")
fp.write("ID,x,y,ColorOfNode\n")
for each in STAs:
    line=str(each.ID)+","+str(each.x/10)+","+str(each.y/10)+","+colors[each.level]+"\n"
    fp.write(line)
fp.close()
