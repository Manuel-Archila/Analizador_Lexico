from graphviz import Digraph
from Postfix_converter import *
from Thompson import *
from collections import *
from checker import *
from to_AFD import to_AFD


running = True
while running:
    input_regex = input("Ingrese la expresion regular: ")

    checker = Checker(input_regex)
    accepted, errors, new_regex = checker.checkRegex()
    for i in errors:
        print(i+"\n")
    if accepted:
        converter = Postfix_converter(new_regex)
        print(converter.postfix)
        print("El lenguaje de la expresion regular es: ", converter.language)
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
            elif i.start:
                afn.node('initial', shape = 'none', label='')
                afn.node(str(i.value))
                afn.edge('initial', str(i.value))
            else:
                afn.node(str(i.value))

        for i in ordered_nodes:
            for j in i.transitions.keys():
                for k in i.transitions[j]:
                    afn.edge(str(i.value), str(k), label = j)

        afn.render('./render/AFN.gv')

        initialc = thomp_afn[0]
        finalc = thomp_afn[1]
        route = thomp.route
        alphabet =converter.language
        toAFD = to_AFD()
        AFD = toAFD.toAFD(alphabet, initialc, route, finalc)


        afd_subconjuntos = Digraph(format="png", graph_attr={'rankdir': 'LR'})

        first_node = AFD[0]
        ordered_nodes = []
        visited_nodes = {first_node}
        queue = deque([first_node])
        while queue:
            node = queue.popleft()
            ordered_nodes.append(node)
            for i in node.transitions.keys():
                for j in node.transitions[i]:
                    if j not in visited_nodes:
                        for k in AFD:
                            if k.value == j:
                                visited_nodes.add(j)
                                queue.append(k)
                            
        for i in ordered_nodes:
            if i.end:
                afd_subconjuntos.node(str(i.value), peripheries = '2')
            elif i.start:
                afd_subconjuntos.node('initial', shape = 'none', label='')
                afd_subconjuntos.node(str(i.value))
                afd_subconjuntos.edge('initial', str(i.value))
            else:
                afd_subconjuntos.node(str(i.value))

        for i in ordered_nodes:
            for j in i.transitions.keys():
                for k in i.transitions[j]:
                    afd_subconjuntos.edge(str(i.value), str(k), label = j)

        afd_subconjuntos.render('./render/AFD_subconjuntos.gv')

        


        contine = input("Desea ingresar otra expresion regular? (y/n)")
        if contine == 'n':
            running = False
