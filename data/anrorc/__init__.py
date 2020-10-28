import mod
from mod import smiles, ruleGML
import os


def p(path):
    return mod.CWDPath(os.path.join(os.path.dirname(__file__), path))


# Grammar
h2n = smiles("[NH2-]", name="H2N")
h3n = smiles("N", name="H3N")
hydrogen = smiles("[H]", name="Hydrogen")
water = smiles("O", name="Water")
pobr = smiles("O=P(Br)(Br)Br", name="POBr3")
initmol = mod.graphGML(p("graphs/initmol.gml"), name="initmol")

r1to1b = ruleGML(p("rules/1_1b.gml"))
r1to1b.name = "1 -> 1b"
r1bto1c = ruleGML(p("rules/1b_1c.gml"))
r1bto1c.name = "1b -> 1c"
r1cto1d = ruleGML(p("rules/1c_1d.gml"))
r1cto1d.name = "1c -> 1d"
r1to2 = ruleGML(p("rules/1_2.gml"))
r1cto1d.name = "1 -> 2"

r1dto2 = ruleGML(p("rules/1d_2.gml"))
r1dto2.name = "1d -> 2"
r2to3 = ruleGML(p("rules/2_3.gml"))
r2to3.name = "2 -> 3"
r3to4 = ruleGML(p("rules/3_4.gml"))
r3to4.name = "3 -> 4"

# Chemical Network
dg = mod.DG(graphDatabase=mod.inputGraphs)
with dg.build() as b:
    es = b.apply([initmol, h2n], r1to1b)
    g_1b = list(es[0].targets)[0].graph
    es = b.apply([g_1b, hydrogen], r1bto1c)
    g_1c = list(es[0].targets)[0].graph
    es = b.apply([g_1c], r1cto1d)
    g_1d = list(es[0].targets)[1].graph
    b.apply([g_1d, hydrogen, hydrogen], r1dto2)

    b.apply([initmol, h3n], r1to2)
    g_2 = list(es[0].targets)[0].graph
