class node: #class object for nodes
    def __init__(self, state ,parent, children,right,level, visited, isfirst, isleaf, score):
        self.state = state #board of the node
        self.parent = parent #node parent
        self.children = children #list of node children
        self.right = right #node on its right
        self.level = level 
        self.visited = visited #whether its been visited when creating
        self.isfirst = isfirst #whether its the first parent node
        self.isleaf = isleaf
        self.score = score

