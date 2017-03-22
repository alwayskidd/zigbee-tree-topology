from topology import Topology
from node import Node
from tree import Tree
## the parameter settings of PHY topology ##
width,height=200,200
transmission_range=25
number_of_routers,number_of_end_devices=500,0
coordinator_locations=[width/2,height/2]

# phy_topology=Topology(width,height,transmission_range,number_of_routers,number_of_end_devices,coordinator_locations)
# phy_topology.generate_topology(node_distribution="uniform")
# filename="area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
#     "_endDevices="+str(number_of_end_devices)+".pkl"
# phy_topology.write_topology_on_disk(filename)

# filename=filename="area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
#     "_endDevices="+str(number_of_end_devices)+".csv"
# phy_topology.create_edge_table_for_gephi(filename)
phy_topology=Topology()
filename="area=["+str(width)+","+str(height)+"]_routers="+str(number_of_routers)+\
    "_endDevices="+str(number_of_end_devices)+".pkl"
phy_topology.read_topology_from_disk(filename)
print(phy_topology.width,phy_topology.height,phy_topology.coordinator.x,phy_topology.coordinator.y)