import numpy as np
from bayesian_node import BayesianNode
import random

class BayesianNetwork:
    def __init__(self, values : list, nodes: dict = {}, edges: dict = {}):
        # nodes is a list of Bayesian Nodes
        # edges is a dict of {node: list of nodes it points to}
        self.nodes = nodes
        self.edges = edges 
        self.values = values  #determines the possible values assumed by the variables

    def __str__(self) -> str:
        return f"Nodes: {self.nodes.keys()}, Edges: {self.edges}"
    
    def add_node(self, node: BayesianNode):
        self.nodes.update({node.name : node})
    
    def add_edge(self, parent, children):
        if parent in self.nodes.keys():
            
            self.edges.update({parent:children})
        else:
            raise ValueError("Node not in network")

    def get_parents(self, node:str ) ->  list:
        # Get parents of a node
        parents = []
        for edge in self.edges.items():
            if node in edge[1]:
                count += 1
                parents.append(edge[0])
        return parents
    
    def topo_sort(self):
        # Topological sort
        sorted_nodes = []
        starting_nodes = [node for node in self.nodes.keys() if not (node in list(self.edges.values()))] #nodes with no incoming edges
        while starting_nodes:
            node = starting_nodes.pop()
            sorted_nodes.append(node)
            node_children = self.edges[node]

            for child in node_children:
                self.edges[node].remove(child)
                if not self.edges[child]:
                    starting_nodes.append(child)
        if self.edges:
            return None
        
        return sorted_nodes
    
    def check_valid(self) -> bool:
        # Check if the network is valid
        res = True
        if self.topo_sort() is None:
            print("Network has cycles")
            res = False
        for node in self.nodes:
            if len(self.get_parents(node)) != len(node.prob_table):
                print(f"probabilities do not match number of parents of node {node.name}")
                res = False
            
        return res