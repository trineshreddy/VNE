from audioop import reverse
import alib.datamodel
import alib.solutions
from collections import namedtuple, OrderedDict


#generate the substarte_graph
def create_substrate_graph():
    substrate_graph = alib.datamodel.Substrate("S")
    print("Enter the number of substrate nodes")
    number_substrate_nodes = int(input())
    count = 0
    while(count < number_substrate_nodes):
        total_cpu_capacity = float(input("Enter the total CPU capacity "))
        available_capacity = 0.0
        substrate_graph.add_node(str(count), {"a"}, capacity={"a": total_cpu_capacity}, cost={"a": available_capacity})
        count += 1
    print("Enter the number of substrate edges")
    number_substrate_edges = int(input())
    count = 0
    while(count < number_substrate_edges):
        u = input("Enter the first node ")
        v = input("Enter the second node ")
        edge_bandwidth = float(input("Enter the edge bandwidth "))
        substrate_graph.add_edge(str(u), str(v), edge_bandwidth)
        count += 1
    return(substrate_graph)


#generate the virtual_graph
def create_virtual_graph():
    virtual_graph = alib.datamodel.LinearRequest("V")
    print("Enter the number of virtual nodes")
    number_virtual_nodes = int(input())
    count = 0
    while(count < number_virtual_nodes):
        cpu_capacity = float(input("Enter the CPU capacity "))
        mapped_substrate_node  = []
        requirement = namedtuple("requirement", ["cpu_request", "mapped_substrate_node"])
        demand = requirement(cpu_capacity, mapped_substrate_node)
        virtual_graph.add_node(str(count), demand, "t1")
        count += 1
    print("Enter the number of virtual edges")
    number_virtual_edges = int(input())
    count = 0
    while(count < number_virtual_edges):
        u = input("Enter the first node ")
        v = input("Enter the second node ")
        edge_bandwidth = float(input("Enter the edge bandwidth "))
        virtual_graph.add_edge(str(u), str(v), edge_bandwidth)
        count += 1
    return(virtual_graph)
    

#generate the  virtual_network_request
def virtual_network_request():
    virtual_graph = create_generate_virtual_graph()
    Ta = float(input("enter the arrival time"   ))
    t = float(input("Enter duration of VN in substrate network"))
    e = int(input("enter the binary variable"))
    d = int(input("enter the delat value of virtual network request"))
    k = int(input("enter number of virtual network request"))
    vnr = {"virtual_graph":virtual_graph,"Ta":Ta,"t":t,"e":e,"d":d,"k":k}
    return(vnr)

#handles the VNR in r_new queue
def handle_r_new(substrate_graph,vnr):
    VG =vnr[virtual_graph]
    mapping = alib.solutions.Mapping("VNE_DR_map", VG, substrate_graph, True)

    #Mapping Virtual Nodes
    for vnode in VG.get_nodes():
        for snode in substrate_graph.get_nodes():
            total_capacity = substrate_graph.get_node_capacity(snode)
            available_capacity=substrate_graph.get_node_cost(snode)
            demand = VG.get_node_demand(vnode)
            if(available_capacity>=demand.cpu_capacity):
                available_capacity-=demand.cpu_capacity
                demand.mapped_substrate_node.append(snode)
                break

    #Mapping Virtual Edges

    for vedge in VG.get_edges():

        u,v = vedge
        Virtual_edge_bandwidth = VG.get_edge_bandwidth(vedge)

        sub_u = VG.get_node_demand(u).mapped_substrate_node[0]
        sub_v = VG.get_node_demand(v).mapped_substrate_node[0]
        mapped_path= get_best_path(sub_u,sub_v,substrate_graph)
        for edge in mapped_path:
            curr = substrate_graph.get_edge_demand(edge)
            min_substrate_bandwidth = 10000000
            min_substrate_bandwidth = min(curr,min_substrate_bandwidth)
        if(Virtual_edge_bandwidth<=min_substrate_bandwidth ):
              mapping.map_edge(vedge,mapped_path)
              for edge in mapped_path:
                  curr_bandwidth = substrate_graph.get_edge_demand(edge)
                  curr_bandwidth-=Virtual_edge_bandwidth

        else:
            print("Virtual Edge Bandwidth is more than available os we cant map Virtual edge")


#handles the VNR in r_increase queue
def handle_r_decrease(substrate_graph,vnr):
    VG =vnr[virtual_graph]
    mapping = alib.solutions.Mapping("VNE_DR_map", VG, substrate_graph,true)

    #Remove Mapped Virtual Nodes
    for vnode in VG.get_nodes():
        demand = VG.get_node_demand(vnode)
        substrate_node = demand.mapped_substrate_node[0]
        #removing allocated capacity in substrate_node
        available_capacity=substrate_graph.get_node_cost(substrate_node)
        available_capacity+=demand.cpu_capacity
        #removing mapping
        demand.mapped_substrate_node.pop(0)

    #Remove Mapped Virtual edges
    for vegde in VG.get_edges:
        mapping.remove_mapped_edge(vedge,mapped_path,substrate_graph)



def virtalnodemigration1(substrate_graph,vnr):
    pass

def virtalnodemigration2(substrate_graph,vnr):
    pass


def handle_add_node(substrate_graph,vnr):
    pass


def handle_increase_resource(substrate_graph,vnr):
    pass

#handles the VNR in r_increase queue
def handle_r_increase(substrate_graph,vnr,d):
    if(d==3):
        handle_add_node(substrate_graph,vnr)
    elif(d==4):
        handle_increase_resource(substrate_graph,vnr)

    
def VNE_DR_Algorithm():
    substrate_graph = create_substrate_graph()
    r_new =[]
    r_increase = []
    r_decrease = []
    num_vnr = int(input("Enter the number of virtual network requeests"))
    count = 0
    #d=1 means delete node request
    #d=2 means decrease resource node
    #d=3 means add node request
    #d=4 means incease resource node
    while( count < num_vnr):
        vnr = virtual_network_request()
        if vnr[e] == 1 :
            r_new.append(vnr)
        elif vnr[e] == 0  and (vnr[d] == 3 or vnr[d]==4):
            r_increase.append(vnr)
        elif vnr[e] ==0 and (vnr[d] == 2 or vnr[d]==1) :
            r_decrease.append(vnr)
        count+=1
    d=vnr[d]
    for _ in r_decrease:
        handle_r_decrease(substrate_graph,_)
        r_decrease.pop()
    for _ in r_increase:
        handle_r_increase(substrate_graph,_,d)
        r_increase.pop()
    if(len(r_increase)==0):
        for _ in r_new:
            handle_r_new(substrate_graph,_)
            r_new.pop()
     
result = VNE_DR_Algorithm()
print(result)

    


        
    
    
       

        

