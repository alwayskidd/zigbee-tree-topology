from node import node

width=200
height=200
transmission_range=25
number_of_node=500
import random
# random.seed()
STAs=[]
STAs.append(node([width/2,height/2],0))
for i in range(1,number_of_node):
    x=random.uniform(0,width)
    y=random.uniform(0,height)
    STAs.append(node([x,y],i))
#### building the neighhood of each STA #######
for i in STAs:
    for j in STAs:
        if i.if_can_hear(j,transmission_range) and not i==j:
            i.add_neighbour(j)
            j.add_neighbour(i)

fp=open("node_record.pkl","wb")
import pickle
pickle.dump(number_of_node,fp)
pickle.dump(transmission_range,fp)
for each in STAs:
    pickle.dump(each.x,fp)
    pickle.dump(each.y,fp)
fp.close()

#### wirte the neighbourship #####
fp=open("../edges_"+str(number_of_node)+".csv","w")
fp.write("Source,Target,Type,Weight\n")
for each in STAs:
    for each_neighbour in each.neighbours:
        line=str(each.ID)+","+str(each_neighbour.ID)+",Undirected,1\n"
        fp.write(line)
        each_neighbour.delete_neighbour(each)
fp.close()