from graphviz import Digraph
from Postfix_converter import *
from Thompson import *
from collections import *
from checker import *


running = True
while running:
    input_regex = input("Ingrese la expresion regular: ")

    checker = Checker(input_regex)
    accepted, message, new_regex = checker.checkRegex()
    print(message)
    if accepted:
        converter = Postfix_converter(new_regex)
        print(converter.postfix)
        thomp = Thompson(converter.postfix)
        thomp_afn = thomp.construction()
        thomp_afn[0].start = True
        thomp_afn[1].end = True


        afn = Digraph(format="png", graph_attr={'rankdir': 'LR'})

        first_node = thomp_afn[0]
        ordered_nodes = []
        visited_nodes = {first_node}
        queue = deque([first_node])
        while queue:
            node = queue.popleft()
            ordered_nodes.append(node)
            for i in node.transitions.keys():
                for j in node.transitions[i]:
                    if j not in visited_nodes:
                        for k in thomp.route:
                            if k.value == j:
                                visited_nodes.add(j)
                                queue.append(k)
                            


        for i in ordered_nodes:
            if i.end:
                afn.node(str(i.value), peripheries = '2')
            else:
                afn.node(str(i.value))

        for i in ordered_nodes:
            for j in i.transitions.keys():
                for k in i.transitions[j]:
                    afn.edge(str(i.value), str(k), label = j)

        afn.render('./render/grapgh.gv', view=True)
        contine = input("Desea ingresar otra expresion regular? (y/n)")
        if contine == 'n':
            running = False
