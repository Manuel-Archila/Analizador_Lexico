from graphviz import Digraph
from Postfix_converter import *
from Thompson import *
from collections import *
from checker import *
from to_AFD import to_AFD
from Direct import Direct
from Simulator import Simulator

def drawAF(nodes, name, route, p):
    af = Digraph(format="png", graph_attr={'rankdir': 'LR'})

    first_node = nodes[0]
    ordered_nodes = []
    visited_nodes = {first_node}
    queue = deque([first_node])
    while queue:
        node = queue.popleft()
        ordered_nodes.append(node)
        for i in node.transitions.keys():
            for j in node.transitions[i]:
                if j not in visited_nodes:
                    for k in route:
                        if k.value == j:
                            visited_nodes.add(j)
                            queue.append(k)
    
    new_ordered_nodes = []
    for i in ordered_nodes:
        if i not in new_ordered_nodes:
            new_ordered_nodes.append(i)
    
                        
    for i in new_ordered_nodes:
        if i.end:
            af.node(str(i.value), peripheries = '2')
        elif i.start:
            af.node('initial', shape = 'none', label='')
            af.node(str(i.value))
            af.edge('initial', str(i.value))
        else:
            af.node(str(i.value))

    for i in new_ordered_nodes:
        for j in i.transitions.keys():
            for k in i.transitions[j]:
                af.edge(str(i.value), str(k), label = j)

    af.render('./render/'+name+'.gv')



running = True
while running:
    input_regex = input("Ingrese la expresion regular: ")

    checker = Checker(input_regex)
    accepted, errors, new_regex = checker.checkRegex()
    for i in errors:
        print(i+"\n")
    if accepted:
        string = input("Ingrese la cadena a evaluar: ")
        converter = Postfix_converter(new_regex)
        postfix_exp = converter.postfix
        print(postfix_exp)
        #print("El lenguaje de la expresion regular es: ", converter.language)
        thomp = Thompson(converter.postfix)
        thomp_afn = thomp.construction()
        thomp_afn[0].start = True
        thomp_afn[1].end = True


        drawAF(thomp_afn, 'AFN', thomp.route, False)

        initialc = thomp_afn[0]
        finalc = thomp_afn[1]
        route = thomp.route
        alphabet =converter.language
        toAFD = to_AFD()
        AFD = toAFD.toAFD(alphabet, initialc, route, finalc)


        drawAF(AFD, 'AFD', AFD, False)

        direct = Direct(postfix_exp)
        direct_afd = direct.direct_construction(alphabet)

        drawAF(direct_afd, 'AFD_directo', direct_afd, True)

        print('Accepted' if toAFD.simulateAFN(thomp_afn[0], string, thomp_afn[1]) else 'Not Accepted')

        simulator = Simulator()

        print('Accepted' if simulator.simulateAFD(string, AFD[0]) else 'Not Accepted')

        print('Accepted' if simulator.simulateAFD(string, direct_afd[0]) else 'Not Accepted')


        contine = input("Desea ingresar otra expresion regular? (y/n)")
        if contine == 'n':
            running = False
