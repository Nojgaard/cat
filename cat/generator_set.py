from cat.transformation import Transformation
import mod


class GeneratorSet:
    def __init__(self, dg, fun_ignore=lambda v: False, fix_vertices=[], rename_fix_verts=False,
                 transformations=None):
        self.dg = dg
        self.ignore_vertex = fun_ignore
        self.id_map = PointMap(dg, self.ignore_vertex)
        self.fix_ids = [self.get_id(v) for v in fix_vertices if self.has_id(v)]

        self.transformation_map = {e: set() for e in dg.edges}

        if transformations is not None:
            emap = {}
            for e in dg.edges:
                left_ids = tuple(sorted(self.get_id(v) for w in e.sources for v in w.graph.vertices if self.has_id(v)))
                right_ids = tuple(sorted(self.get_id(v) for w in e.targets for v in w.graph.vertices if self.has_id(v)))
                emap[(left_ids, right_ids)] = e

            for t in transformations:
                left_ids = tuple(sorted(t.left_map))
                right_ids = tuple(sorted(t.right_map))
                self.transformation_map[emap[(left_ids, right_ids)]].add(t)
            return

        tid = 0
        for i, e in enumerate(dg.edges):
            vm = mod.dgVertexMap(dg, e, self.ignore_vertex)

            for m in vm.maps:
                left_map = []
                right_map = []

                for left_point in vm.getLeft().vertices:
                    assert(not left_point.isNull())
                    if fun_ignore(left_point.vertex): continue
                    right_point = m.leftToRight(left_point)
                    if fun_ignore(right_point.vertex): continue

                    # print("vid:", left_point.id, "gid:", left_point.graphId)

                    lpid = self.get_id(left_point.vertex)
                    if lpid in self.fix_ids: continue

                    rpid = self.get_id(right_point.vertex)
                    if rename_fix_verts and rpid in self.fix_ids:
                        rpid = self.fix_ids[0]
                    left_map.append(lpid)
                    right_map.append(rpid)

                t = Transformation(tid, left_map, right_map)
                if t not in self.transformation_map[e]:
                    tid += 1
                self.transformation_map[e].add(t)

    def get_id(self, dg_vertex):
        return self.id_map.point_to_id(dg_vertex)

    def get_vertex(self, dg_vertex_id):
        return self.id_map.id_to_point(dg_vertex_id)

    def has_id(self, dg_vertex):
        return self.id_map.has_id(dg_vertex)

    def __getitem__(self, e):
        return self.transformation_map[e]

    def _print_transformations(self, f, e, vertex_visible, trace_limit):
        color_list = ["red", "blue", "cyan", "green"]
        for i, t in enumerate(self[e]):
            if trace_limit is not None and i >= trace_limit:
                break
            for hv in e.sources:
                if vertex_visible and not vertex_visible(hv.graph, self.dg): continue
                for vLeft in hv.graph.vertices:
                    if not self.has_id(vLeft): continue
                    lid = self.get_id(vLeft)
                    rid = t[lid]
                    if lid == rid: continue

                    vRight = self.get_vertex(rid)
                    if vertex_visible and not vertex_visible(vRight.graph, self.dg): continue

                    bendDir = "bend left" if i%2 == 1 else "bend right"
                    vDGLeft = self.dg.findVertex(vLeft.graph)
                    vDGRight = self.dg.findVertex(vRight.graph)
                    line = "\\draw[derEdge, %s, ->, %s] (v-%d-%d-v-%d) to (v-%d-%d-v-%d);\n" \
                            % (color_list[i%len(color_list)], bendDir, vDGLeft.id, 0, vLeft.id, vDGRight.id, 0, vRight.id)
                    f.write(line)
    
    def _print_path(self, f, path, vertex_visible):
        color_list = ["red", "blue", "orange", "green"]
        prev = path[0]
        for cur in path[1:]:
            for c, (srcid, tarid) in enumerate(zip(prev, cur)):
                vLeft = self.get_vertex(srcid)
                if vertex_visible and not vertex_visible(vLeft): continue
                vRight = self.get_vertex(tarid)
                if vertex_visible and not vertex_visible(vRight): continue
                vDGLeft = self.dg.findVertex(vLeft.graph)
                vDGRight = self.dg.findVertex(vRight.graph)
                line = "\\draw[derEdge, %s, ->, bend left] (v-%d-%d-v-%d) to (v-%d-%d-v-%d);\n" \
                        % (color_list[c], vDGLeft.id, 0, vLeft.id, vDGRight.id, 0, vRight.id)
                f.write(line)
            prev = cur

    def print_dg(self, file_path = "out/fig.tex", path_list = None,
            vertex_visible = None, edge_visible = None, draw_trace = True, collapse_hydrogens = True, trace_limit = None):
        dgPrinter = mod.DGPrinter()
        dgPrinter.withInlineGraphs = True
        dgPrinter.graphPrinter.collapseHydrogens = collapse_hydrogens
        if vertex_visible is not None:
            dgPrinter.pushVertexVisible(vertex_visible)
        if edge_visible is not None:
            dgPrinter.pushEdgeVisible(edge_visible)
        dgPrinter.withShortcutEdgesAfterVisibility = True

        # dgPrinter.setRotationOverwrite(lambda g: -30 if g.name != "Glycolaldehyde" else 0)

        f = self.dg.print(printer = dgPrinter)
        f = (f[0][:-4] + ".tex", f[1])
        fBase = f[0]
        fName = file_path
        mod.post("summaryInput \"%s\"" % fName)
        with open(fName, "w") as f:
            f.write("\\centering{ \\resizebox{0.8\\textwidth}{!}{%\n")
            f.write("\\input{%s}\n" % fBase)
            f.write("""\\begin{tikzpicture}[overlay, remember picture,
                    autEdge/.style={dashed, blue},
                    derEdge/.style={modRCMatchEdge},
            ]
            """)

            for hv in self.dg.vertices:
                if vertex_visible and not vertex_visible(hv): continue
                for v in hv.graph.vertices:
                    if not self.has_id(v): continue
                    vid = self.get_id(v)
                    lbl = "\\node [above=0.03cm of v-%d-%d-v-%d] {%d};\n" % (hv.id, 0, v.id, vid)
                    f.write(lbl)
            
            if draw_trace:
                if path_list is not None:
                    for path in path_list:
                        self._print_path(f, path, vertex_visible)
                else:
                    for e in self.dg.edges:
                        self._print_transformations(f, e, vertex_visible, trace_limit)

            f.write("\\end{tikzpicture}\n")
            f.write("}}\n")

    def __len__(self):
        return sum(len(ts) for ts in self.transformation_map.values())


class PointMap:
    def __init__(self, derivation_graph, ignore_point_func):
        self._id2point = {}
        self._point2id = {}

        point_id = 0
        for v in derivation_graph.vertices:
            for point in v.graph.vertices:
                if ignore_point_func(point): continue
                point_id += 1
                # print("Storing atom: (", point.id, ",", point.stringLabel, ",",  v.graph.name, ") as", point_id)
                self._id2point[point_id] = point
                self._point2id[point] = point_id

    def has_id(self, point):
        return point in self._point2id

    def id_to_point(self, i):
        return self._id2point[i]

    def point_to_id(self, point):
        return self._point2id[point]

