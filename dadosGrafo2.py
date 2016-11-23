##################################################
########### TESTE 2 - 2 PTTs VITIMA NO MEIO ######
##################################################

grafo = {}
grafo["PTT1"] = ["ISP1","ISP2","TP1"]
grafo["PTT2"] = ["ISP3","ISP4","TP1"]
grafo["ISP1"] = ["PTT1"]
grafo["ISP2"] = ["PTT1"]
grafo["ISP3"] = ["PTT2"]
grafo["ISP4"] = ["PTT2"]
grafo["TP1"] = ["PTT1","PTT2","CP1"]
grafo["CP1"] = ["TP1"]

defs = {}
defs["PTT1"] = (1,True)
defs["PTT2"] = (2,True)
defs["ISP1"] = (1,15, 0)
defs["ISP2"] = (2,15, 8)
defs["ISP3"] = (3,15, 8)
defs["ISP4"] = (4,15, 8)
defs["TP1"] = (201,)
defs["CP1"] = (101,15,4)

