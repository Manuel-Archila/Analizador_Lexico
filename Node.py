class Node(object):
    def __init__(self, start = False, end = False, transitions = {}, value = ""):
        self.start = start
        self.end = end
        self.transitions = transitions
        self.value = value
    
    def addTransition(self, element, node):
        if element in self.transitions.keys():
            self.transitions[element].append(node.value)
            #self.nextmove[element].append(node)
        else:
            self.transitions[element] = [node.value]
            #self.nextmove[element]=[node]
    
    def __repr__(self): 
        return "Node: " + self.value + " Start: " + str(self.start) + " End: " + str(self.end) + " Transitions: " + str(self.transitions)

    #def __repr__(self):
        #return self.value
        