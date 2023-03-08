from Branch import Branch
import Branches
from Node import Node

class Direct(object):
    def __init__(self, postfix):
        self.stack = []
        self.postfix = postfix + "#."
        self.final_pos = 0
        self.create_stack()
    
    def create_stack(self):
        for element in self.postfix:
            self.stack.append(element)

    
    def direct_construction(self, language):
        branch_creator = Branches.Branches()
        tree = branch_creator.tree(self.stack)
        branches = branch_creator.branches
        branches.append(tree)

        for i in branches:
            if i.nullable == None:
                self.nullable(i)
            if i.firstpos == None:
                self.firstpos(i)
            if i.lastpos == None:
                self.lastpos(i)
    
        branch_creator.Followpos(tree)
        #print(branch_creator.followpos)

        Dtran, Dstates = self.group_construction(branches, branch_creator, language)
        states = {}
        nodes = []
        counter = 1
        for n in Dstates:
            start = False
            end = False
            for element in n['group']:
                if element == branch_creator.acceptance_value:
                    end = True
            if counter == 1:
                start = True
            states[counter] = n['group']

            nodes.append(Node(start, end, {}, counter))
            counter += 1

        for trans in Dtran:
            for element in states:
                if Dtran[trans] == states[element]:
                    Dtran[trans] = element
        
        for n in nodes:
            for trans in Dtran:
                if trans[0] == n.value:
                    for node in nodes:
                        if node.value == Dtran[trans]:
                            #print(123)
                            n.addTransition(trans[1], node)
        return nodes

        
    def allMarked(self,states):
        temp = []
        for i in states:
            if i['marked']:
                temp.append(True)
            else:
                temp.append(False)
        return False if False in temp else True

    def group_construction(self, branches, branchc, language):
        first = branches[-1].firstpos
        Dtran = {}
        Dstates = [
            {
            "group": first,
            "marked": False,
            }
        ]
        counter= 0

        while(not self.allMarked(Dstates)):
            Dstates[counter]["marked"] = True
            temp_dict = Dstates[counter]
            for element in language:
                group = []
                for part in temp_dict["group"]:
                    for branch in branches:
                        if part == branch.pos and element == branch.value:
                            group.extend(branchc.followpos[part])
                iin = False
                group = sorted(list(dict.fromkeys(group)), reverse = False)
                for state in Dstates:
                    if state["group"] == group:
                        iin = True
                
                if not iin:
                    Dstates.append({
                        "group": group,
                        "marked": False,
                    })
                #print(Dstates)
                Dtran[counter+1, element] = group
                #print(Dtran)
            counter += 1
        return Dtran, Dstates
    
    def nullable(self, node):
        if node.value == "|":
            if node.rightChildren.nullable == None:
                self.nullable(node.rightChildren)
            if node.leftChildren.nullable == None:
                self.nullable(node.leftChildren)
            
            if node.rightChildren.nullable == True or node.leftChildren.nullable == True:
                node.nullable = True
            else:
                node.nullable = False
        elif node.value == ".":
            if node.rightChildren.nullable:
                self.nullable(node.rightChildren)
            
            if node.leftChildren.nullable:
                self.nullable(node.leftChildren)
            
            if node.rightChildren.nullable == True and node.leftChildren.nullable == True:
                node.nullable = True
            else:
                node.nullable = False
        elif node.value == "+":
            node.nullable = False
        elif node.value == "*":
            node.nullable = True
        else:
            if node.value == "ε":
                node.nullable = True
            else:
                node.nullable = False
        #print(node.value, node.nullable)
        
    def firstpos(self, node):
        if node.firstpos == None:
            if node.value == ".":
                if node.rightChildren.firstpos == None:
                    self.firstpos(node.rightChildren)
                if node.leftChildren.firstpos == None:
                    self.firstpos(node.leftChildren)
                
                if node.leftChildren.nullable == True:
                    node.firstpos = [*node.rightChildren.firstpos, *node.leftChildren.firstpos]
                else:
                    node.firstpos = [*node.leftChildren.firstpos]
            elif node.value == "|":
                if node.rightChildren.firstpos == None:
                    self.firstpos(node.rightChildren)
                if node.leftChildren.firstpos == None:
                    self.firstpos(node.leftChildren)
                
                node.firstpos = [*node.rightChildren.firstpos, *node.leftChildren.firstpos]
            elif node.value == "*":
                if node.leftChildren.firstpos == None:
                    self.firstPos(node.leftChildren)

                node.firstpos = [*node.leftChildren.firstpos]
                node.firstpos.sort()
            elif node.value == "+":
                if node.leftChildren.firstpos == None:
                    self.firstPos(node.leftChildren)

                node.firstpos = [*node.leftChildren.firstpos]
                node.firstpos.sort()
            else:
                node.firstpos = [node.pos]
        
        node.firstpos.sort()
        #print(node.value, node.firstpos)

    def lastpos(self, node):
        if node.lastpos == None:
            if node.value == "|":
                if node.leftChildren.lastpos == None:
                    self.lastPos(node.leftChildren)
                if node.rightChildren.lastpos == None:
                    self.lastPos(node.rightChildren)
                
                node.lastpos = [*node.rightChildren.lastpos, *node.leftChildren.lastpos]
            
            elif node.value == ".":
                if node.leftChildren.lastpos == None:
                    self.lastPos(node.leftChildren)
                if node.rightChildren.lastpos == None:
                    self.lastPos(node.rightChildren)
                
                if node.rightChildren.nullable == True:
                    node.lastpos = [*node.rightChildren.lastpos, *node.leftChildren.lastpos]
                else:
                    node.lastpos = [*node.rightChildren.lastpos]
            elif node.value == "+":
                if node.leftChildren.lastpos == None:
                    self.lastpos(node.leftChildren)
                node.lastpos = [*node.leftChildren.lastpos]
                node.lastpos.sort()
            elif node.value == "*":
                if node.leftChildren.lastpos == None:
                    self.lastpos(node.leftChildren)
                node.lastpos = [*node.leftChildren.lastpos]
                node.lastpos.sort()
            else:
                node.lastpos = [node.pos]
        node.lastpos.sort()
        #print(node.value, node.lastpos)
    







    


