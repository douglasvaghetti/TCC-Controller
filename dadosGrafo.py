##################################################
########### TESTE 1 - MEGA SIMPLES ###############
##################################################

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

##################################################
########### TESTE 2 - 1 PTT VARIOS AS ############
##################################################

grafo = {}

grafo["PTT1"] = ["TP2", "ISP4", "CP1", "ISP3", "TP1"]
grafo["ISP1"] = ["TP1"]
grafo["ISP2"] = ["TP1"]
grafo["ISP3"] = ["PTT1"]
grafo["ISP4"] = ["PTT1"]
grafo["ISP5"] = ["TP2"]
grafo["CP1"] = ["PTT1"]
grafo["CP2"] = ["TP2"]
grafo["TP1"] = ["ISP1", "ISP2", "PTT1"]
grafo["TP2"] = ["CP2", "ISP5", "PTT1"]

defs = {}
defs["PTT1"] = (1, True)
defs["ISP1"] = (1, 10, 0)
defs["ISP2"] = (2, 10, 5)
defs["ISP3"] = (3, 10, 3)
defs["ISP4"] = (4, 10, 0)
defs["ISP5"] = (5, 10, 7)
defs["CP1"] = (101, 5, 0)
defs["CP2"] = (102, 5, 2)
defs["TP1"] = (201, )
defs["TP2"] = (202, )
