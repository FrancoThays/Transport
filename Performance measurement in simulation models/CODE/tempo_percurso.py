'''
Script para automatizar o monitoramento do tempo de percurso do VISUM
Thays Franco
2022-05-12
'''
#=====================================================
#IMPORTS
import win32com.client as com
import numpy as np
import matplotlib.pyplot as plt

#=====================================================

arquivo_visum = r"C:\TRANS\ATIVIDADES\T05\DATA\modelo_visum.ver"
id_zona_origem = 11151
id_zona_destino = 11124


tca = 0.10 #10% ao ano
horizonte = 30 #anos
arquivo_grafico = r"..\RESULT\grafico.png"


#=====================================================

assignments = ["Equilibrium", "Incremental"]
for assignment in assignments:

    Visum = com.Dispatch("Visum.Visum") #Abrindo o Visum
    Visum.LoadVersion(arquivo_visum)

    ZonaOrigem = Visum.Net.Zones.ItemByKey(id_zona_origem)
    ZonaDestino = Visum.Net.Zones.ItemByKey(id_zona_destino)

    Proc = Visum.Procedures
    Proc.Operations.ItemByKey(1).PrTAssignmentParameters.SetAttValue("PrTAssignmentVariant", assignment)
    dSeg = Visum.Net.DemandSegments.ItemByKey('C')

    p_list = Visum.Lists.CreatePrTPathLinkList
    p_list.AddColumn("Link\TCur_PrTSys(CAR)", 2, 3)
    p_list.SetObjects(ZonaOrigem, dSeg, 1 )

    NetElementContainer = Visum.CreateNetElements()
    NetElementContainer.Add(ZonaOrigem)
    NetElementContainer.Add(ZonaDestino)


    FlowBundle = dSeg.FlowBundle

    demanda_atual = np.asarray(dSeg.ODMatrix.GetValues())
    #print(demanta_atual)

    anos = []
    tempos = []

    for ano in range(horizonte):

        demanda_futura = demanda_atual * (1 + tca) ** ano

        dSeg.ODMatrix.SetValues(demanda_futura)

        Proc.Execute()
        FlowBundle.Clear
        FlowBundle.Execute(NetElementContainer)

        #verificar se é vazia, se for, verificar qual i[0] é menor e somar

        valores = p_list.SaveToArray()
        #print(valores)

        x = []
        y = []
        z = []
        soma = 0

        for i in valores:

            if i[0] == "":
                x.append(i[0])
            elif len(x) < 2:
                y.append(i[0])
            elif len(x) < 3:
                z.append(i[0])

        soma = min([s for s in [sum(y), sum(z)] if s!=0.0])

        print("soma = %f" % soma)

        anos.append(ano)
        tempos.append(soma)

    plt.plot(anos, tempos, label= assignment )

plt.title("Tempo de percurso Ingleses x João Paulo - Florianópolis - SC\n")
plt.xlabel("Anos")
plt.ylabel("Tempo de percurso (minutos)")
plt.grid()
plt.legend()
plt.savefig(arquivo_grafico)


#Fechando Visum
Visum = None