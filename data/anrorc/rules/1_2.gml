rule [
  ruleID "TEST"
  left [
    edge [ source 1 target 0 label "=" ]
    edge [ source 5 target 4 label "=" ]
    edge [ source 4 target 3 label "-" ]
    edge [ source 3 target 2 label "=" ]
    edge [ source 2 target 1 label "-" ]
    edge [ source 0 target 5 label "-" ]
    edge [ source 7 target 4 label "-" ]
    edge [ source 9 target 8 label "-" ]
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
    node [ id 7 label "Br" ]
    node [ id 10 label "H" ]
    node [ id 9 label "H" ]
    edge [ source 6 target 2 label "-" ]
    edge [ source 10 target 8 label "-" ]
  ]
  right [
    edge [ source 1 target 0 label "-" ]
    edge [ source 5 target 4 label "-" ]
    edge [ source 4 target 3 label "=" ]
    edge [ source 3 target 2 label "-" ]
    edge [ source 2 target 1 label "=" ]
    edge [ source 0 target 5 label "=" ]
    edge [ source 4 target 8 label "-" ]
  ]
]