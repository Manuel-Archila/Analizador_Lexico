import pydot
from Postfix_converter import *
from Thompson import *
from collections import *




converter = Postfix_converter("(a|b)*|(c|d)*")
print(converter.postfix)
thomp = Thompson(converter.postfix)
thomp_afn = thomp.construction()
thomp_afn[0].start = True
thomp_afn[1].end = True


afn = pydot.Dot(graph_type='digraph', rankdir='LR')

first_node = thomp_afn[0]
ordered_nodes = []
visited_nodes = {first_node}
print(visited_nodes)
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
        temp_node = pydot.Node(str(i.value), peripheries = '2')
    else:
        temp_node = pydot.Node(str(i.value))
    afn.add_node(temp_node)

for i in ordered_nodes:
    for j in i.transitions.keys():
        for k in i.transitions[j]:
            if j == "ε":
                afn.add_edge(pydot.Edge(str(i.value),str(k), label = "&"))
            else:
                afn.add_edge(pydot.Edge(str(i.value), str(k), label = j))

afn.write_png('afn.png')
