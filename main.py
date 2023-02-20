import pydot
from Postfix_converter import *
from Thompson import *
converter = Postfix_converter("a?b*")
#converter = Postfix_converter("(a|x*)a*|ε")
print(converter.postfix)
thomp = Thompson(converter.postfix)
thomp_afn = thomp.construction()
thomp_afn[0].start = True
thomp_afn[1].end = True
thomp.route.append(thomp_afn[0])

afn = pydot.Dot(graph_type='digraph')
for i in thomp.route:
    temp_node = pydot.Node("Node" + str(i.value))
    afn.add_node(temp_node)

for i in thomp.route:
    for j in i.transitions.keys():
        for k in i.transitions[j]:
            if j == "ε":
                afn.add_edge(pydot.Edge("Node" + str(i.value), "Node" + str(k), weight = "&epsilon"))
            else:
                afn.add_edge(pydot.Edge("Node" + str(i.value), "Node" + str(k), weight = j))

afn.write_png('afn.png')
