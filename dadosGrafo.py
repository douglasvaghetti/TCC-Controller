# defs = {}
# defs["PTT1"] = 1
# defs["PTT2"] = 2
# defs["AS1"] = (1,2) #prefixo 33, 10 hosts
# defs["AS2"] = (2,2)
# defs["AS3"] = (3,2)
# defs["AS4"] = (4,2)
# defs["AS5"] = (5,2)
# defs["AS6"] = (6,2)
# defs["AS7"] = (7,2)
# defs["AS8"] = (8,2)
# defs["AS9"] =(9,2)

# grafo = {}
# grafo["PTT1"] = ["AS1","AS6","AS2"]
# grafo["PTT2"] = ["AS3","AS7","AS2"]
# grafo["AS1"] = ["PTT1","AS8"]
# grafo["AS2"] = ["PTT1","PTT2","AS9"]
# grafo["AS3"] = ["AS4","AS5","PTT2"]
# grafo["AS4"] = ["AS3"]
# grafo["AS5"] = ["AS3"]
# grafo["AS6"] = ["PTT1"]
# grafo["AS7"] = ["PTT2"]
# grafo["AS8"] = ["AS1"]
# grafo["AS9"] = ["AS2"]

#grafo = {}
#grafo["PTT1"] = ["AS1","AS2"]
#grafo["AS1"] = ["PTT1","AS3"]
#grafo["AS2"] = ["PTT1"]
#grafo["AS3"] = ["AS1"]

#defs = {}
#defs["PTT1"] = 1
#defs["AS1"] = (1,2) #prefixo 33, 10 hosts
#defs["AS2"] = (2,2)
#defs["AS3"] = (3,2)


# grafo = {}
# grafo["PTT1"] = ["ISP1","CP1","TP2","TP1"]
# grafo["PTT2"] = ["TP2","ISP4","ISP5","TP3"]
#
#
# grafo["ISP1"] = ["PTT1"]
# grafo["ISP2"] = ["TP1"]
# grafo["ISP3"] = ["TP1"]
# grafo["ISP4"] = ["PTT2"]
# grafo["ISP5"] = ["PTT2"]
# grafo["ISP6"] = ["TP3"]
#
# grafo["TP1"] = ["ISP2","ISP3","CP2","PTT1"]
# grafo["TP2"] = ["PTT1","PTT2"]
# grafo["TP3"] = ["ISP6","CP3","CP4","PTT2"]
#
# grafo["CP1"] = ["PTT1"]
# grafo["CP2"] = ["TP1"]
# grafo["CP3"] = ["TP3"]
# grafo["CP4"] = ["TP3"]
#
# defs = {}
# defs["PTT1"] = (1,False) #numero do PTT, implementa bloqueio
# defs["PTT2"] = (2,False)
#
#
# defs["ISP1"] = (1,3,2) #prefixo, numero de hosts, numero de agressores
# defs["ISP2"] = (2,4,0)
# defs["ISP3"] = (3,20,0)
# defs["ISP4"] = (4,4,0)
# defs["ISP5"] = (5,4,0)
# defs["ISP6"] = (6,4,0)
#
# defs["TP1"] = (201,) #prefixo
# defs["TP2"] = (202,)
# defs["TP3"] = (203,)
#
# defs["CP1"] = (101,1,0) #prefixo, numero de hosts, numero de vitimas
# defs["CP2"] = (102,1,3)
# defs["CP3"] = (103,1,0)
# defs["CP4"] = (104,1,0)


grafo = {}
grafo["PTT1"] = ["CP1","TP1"]
grafo["ISP1"] = ["TP1"]
grafo["CP1"] = ["PTT1"]
grafo["TP1"] = ["ISP1","PTT1"]

defs = {}
defs["PTT1"] = (1,False)
defs["ISP1"] = (1,1,0)
defs["CP1"] = (101,1,0)
defs["TP1"] = (201,)
