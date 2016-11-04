# grafo = {}
# grafo["PTT1"] = ["ISP1","CP1","TP2","TP1"]
# grafo["PTT2"] = ["TP2","ISP4","ISP5","TP3"]


# grafo["ISP1"] = ["PTT1"]
# grafo["ISP2"] = ["TP1"]
# grafo["ISP3"] = ["TP1"]
# grafo["ISP4"] = ["PTT2"]
# grafo["ISP5"] = ["PTT2"]
# grafo["ISP6"] = ["TP3"]

# grafo["TP1"] = ["ISP2","ISP3","CP2","PTT1"]
# grafo["TP2"] = ["PTT1","PTT2"]
# grafo["TP3"] = ["ISP6","CP3","CP4","PTT2"]

# grafo["CP1"] = ["PTT1"]
# grafo["CP2"] = ["TP1"]
# grafo["CP3"] = ["TP3"]
# grafo["CP4"] = ["TP3"]

# defs = {}
# defs["PTT1"] = (1,True) #numero do PTT, implementa bloqueio
# defs["PTT2"] = (2,False)


# defs["ISP1"] = (1,3,2) #prefixo, numero de hosts, numero de agressores
# defs["ISP2"] = (2,4,0)
# defs["ISP3"] = (3,2,1)
# defs["ISP4"] = (4,4,0)
# defs["ISP5"] = (5,4,0)
# defs["ISP6"] = (6,4,0)

# defs["TP1"] = (201,) #prefixo
# defs["TP2"] = (202,)
# defs["TP3"] = (203,)

# defs["CP1"] = (101,1,0) #prefixo, numero de hosts, numero de vitimas
# defs["CP2"] = (102,3,3)
# defs["CP3"] = (103,1,0)
# defs["CP4"] = (104,1,0)

grafo = {}
grafo["PTT1"] = ["ISP1","CP1"]
grafo["CP1"] = ["PTT1"]
grafo["TP1"] = ["PTT2","CP2"]
grafo["PTT2"] = ["TP1","ISP1"]
grafo["ISP1"] = ["PTT1","PTT2"]
grafo["CP2"] = ["TP1"]

defs = {}
defs["PTT1"] = (1,True)
defs["PTT2"] = (2,True)
defs["ISP1"] = (1,10,5)
defs["CP1"] = (101,2,1)
defs["CP2"] = (102,2,0)
defs["TP1"] = (201,)

# grafo = {}

# grafo["PTT1"] = ["CP1","TP1"]
# grafo["ISP1"] = ["TP1"]
# grafo["CP1"] = ["PTT1"]
# grafo["TP1"] = ["ISP1","PTT1"]

# defs = {}
# defs["PTT1"] = (1,False)
# defs["ISP1"] = (1,5,3)
# defs["CP1"] = (101,5,3)
# defs["TP1"] = (201,)