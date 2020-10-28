import mod
import networkx as nx


class State:
    def __init__(self, atom_state, e, t):
        self._atom_state = tuple(atom_state)
        self._key = self._atom_state
        self._neighbors = []
        self.edge = e
        self.trans = t

    def add_neighbor(self,state):
        self._neighbors.append(state)

    def transition_always(self, e, ts):
        new_states = set()
        for t in ts:
            should_fire = False
            new_atom_state = list(self._atom_state)
            for i in range(len(new_atom_state)):
                new_atom_state[i] = t[new_atom_state[i]]
                if new_atom_state[i] != self._atom_state[i]:
                    should_fire = True
            if should_fire:
                new_states.add(State(new_atom_state, e, t))
        return new_states

    def transition(self, e, ts):
        new_states = set()
        for t in ts:
            new_atom_state = list(self._atom_state)
            for i in range(len(new_atom_state)):
                new_atom_state[i] = t[new_atom_state[i]]
            new_states.add(State(new_atom_state, e, t))
        return new_states

    def is_enabled(self, e, ts):
        t = ts[0]
        atom_state = self._atom_state
        for i in range(len(self._atom_state)):
            if atom_state[i] != t[self._atom_state[i]]:
                return True
        return False

    def __str__(self):
        return str(self._atom_state)

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other):
        return self._key == other._key


class ProjectedCayleyGraph:
    def __init__(self, atomTrace, semigroup):
        self.dg = semigroup.dg
        self.semigroup = semigroup
        atom_state = [self.semigroup.get_id(v) for v in atomTrace]
        self.initialState = State(atom_state, None, None)
        self._state_space = []
        self.has_nxgraph = False

    def get_label(self, state):
        lbl = "("
        for i, a in enumerate(state._atom_state):
            if a in self.semigroup.fix_ids:
                lbl += '_'
            else:
                lbl += str(a)
            if i + 1 < len(state._atom_state):
                lbl += ", "
        lbl += ")"
        return lbl

    def get_nxgraph(self):
        # if self.has_nxgraph:
        #     return self._nxgraph

        nxgraph = nx.DiGraph()
        idmap = {}
        for i, state in enumerate(self._state_space):
            idmap[state] = i
            # nxgraph.add_node(str(i), label = str(state._atom_state),
            #         atom_state = state._atom_state)
            nxgraph.add_node(str(i), label = self.get_label(state),
                    atom_state = state._atom_state)

        for i, state in enumerate(self._state_space):
            for adj_state in state._neighbors:
                nxgraph.add_edge(str(i), str(idmap[adj_state]), label = str(adj_state.trans.id))

        self.has_nxgraph = True
        self._nxgraph = nxgraph
        return nxgraph

    def compute_stubborn(self, state):
        ke = None
        for e in self.dg.edges:
            if state.is_enabled(e, self.semigroup[e]):
                ke = e
                break
        if not ke: return []

        marked = {e: False for e in self.dg.edges}
        marked[e] = True
        ssets = [ke]
        stack = [ke]
        while stack:
            e = stack.pop()
            for hv in e.sources:
                for ep in hv.outEdges:
                    if marked[ep]: continue
                    if not state.is_enabled(ep, self.semigroup[ep]): continue
                    marked[ep] = True
                    stack.append(ep)
                    ssets.append(ep)
            for hv in e.targets:
                for ep in hv.outEdges:
                    if marked[ep]: continue
                    if state.is_enabled(ep, self.semigroup[ep]): continue
                    marked[ep] = True
                    stack.append(ep)
        return ssets

    def find_path(self, src, tar):
        nxgraph = self.get_nxgraph()
        for v in nxgraph.nodes():
            if nxgraph.nodes[v]["atom_state"] == src:
                vsrc = v
            if nxgraph.nodes[v]["atom_state"] == tar:
                vtar = v
        assert(src is not None and tar is not None)
        path = nx.shortest_path(nxgraph, vsrc, vtar)
        atom_path = [nxgraph.nodes[p]["atom_state"] for p in path]
        return atom_path

    def calc(self, max_iter = None):
        used_states = set()
        used_states.add(self.initialState)
        active_states = [self.initialState]

        num_iter = 0
        while active_states:
            num_iter += 1
            if max_iter and max_iter <= num_iter: break

            state = active_states.pop()
            # for e in self.compute_stubborn(state):
            for e in self.dg.edges:
                new_state_list = state.transition_always(e, self.semigroup[e])
                if new_state_list is None: continue

                for new_state in new_state_list:
                    state.add_neighbor(new_state)
                    if new_state in used_states: 
                        continue
                    
                    used_states.add(new_state)
                    active_states.append(new_state)
            if len(used_states) % 500 == 0:
                print("iter %d: %d found states" % (num_iter, 
                    len(used_states)))

        self._state_space = list(used_states)

    def print(self, path = "out/statespace", engine="dot"):
        g = self.get_nxgraph()
        A = nx.nx_agraph.to_agraph(g)
        if engine == "neato":
            A.graph_attr.update(overlap='false')
        A.layout(prog = engine)
        # A.node_attr.update(fontsize="20", landscape='true',ranksep='1')
        # A.edge_attr.update(fontsize="20")
        A.draw(path+".pdf")
        file_name = path
        with open(f"{file_name}.tex", "w") as f:
            f.write(r"\begin{center}" + "\n")
            f.write(r"\includegraphics[width=\textwidth]{./" + file_name + ".pdf}" + "\n")
            f.write(r"\end{center}" + "\n")
        mod.post(f"summaryInput {file_name}.tex")


    def __len__(self):
        return len(self._state_space)

