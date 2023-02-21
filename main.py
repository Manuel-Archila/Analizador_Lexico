import pydot
from Postfix_converter import *
from Thompson import *
converter = Postfix_converter("(a|b)|c+")
thomp = Thompson(converter.postfix)
thomp_afn = thomp.construction()
thomp_afn[0].start = True
thomp_afn[1].end = True

afn = pydot.Dot(graph_type='digraph', rankdir='LR')


for i in thomp.route:
    if i.end:
        temp_node = pydot.Node(str(i.value), peripheries = '2')
    else:
        temp_node = pydot.Node(str(i.value))
    afn.add_node(temp_node)

for i in thomp.route:
    for j in i.transitions.keys():
        for k in i.transitions[j]:
            if j == "ε":
                afn.add_edge(pydot.Edge(str(i.value),str(k), label = "&"))
            else:
                afn.add_edge(pydot.Edge(str(i.value), str(k), label = j))

afn.write_png('afn.png')
