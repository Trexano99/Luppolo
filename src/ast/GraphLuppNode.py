


from src.utils.LuppoloLogger import LuppoloLogger


class GraphLuppNode():
    '''
    This class represent a graphicable Luppolo Node in the AST.
    The class has been created due to semplify the graph rapresentation of the AST.
    '''

    def __init__(self, baseLuppNode):
        '''
        This method initializes the GraphLuppNode object.
        The method takes the following parameters:
        - baseLuppNode: the base Luppolo node to rapresent in the graph.
        '''
        self.baseLuppNode = baseLuppNode
        self.grapAttributes = {}
        self.nodeId = str(id(baseLuppNode))

    def updateGraphAttribute(self, attribute:tuple):
        ''' 
        This method updates the graph attributes for the node.
        The attributes are added to the node table, and they are stored as 
        key-value pairs in a dictionary. Updating an attribute with the same key
        will overwrite the previous value.
        '''
        self.grapAttributes[attribute[0]] = attribute[1]

    def developGraph(self, graph):
        ''' 
        This method develops the graph for the node and its children.
        Return the id of this node
        '''

        LuppoloLogger.logDebug(f"Developing Graph for node {self.baseLuppNode.name}")
        # Construct the node table
        label = self.__constructNodeTable()

        # Define the node with the custom label
        graph.node(name=self.nodeId, label=label, shape='plaintext')

        # Recursively add edges and develop the graph for child nodes
        for child in self.baseLuppNode.children:
            childId = child.getGraphRapresentation(graph)
            graph.edge(self.nodeId, childId)
        return self.nodeId
    
    def __constructNodeTable(self):
        '''
        This method constructs the table for the node
        Return the table label
        '''
        # Construct a table label
        label = f"""<<table border="0" cellborder="1" cellspacing="0">"""
        # Add the node name
        label += f'<tr><td colspan="2"><b>{self.baseLuppNode.name}</b></td></tr>'
        #Add the attribute lines
        label += ''.join(self.__constructAttributesTableLines())
        # Close the table
        label += '</table>>'
        return label

    def __constructAttributesTableLines(self):
        '''
        This method constructs the lines of the attributes table.
        Return the lines of the attributes table.
        '''
        lines = []
        for attribute in self.grapAttributes.items():
            lines.append(f'<tr><td><b>{attribute[0]}</b></td><td>{attribute[1]}</td></tr>')
        return lines

