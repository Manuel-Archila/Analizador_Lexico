from Node import Node

class to_AFD(object):
    def __init__(self):
        self.Dstates = {}
        self.visited_nodes = []

    def e_closure(self, node):
        #reachable_states_nodes = []
        reachable_states_text = []
        reachable_states_text.append(node.value)
        #reachable_states_nodes.append(node)
        actual_node = node
        if actual_node not in self.visited_nodes:
            self.visited_nodes.append(actual_node)
        while (actual_node.hasNext("ε")):
            available_nodes = actual_node.getNext("ε")
            for i in available_nodes:
                if i not in self.visited_nodes:
                    reachable_states_text+=i.value
                    self.visited_nodes.append(i)
                    reachable_states_text+=self.e_closure(i)[0]
            actual_node = available_nodes[0]
        
        sorted_states = sorted(list(set(reachable_states_text)))
        return [sorted_states, self.visited_nodes]
    
    def state_names(self, subset):
        name = ""
        for i in subset:
            name += i
        return name
    
    def move(self, node, element):
        return node.getNext(element)
    
    def toAFD(self, alphabet, start, T, end):
        next_state = []
        node_value = 1
        node_transition = alphabet

        actual_state = self.e_closure(start)
        acceptance = False
        if end in actual_state[1]:
            acceptance = True
        self.Dstates[self.state_names(actual_state[0])] = Node(True, acceptance, {}, str(node_value))
        next_state.append(actual_state)
        self.visited_nodes = []

        while(len(next_state) > 0):
            actual_state = next_state.pop(0)

            for node in actual_state[1]:
                if node in T:
                    T.remove(node)
            
            for element in node_transition:
                visited_elements = []
                state_name = ""
                for node in actual_state[1]:
                    if self.move(node, element):
                        state_name+=node.value
                        visited_elements.append(node.getNext(element)[0])
            
                union_text = []
                union_nodes = []

                if len(visited_elements) != 0:

                    for eclosure_node in visited_elements:
                        e_closure = self.e_closure(eclosure_node)

                        union_text += e_closure[0]
                        for i in e_closure[1]:
                            if i not in union_nodes:
                                union_nodes.append(i)
                        self.visited_nodes = []

                    union_text = sorted(list(set(union_text)))
                    union_text = self.state_names((union_text))

                    if union_text not in self.Dstates:
                        acceptance = False
                        if end in union_nodes:
                            acceptance = True
                        node_value +=1
                        self.Dstates[union_text] = Node(False, acceptance, {}, str(node_value))
                        next_state.append([union_text, union_nodes])
                        self.Dstates[self.state_names(actual_state[0])].addTransition(element, self.Dstates[union_text])
                    else:
                        self.Dstates[self.state_names(actual_state[0])].addTransition(element, self.Dstates[union_text])
        
        
        route = []
        for key in self.Dstates: 
            route.append(self.Dstates[key])
        return route
    
    def simulateAFN(self, start, string, end):
        next_trans = []
        node_transition = []
        for i in string:
            next_trans.append(i)
        
        actual_state = self.e_closure(start)
        self.visited_nodes = []
        if start.value == end.value and len(next_trans) == 0:
            return True
        elif len(next_trans) == 0:
            for node_e2 in actual_state[1]:
                if node_e2.value == end.value:
                    return True
            return False
        
        transition = next_trans.pop(0)
        for node_e in actual_state[1]:
            if node_e.hasNext(transition):
                node_transition.append(node_e.getNext(transition))
        
        if len(node_transition) == 0:
            return False

        for visited_node in node_transition:
            temp = self.simulateAFN(visited_node[0], string[1:len(string)], end)
            if temp:
                return True
        return False

        
                    
                    