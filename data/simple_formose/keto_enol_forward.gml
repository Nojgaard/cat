rule [
    ruleID "Keto-enol isomerization ->"
    left [
        edge [ source 0 target 3 label "-" ]
        edge [ source 0 target 1 label "-" ]
        edge [ source 1 target 2 label "=" ]
    ]
    context [
        node [ id 0 label "C" ]
        node [ id 1 label "C" ]
        node [ id 2 label "O" ]
        node [ id 3 label "H" ]
    ]
    right [
        edge [ source 2 target 3 label "-" ]
        edge [ source 2 target 1 label "-" ]
        edge [ source 1 target 0 label "=" ]
    ]
    constrainAdj [
        id 1
        op "="
        count 1
        nodeLabels [
            label "O"
        ]
    ]
]
