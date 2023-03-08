class Simulator():
    
    def simulateAFD(self, string, node):
        self.movements = []
        actual_state = node
        for element in string:
            if actual_state.hasNext(element):
                #self.movements.append(actual_state.value + " " + element + " " + actual_state.getNext(element).value)
                actual_state = actual_state.getNext(element)[0]
            else:
                return False
        
        return actual_state.end
    