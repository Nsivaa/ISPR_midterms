import numpy as np
import random

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
    
    def add_node(self, node: str, prob_table: list = [0.5, 0.5]):
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
                count += 1
                parents.append(parent)
        return parents
    
    def topo_sort(self):
        # Topological sort
        sorted_nodes = []
        edges_flat_list = [edge for edges in self.edges.values() for edge in edges] # very dirty
        starting_nodes = [node for node in self.nodes.keys() if not (node in edges_flat_list)] # nodes with no incoming edges
        while starting_nodes:
            node = starting_nodes.pop()
            sorted_nodes.append(node)
            try:
                node_children = self.edges[node]
                for child in node_children:
                    self.edges[node].remove(child)
                    try:
                        if not self.edges[child]:
                            pass
                    except KeyError:
                        starting_nodes.append(child)

            except KeyError:
                pass
        if any(self.edges.values()):
            return None
        
        return sorted_nodes
    
    def check_valid(self) -> bool:
        # Check if the network is valid
        res = True
        if self.topo_sort() is None:
            print("Network has cycles")
            res = False

        for node, prob in self.nodes.items():
            if len(self.get_parents(node)) != len(prob):
                print(f"probabilities do not match number of parents of node {node}")
                res = False
            
        return res