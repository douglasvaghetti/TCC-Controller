##################################################
########### TESTE 3 - 3 PTTs MUITO LOUCO #########
##################################################

grafo = {}
grafo["PTT1"] = ["ISP1","TP1"]
grafo["PTT2"] = ["ISP2","ISP3","TP1","TP2"]
grafo["PTT3"] = ["ISP5","TP2"]
grafo["ISP1"] = ["PTT1"]
grafo["ISP2"] = ["PTT2"]
grafo["ISP3"] = ["PTT2"]
grafo["ISP4"] = ["TP2"]
grafo["ISP5"] = ["PTT3"]
grafo["TP1"] = ["CP1","PTT1","PTT2"]
grafo["TP2"] = ["PTT3","ISP4","PTT2"]
grafo["CP1"] = ["TP1"]


defs = {}
defs["PTT1"] = (1,True)
defs["PTT2"] = (2,True) 
defs["PTT3"] = (3,True)
defs["ISP1"] = (1,5,3)
defs["ISP2"] = (2,5,0)
defs["ISP3"] = (3,5,3)
defs["ISP4"] = (4,5,3)
defs["ISP5"] = (5,10,6)
defs["TP1"] = (201,)
defs["TP2"] = (202,)
defs["CP1"] = (101,5,2)

