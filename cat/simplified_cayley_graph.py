import mod
import networkx as nx
import itertools


def remove_trivial(G, include_state, SCC, rm_system_edges = True):
    component_removed = []
    for c in SCC:
        component_removed.append(False)
        if rm_system_edges:
            G.remove_edges_from(c.edges)
        contains_repr = False
        for n in c.nodes:
            contains_repr = any(i in G.nodes[n]["atom_state"] for i in
                    include_state)
            if contains_repr: break
        if len(c.nodes) > 1 or contains_repr or len(list(G.out_edges(c.nodes))) == 0: 
            continue
        ine = G.in_edges(c.nodes)
        oute = G.out_edges(c.nodes)
        for in_e, out_e in itertools.product(ine, oute):
            # lbl = str(G.edges[in_e]["label"]) + "," + str(G.edges[out_e]["label"])
            lbl = ""
            src, tar = in_e[0], out_e[1]
            G.add_edge(src, tar, label = lbl)
        component_removed[-1] = True
        G.remove_nodes_from(c.nodes)
    return component_removed


def repr_graph(G, SCC, repr_atoms):
    Q = nx.DiGraph()
    g2q = {}
    for c in SCC:
        r = []
        for n in c.nodes:
            if all(a in repr_atoms for a in G.nodes[n]["atom_state"]):
                r.append(n)
        if len(r) == 0:
            r = [n for n in c.nodes]
        assert(len(r) > 0)
        for n in r:
            Q.add_node(n, label = G.nodes[n]["label"])
        for n in c.nodes:
            g2q[n] = r[0]

    for e in G.edges:
        Q.add_edge(g2q[e[0]], g2q[e[1]], label = G.edges[e]["label"])

    return Q


class SimplifiedCayleyGraph:
    def __init__(self, state_space, include_trivial=False,
            include_trivial_states = [],
            repr_state=None, remove_system_edges = True):
        self.state_space = state_space
        G = self.state_space.get_nxgraph()
        SCC = list(G.subgraph(c).copy() for c in nx.strongly_connected_components(G))
        num_non_triv = len([c for c in SCC if len(c.nodes) > 1])
        if not include_trivial:
            component_removed = remove_trivial(G,
                    include_trivial_states, SCC)
        else:
            component_removed = [False for c in SCC]
        SCC = [c for i, c in enumerate(SCC) if not component_removed[i]]
        if repr_state:
            self.skeleton = repr_graph(G, SCC, repr_state)
            self.SCC = SCC
        else:
            self.skeleton = G
            self.SCC = SCC

    def print_subsystem(self, state = (1,5,6,7), path = "cycle_graph",
            engine = "dot"):
        G = self.state_space.get_nxgraph()
        SCC = list(G.subgraph(c).copy() for c in nx.strongly_connected_components(G))
        g = None
        gn = None
        for c in SCC:
            for n in c.nodes:
                if G.nodes[n]["atom_state"] == state:
                    g = c
                    gn = n
                    break

        A = nx.nx_agraph.to_agraph(g)
        A.graph_attr.update(overlap = "false")
        an = A.get_node(gn)
        an.attr["color"] = "red"
        A.layout(prog = engine)
        A.draw(path + ".pdf")

    def print(self, path="out/subsystem", print_skeleton=True, engine="dot"):
        if print_skeleton:
            A = nx.nx_agraph.to_agraph(self.skeleton)
            for i, c in enumerate(self.SCC):
                style = "filled"
                if len(c) == 1:
                    style = "dotted"
                C = A.subgraph(nbunch=c.nodes, name = "cluster%d"%i,
                        style = style, color = "lightgrey")
        else:
            G = self.state_space.get_nxgraph()
            node_color = ["blue", "red", "yellow", "green", "purple", "orange", "cyan3", "orangered", "orchid", "limegreen", "peru"]
            coli = 0
            for comp in self.SCC:
                if len(comp) < 2: continue
                for v in comp:
                    G._node[v]["color"] = node_color[coli]
                coli += 1
                coli = coli%len(node_color)
            A = nx.nx_agraph.to_agraph(G)

        A.layout(prog = engine)
        A.draw(path+".pdf")
        file_name = path
        with open(f"{file_name}.tex", "w") as f:
            f.write(r"\begin{center}" + "\n")
            f.write(r"\includegraphics[width=\textwidth]{./" + file_name + ".pdf}" + "\n")
            f.write(r"\end{center}" + "\n")
        mod.post(f"summaryInput {file_name}.tex")
