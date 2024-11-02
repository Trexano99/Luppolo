from abc import ABC, abstractmethod
from antlr4.tree.Tree import Tree

from src.ast.GraphLuppNode import GraphLuppNode

class BaseLuppNode(Tree, ABC):
    '''
    The abstract class BaseLuppNode is the base class for all the nodes in the AST.
    '''

    @abstractmethod
    def __init__(self, name, children = None):
        '''
        This method initializes the BaseLuppNode object.
        The method takes the following parameters:
        - name: the name of the node.
        - children: the children of the node.
        '''
        self.name = name
        self.children = children if children is not None else []

    def getGraphRapresentation(self, graph, attributes = None):
        '''
        This method is used to get the graph representation of the node.
        The method takes the following parameters:
        - graph: the graph into which the node will be represented.
        - attributes: the attributes of the node.
        Return the id of the node
        '''
         
        graphNode = GraphLuppNode(self)
        if attributes is not None:
            for attribute in attributes:
                graphNode.updateGraphAttribute(attribute)
        return graphNode.developGraph(graph)
    
    def getPayload(self):
        ''' Return the node payload'''
        return self.name
    
    def getChild(self, i):
        ''' Return the ith child of the node'''
        return self.children[i]
    
    def getChildCount(self):
        ''' Return the number of children of the node'''
        return len(self.children)
    
    def addChild(self, child):
        ''' Add a child to the node. Set the parent of the child to this current node'''
        child.parent = self
        self.children.append(child)
