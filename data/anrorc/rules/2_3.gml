rule [
  ruleID "TEST"
  left [
    edge [ source 5 target 4 label "-" ]
    edge [ source 4 target 3 label "=" ]
    edge [ source 15 target 14 label "-" ]
    edge [ source 16 target 14 label "-" ]
  ]
  context [
    node [ id 8 label "N" ]
    node [ id 0 label "C" ]
    node [ id 1 label "N" ]
    node [ id 5 label "N" ]
    node [ id 2 label "C" ]
    node [ id 3 label "C" ]
    node [ id 4 label "C" ]
    node [ id 6 label "Ph" ]
    node [ id 12 label "H" ]
    node [ id 13 label "H" ]
    node [ id 16 label "H" ]
    node [ id 14 label "O" ]
    node [ id 15 label "H" ]
    edge [ source 6 target 2 label "-" ]
    edge [ source 8 target 0 label "=" ]
    edge [ source 3 target 2 label "-" ]
    edge [ source 2 target 1 label "=" ]
    edge [ source 1 target 0 label "-" ]
    edge [ source 5 target 12 label "-" ]
    edge [ source 5 target 13 label "-" ]
    edge [ source 8 target 4 label "-" ]
  ]
  right [
    edge [ source 4 target 3 label "-" ]
    edge [ source 4 target 14 label "=" ]
  ]
]