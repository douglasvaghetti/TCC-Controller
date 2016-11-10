##################################################
########### EXEMPLO - MEGA SIMPLES ###############
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
########### TESTE 1 - 1 PTT VARIOS AS ############
##################################################

# grafo = {}

# grafo["PTT1"] = ["TP2", "ISP4", "CP1", "ISP3", "TP1"]
# grafo["ISP1"] = ["TP1"]
# grafo["ISP2"] = ["TP1"]
# grafo["ISP3"] = ["PTT1"]
# grafo["ISP4"] = ["PTT1"]
# grafo["ISP5"] = ["TP2"]
# grafo["CP1"] = ["PTT1"]
# grafo["CP2"] = ["TP2"]
# grafo["TP1"] = ["ISP1", "ISP2", "PTT1"]
# grafo["TP2"] = ["CP2", "ISP5", "PTT1"]

# defs = {}
# defs["PTT1"] = (1, True)
# defs["ISP1"] = (1, 5, 0)
# defs["ISP2"] = (2, 5, 3)
# defs["ISP3"] = (3, 5, 3)
# defs["ISP4"] = (4, 5, 0)
# defs["ISP5"] = (5, 5, 3)
# defs["CP1"] = (101, 5, 0)
# defs["CP2"] = (102, 5, 2)
# defs["TP1"] = (201, )
# defs["TP2"] = (202, )


##################################################
########### TESTE 2 - 2 PTTs VITIMA NO MEIO ######
##################################################

# grafo = {}
# grafo["PTT1"] = ["ISP1","ISP2","TP1"]
# grafo["PTT2"] = ["ISP3","ISP4","TP1"]
# grafo["ISP1"] = ["PTT1"]
# grafo["ISP2"] = ["PTT1"]
# grafo["ISP3"] = ["PTT2"]
# grafo["ISP4"] = ["PTT2"]
# grafo["TP1"] = ["PTT1","PTT2","CP1"]
# grafo["CP1"] = ["TP1"]


# defs = {}
# defs["PTT1"] = (1,True)
# defs["PTT2"] = (2,True)
# defs["ISP1"] = (1,5, 0)
# defs["ISP2"] = (2,5, 3)
# defs["ISP3"] = (3,5, 3)
# defs["ISP4"] = (4,5, 3)
# defs["TP1"] = (201,)
# defs["CP1"] = (101,5,2)


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