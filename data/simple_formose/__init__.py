import mod
import os


def p(path):
    return mod.CWDPath(os.path.join(os.path.dirname(__file__), path))


glycolaldehyde = mod.smiles("OCC=O", "Glycolaldehyde")
g1 = mod.smiles("C(O)=CO", "p_0")
g2 = mod.smiles("C(C(C(CO)O)O)=O", "p_1")
ketoEnol_F = mod.ruleGML(p("keto_enol_forward.gml"))
ketoEnol_B = mod.ruleGML(p("keto_enol_backward.gml"))
aldolAdd_F = mod.ruleGML(p("aldol_addition_forward.gml"))
aldolAdd_B = mod.ruleGML(p("aldol_addition_backward.gml"))

ders = [
    [ketoEnol_F, [glycolaldehyde], [g1]],
    [ketoEnol_B, [g1], [glycolaldehyde]],
    [aldolAdd_F, [glycolaldehyde, g1], [g2]]
]
dg = mod.DG()
with dg.build() as b:
    for r, left, right in ders:
        d = mod.Derivation()
        d.rule = r
        d.left = left
        d.right = right
        b.addDerivation(d)
