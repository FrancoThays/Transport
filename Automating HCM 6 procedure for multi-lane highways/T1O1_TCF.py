"""
TAREFA 01 - OBJETIVO 01
AUTORA: THAYS FRANCO
RESULTADO ESPERADO: DETERMINAÇÃO DO NÍVEL DE SERVIÇO EM RODOVIAS DE MÚLTIPLAS FAIXAS DO HCM 6

ESPECIFICAÇÕES:
    OPERAÇÕES IDEAIS NO SEGMENTO;
    FREE FLOW SPEED (FFS) MEDIDA EM CAMPO;
    TERRENOS GERAIS - PLANO OU ONDULADO;
    
MEU OBJETIVO PESSOAL É REALIZAR O CÓDIGO DE MODO QUE UMA VEZ FINALIZADO,
CADA VEZ QUE FOR UTILIZADO, O USUÁRIO NÃO NECESSITE REESCREVER OS PARÂMETROS

"""

#BIBLIOTECA DE VALORES PRÉ-DEFINIDOS - FIXOS

import sys
Et = { "ondulado": 3.0, "plano": 2.0}

#PASSO 1: DADOS DE ENTRADA 

V = 2300 #veh/h
FFS = 65 #mi/h
PHF = 0.95               
Pt = 0.13
Ln = 2
Terreno = "ondulado"
SAF= 1.0 #Ajuste de velocidade
CAF = 1.0 #Ajuste de capacidade
a = 1.31 #Parâmetro de calibração exponencial 
BP = 1.400 #breakpoint em pc/h/ln
Dc = 45 #Capacidade de densidade em pc/mi/ln



#PASSO 2: ESTIMAR E AJUSTAR A FFS

""" 
Para FFS medida diretamente, nenhum ajuste será aplicado;
Desta forma, é necessário apenas o ajuste de velocidade para condições adversas.

"""
FFSadj = FFS * SAF

#PASSO 3: ESTIMAR E AJUSTAR A CAPACIDADE 
    
C = 1900 + 20 * (FFSadj - 45) #Capacidade básica para rodovia de múltiplas faixas estimada
Cadj = C * CAF #Capacidade básica para rodovia de múltiplas faixas ajustada

#VERIFICAÇÕES:

if FFSadj < 45 or FFSadj > 70:
    print("REVISAR VALOR DE VELOCIDADE DE FLUXO LIVRE")
    sys.exit(0)
elif Cadj > 2300:
    print("CAPACIDADE MAIOR DO QUE VALOR MÁXIMO PERMITIDO")
    sys.exit(0)
else:
    print("RESULTADOS: ")
    print( "O valor da capacidade ajustada é %d pc/h/ln" %Cadj)
        
#PASSO 4: AJUSTE DO VOLUME 

#4.1. Verificação do tipo de terreno

if Terreno not in Et.keys():
    print("\nTipo de terreno não conhecido. Terminando a execução")
    sys.exit(0)

#4.2. Fator de ajustamento para veículos pesados

FHV = 1 / (1 + Pt * (Et[Terreno] - 1))

#4.3. Taxa de fluxo de demanda equivalente em pc/h/ln

Vp = V / (PHF * Ln * FHV)

#4.4. Verificação de extrapolação da capacidade

if Vp > C:
    print ("Volume (%d pc/h/ln) excedeu a capacidade (%d pc/h/ln)" % (Vp,C))
    sys.exit(0)
else:   
    print("Volume em condições básicas = {} pc/h/ln. \nRelação Vp/c = {:0.2f}" .format(round(Vp),Vp/C))
    
#PASSO 5: ESTIMAR A VELOCIDADE E A DENSIDADE

if Vp <= BP:
    S = FFSadj
else:
    S = FFSadj - ((FFSadj - Cadj / Dc) * (Vp - BP) ** a) / (Cadj - BP) ** a 
    
D = Vp / S
print ("A densidade é de %0.2f pc/mi/ln" %D)

#PASSO 6: DETERMINAR LOS

def pega_los (densidade):
    if densidade <= 11: 
        return "A"
    elif densidade <= 18: 
        return "B"
    elif densidade <= 26: 
        return "C"
    elif densidade <= 35: 
        return "D"
    elif densidade <= 45: 
        return "E"
    else:
        return "F"
    

print("O nível de serviço é \"%c\"!" %pega_los (D))
    
