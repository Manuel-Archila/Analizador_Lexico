from Node import Node

class Thompson(object):
    def __init__(self, postfix):
        self.operands = ["|", "+", "*", "."]
        self.b_operands = ["|", "."]
        self. u_operands = ["+", "*"]
        self.nodes = []
        self.postfix = postfix
        self.counter = 0
        self.route = []
        self.stack = []
        self.createStack()

    def getRoute(self):
        for i in self.route:
            print(i)

    def createStack(self):
        for i in self.postfix:
            self.stack.append(i)

    def assignValue(self):
        self.counter += 1
        return str(self.counter)

    def sTransition(self, element):
        n1 = Node(False, False, {}, self.assignValue())
        #print("n1 is ", n1)
        n2 = Node(False, False, {}, self.assignValue())
        #print("n2 is ", n2)

        #print(n1, " va a ", n2, " con ", element)
        n1.addTransition(element, n2)

        self.route.append(n1)
        self.route.append(n2)

        return [n1, n2]

    
    def positive(self, expression):
        n1 = Node(False, False, {}, self.assignValue())
        n2 = expression[0]
        n3 = expression[1]
        n4 = Node(False, False, {}, self.assignValue())

        n1.addTransition("ε", n2)
        n3.addTransition("ε", n4)
        n3.addTransition("ε", n2)

        self.route.append(n1)
        self.route.append(n4)

        return [n1, n4]

    def kleene(self, expression):
        #print(expression)
        n1 = Node(False, False, {}, self.assignValue())
        n2 = expression[0]
        n3 = expression[1]
        n4 = Node(False, False, {}, self.assignValue())

        n1.addTransition("ε", n2)
        n1.addTransition("ε", n4)
        n3.addTransition("ε", n4)
        n3.addTransition("ε", n2)

        self.route.append(n1)
        self.route.append(n4)

        return [n1, n4]

    def concatenation(self, expression):
        n1 = expression[1][1]
        #print("n1 is ", n1)
        n2 = expression[0][0]
        #print("n2 is ", n2)
        n3 = expression[1][0]
        #print("n3 is ", n3)
        n4 = expression[0][1]
        #print("n4 is ", n4)

        n1.addTransition("ε",n2)


        return [n3, n4]

    def orr(self, expression):
        n1 = Node(False, False, {}, self.assignValue())
        #print("n1 is ", n1)
        n2 = expression[1][0]
        #print("n2 is ", n2)
        n3 = expression[1][1]
        #print("n3 is ", n3)
        n4 = expression[0][0]
        #print("n4 is ", n4)
        n5 = expression[0][1]
        #print("n5 is ", n5)
        n6 = Node(False, False, {}, self.assignValue())
        #print("n6 is ", n6)

        n1.addTransition("ε", n2)
        n1.addTransition("ε", n4)
        n3.addTransition("ε", n6)
        n5.addTransition("ε", n6)

        self.route.append(n1)
        self.route.append(n6)

        return [n1, n6]
    
    def unite(self, operand, expression):
        if operand == "+":
            return self.positive(expression)
        elif operand == "*":
            return self.kleene(expression)
        elif operand == ".":
            return self.concatenation(expression)
        elif operand == "|":
            return self.orr(expression)

        

    def construction(self):
        first_pop = self.stack.pop()
        if first_pop in self.b_operands:
            #print("first_pop, es un operador binario", first_pop)
            pop1 = self.stack.pop()
            #print("pop1", pop1)
            if pop1 in self.operands:
                #print("pop1, es un operador", pop1)
                self.stack.append(pop1)
                pop1 = self.construction()
            pop2 = self.stack.pop()
            if pop2 in self.operands:
                #print("pop2, es un operador", pop2)
                self.stack.append(pop2)
                pop2 = self.construction()
            
            if type(pop1) == str:
                #print("hice transicion a pop1", pop1)
                pop1 = self.sTransition(pop1)
            
            if type(pop2) == str:
                #print("hice transicion a pop2", pop2)
                pop2 = self.sTransition(pop2)
            
            #print(first_pop)
            #print(pop1)
            #print(pop2)
            return self.unite(first_pop, [pop1, pop2])
        elif first_pop in self.u_operands:
            #print("first_pop, es un operador unario", first_pop)
            pop1 = self.stack.pop()
            if pop1 in self.operands:
                self.stack.append(pop1)
                pop1 = self.construction()
            
            if type(pop1) == str:
                #print("hice transicion a pop1", pop1)
                pop1 = self.sTransition(pop1)
            #print(first_pop, pop1)
            return self.unite(first_pop, pop1)
        else:
            #print("first_pop, es un simbolo", first_pop)
            return self.sTransition(first_pop)
        
