from Branch import Branch

class Branches(object):
    def __init__(self):
        self.counter = 0
        self.followpos = {}
        self.branches = []
        self.b_operators = ["|", "."]
        self.u_operators = ["+", "*"]
        self.operators = ["|", ".", "+", "*"]
        self.acceptance_value = 0

    def unite(self,operand,elements):
        if operand =="*":
            self.branches.append(elements[0])
            return Branch(value=operand,leftChildren=elements[0])
        if operand =="+":
            self.branches.append(elements[0])
            return Branch(value=operand,leftChildren=elements[0])
        if operand =="|":
            self.branches.append(elements[0])
            self.branches.append(elements[1])
            return Branch(value=operand,leftChildren=elements[1],rightChildren=elements[0])
        if operand ==".":
            self.branches.append(elements[0])
            self.branches.append(elements[1])
            return Branch(value=operand,leftChildren=elements[1],rightChildren=elements[0])
    
    def simpleTrans(self, value):
        self.counter += 1
        self.followpos[self.counter] = []
        branch = Branch(value=value,pos=self.counter)
        if value == "#":
            self.acceptance_value = self.counter
        return branch
    
    def tree(self, stack):
        first_pop = stack.pop()

        if first_pop in self.b_operators:
            pop1 = stack.pop()
            if pop1 in self.operators:
                stack.append(pop1)
                pop1 = self.tree(stack)
            
            pop2 = stack.pop()
            if pop2 in self.operators:
                stack.append(pop2)
                pop2 = self.tree(stack)
            
            if type(pop1) == str:
                pop1 = self.simpleTrans(pop1)
            
            if type(pop2) == str:
                pop2 = self.simpleTrans(pop2)

            return self.unite(first_pop, [pop1, pop2])
        
        else:
            pop1 = stack.pop()
            if pop1 in self.operators:
                stack.append(pop1)
                pop1 = self.tree(stack)
            
            if type(pop1) == str:
                pop1 = self.simpleTrans(pop1)
            
            return self.unite(first_pop, [pop1])
    
    def Followpos(self,root):
        #print("se llama a followpos")
        if root.rightChildren:
            self.Followpos(root.rightChildren)
            
        if root.leftChildren :
            self.Followpos(root.leftChildren)
        
       
        #Raiz es concatenación
        if root.value =='.':
            for element in root.leftChildren.lastpos:
                if element not in self.followpos:
                    self.followpos[element]=[]
                
                for followposI in root.rightChildren.firstpos:
                    if followposI not in self.followpos[element]:
                        self.followpos[element].append(followposI)

                        self.followpos[element].sort()

        #Raiz es Kleene
        if root.value =='*':
            for element in root.leftChildren.lastpos:
                if element not in self.followpos:
                    self.followpos[element]=[]
                
                for followposI in root.leftChildren.firstpos:
                    if followposI not in self.followpos[element]:
                        self.followpos[element].append(followposI)
        
                        self.followpos[element].sort()

