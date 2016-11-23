##################################################
########### TESTE 1 - 1 PTT VARIOS AS ############
##################################################

grafo = {}

grafo["PTT1"] = ["TP2", "ISP4", "CP2", "ISP3", "TP1"]
grafo["ISP1"] = ["TP1"]
grafo["ISP2"] = ["TP1"]
grafo["ISP3"] = ["PTT1"]
grafo["ISP4"] = ["PTT1"]
grafo["ISP5"] = ["TP2"]
grafo["CP2"] = ["PTT1"] 
grafo["CP1"] = ["TP2"]  
grafo["TP1"] = ["ISP1", "ISP2", "PTT1"]
grafo["TP2"] = ["CP1", "ISP5", "PTT1"]

defs = {}
defs["PTT1"] = (1, True)
defs["ISP1"] = (1, 6, 0)
defs["ISP2"] = (2, 6, 3) 
defs["ISP3"] = (3, 6, 3)
defs["ISP4"] = (4, 6, 0)
defs["ISP5"] = (5, 6, 3)
defs["CP2"] = (101, 5, 0)
defs["CP1"] = (102, 5, 2)
defs["TP1"] = (201, )
defs["TP2"] = (202, )
