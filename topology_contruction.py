from node import node

width=200
height=200
transmission_range=25
number_of_routers=500
number_of_end_devices=0

#generate nodes on the topology
import random
STAs=[]
STAs.append(node([width/2,height/2],0,"coordinator"))
for i in range(1,number_of_routers):# create routers
    x=random.uniform(0,width)
    y=random.uniform(0,height)
    STAs.append(node([x,y],i,"router"))

for i in range(1,number_of_end_devices): # create end devices
    x=random.uniform(0,width)
    y=random.uniform(0,height)
    STAs.append(node([x,y],i,"end device"))

#### building the neighship of each STA #######
for i in STAs:
    for j in STAs:
        if i.if_can_hear(j,transmission_range) and not i==j:
            i.add_neighbour(j)
            j.add_neighbour(i)

#### record the information of nodes onto the pkl file
fp=open("node_record.pkl","wb")
import pickle
pickle.dump(number_of_routers+number_of_end_devices,fp)
pickle.dump(transmission_range,fp)
for each in STAs:
    pickle.dump(each.x,fp)
    pickle.dump(each.y,fp)
    pickle.dump(each.type,fp)
fp.close()

#### wirte the neighbourship #####
fp=open("../edges_"+str(number_of_routers+number_of_end_devices)+".csv","w")
fp.write("Source,Target,Type,Weight\n")
for each in STAs:
    for each_neighbour in each.neighbours:
        line=str(each.ID)+","+str(each_neighbour.ID)+",Undirected,1\n"
        fp.write(line)
        each_neighbour.delete_neighbour(each)
fp.close()