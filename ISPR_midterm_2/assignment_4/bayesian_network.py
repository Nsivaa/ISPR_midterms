import numpy as np
import random
import copy

class BayesianNetwork:
    def __init__(self, values : list, nodes: dict = {}, edges: dict = {}):
        # nodes is a dict of {node : probability table}
        # edges is a dict of {node : list of nodes it points to}
        # determines the possible values assumed by the variables in the network

        self.nodes = nodes
        self.edges = edges 
        self.values = values  

    def __str__(self) -> str:
        return f"Nodes: {self.nodes.keys()}, Edges: {self.edges}"
    
    def add_node(self, node: str, prob_table: dict = {"Prior" : [0.5, 0.5]}):
        self.nodes.update({node : prob_table})
    
    def add_edge(self, parent: str, children: list):
        if parent in self.nodes.keys():
            
            self.edges.update({parent : children})
        else:
            raise ValueError("Node not in network")

    def get_parents(self, node : str ) -> list:
        # Get parents of a node
        parents = []
        for parent, children in list(self.edges.items()):
            if node in children:
                parents.append(parent)
        return parents
    
    def get_probabilities(self, node: str) -> list:
        # Get probabilities of a node
        res = self.nodes[node]
        if "Prior" in res.keys():
            return res["Prior"]
        else:
            print(f"Node {node} has parents")
    
    def topo_sort(self):
        # Topological sort
        sorted_nodes = []
        edges_copy = copy.deepcopy(self.edges) #so that we don't modify the original edges
        edges_flat_list = [edge for edges in self.edges.values() for edge in edges] # dirty way to deal with nested lists
        starting_nodes = [node for node in self.nodes.keys() if not (node in edges_flat_list)] # nodes with no incoming edges
        while starting_nodes:
            node = starting_nodes.pop()
            sorted_nodes.append(node)
            try:
                node_children = edges_copy[node]
                for child in node_children:
                    edges_copy[node].remove(child)

                    if not (child in edges_copy.values()):
                        starting_nodes.append(child)

            except KeyError:
                pass
        if any(edges_copy.values()):
            return None
        
        return sorted_nodes
    
    def check_valid(self) -> bool:
        # Check if the network is valid

        #if the net is not sortable, it has cycles
        res = True
        if self.topo_sort() is None:
            print("Network has cycles")
            res = False

        # check probability table of the nodes
            
        # the sum of the probabilities of each node should be 1
        
        for node, prob in self.nodes.items():
            sum = 0
            
            if type(prob) == dict:
                for _, value in prob.items():
                    sum = np.sum(value)
                    if sum != 1:
                        print(f"Node {node} probability at {value} don't sum to 1")
                        res = False
            elif type(prob) == list:
                sum = np.sum(prob)

            if sum != 1:
                print(f"Node {node} probability don't sum to 1")
                res = False

            # if node has no parents, the number of probabilities should be equal to the number of possible values
            if len(self.get_parents(node)) == 0:
                if len(list(prob.values())[0]) != len(self.values):
                    print(f"Node {node} probability table doesn't match values length")
                    res = False
            else:
            # if node has parents, the number of probabilities should be equal to the number of possible
            # combinations of the possible values of the parents
                if len(prob) != np.prod([len(self.values) for parent in self.get_parents(node)]):
                    print(f"Node {node} probability table doesn't match parents values")
                    res = False
            
        return res

    def add_prob_table(self, node: str, prob_table: dict):
        self.nodes.update({node : prob_table})

    def sample(self, probabilities : list, values : list = [0,1]) -> int:
        # Sample from a distribution, binary by default
        if (len(values)!=len(probabilities)): 
            raise ValueError('Length of values and probabilities are different')
        return np.random.choice(values, p = probabilities)