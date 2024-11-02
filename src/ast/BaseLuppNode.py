from abc import ABC, abstractmethod
from antlr4.tree.Tree import Tree

from src.ast.GraphLuppNode import GraphLuppNode

class BaseLuppNode(Tree, ABC):
    '''
    The abstract class BaseLuppNode is the base class for all the nodes in the AST.
    '''

    @abstractmethod
    def __init__(self, name, children : list = None):
        '''
        This method initializes the BaseLuppNode object.
        The method takes the following parameters:
        - name: the name of the node.
        - children: the children of the node. Should be a list of BaseLuppNode, if not it will be converted to a list.
        '''
        self.children = [children] if type(children) is not list else children
        for child in self.children:
            assert isinstance(child, BaseLuppNode), "Children must be of type BaseLuppNode"
            child.parent = self
        self.name = name
        

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
        assert isinstance(child, BaseLuppNode), "Children must be of type BaseLuppNode"
        child.parent = self
        self.children.append(child)
