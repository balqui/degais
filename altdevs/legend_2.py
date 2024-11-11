import graphviz as gvz
palette = ( # original color sequence by Ely,
                         # except transparent instead of white
                        'transparent', 'black', 'blue', 'blueviolet',
                        'brown', 'burlywood', 'cadetblue', 
                        'chartreuse', 'coral', 'crimson', 'cyan',
                        'darkorange', 'deeppink', 'deepskyblue', 
                        'forestgreen', 'gold', 'greenyellow',
                        'hotpink', 'orangered', 'pink', 'red',
                        'seagreen', 'yellow') 


gvgraph = gvz.Digraph(graph_attr = { "compound": "true", "newrank": "true", 
"ranksep" : "0.1", "fontname" : "Courier New" })
with gvgraph.subgraph(graph_attr = { "rank" : "same" }) as sg0:
    sg0.node("sg0t", shape = "none", label = '')
    sg0.node("sg0h", shape = "none", label = "10 - 50")
    # ~ sg0.node("sg0h", shape = "none", label = "10 - 50        ")
    sg0.edge("sg0t", "sg0h", color = palette[4], arrowhead = "none", penwidth = "2.5" )
with gvgraph.subgraph(graph_attr = { "rank" : "same"}) as sg1:
    sg1.node("sg1t", shape = "none", label = '')
    sg1.node("sg1h", shape = "none", label = "100 - 150")
    sg1.edge("sg1t", "sg1h", color = palette[5], arrowhead = "none", penwidth = "2.5" )
with gvgraph.subgraph(graph_attr = { "rank" : "same" }) as sg2:
    sg2.node("sg2t", shape = "none", label = '')
    sg2.node("sg2h", shape = "none", label = "1000 - 1050")
    sg2.edge("sg2t", "sg2h", color = palette[6], arrowhead = "none", penwidth = "2.5" )

with gvgraph.subgraph(graph_attr = { "rankdir" : "TB", "rank" : "same" }) as vert:
    gvgraph.edge("sg0h", "sg1h", color = palette[0])
    gvgraph.edge("sg1h", "sg2h", color = palette[0])

gvgraph.render(view = True)
