"""
TAREFA 01 - OBJETIVO 02
AUTORA: THAYS FRANCO

OBJETIVO 2: Ajustar procedimento do obj1 para um determinado horizonte de projeto.

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
Terreno = "plano"
SAF= 1.0 #Ajuste de velocidade
CAF = 1.0 #Ajuste de capacidade
a = 1.31 #Parâmetro de calibração exponencial 
BP = 1.400 #breakpoint em pc/h/ln
Dc = 45 #Capacidade de densidade em pc/mi/ln
n = 10 #anos
ano_base = 2019
tca = 0.03 #taxa de crescimento anual


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

resultados = []

for i in range (n):
    ano = ano_base + i
    print ("----------\nano = %d" %ano)
    
    vfut = Vp * (1 + tca) ** i

    if vfut > C:
        print ("Volume (%d pc/h/ln) excedeu a capacidade (%d pc/h/ln)" % (vfut,C))
        sys.exit(0)
    else:   
        print("Volume em condições básicas = {} pc/h/ln. \nRelação Vp/c = {:0.2f}" .format(round(vfut),vfut/C))
    
    #PASSO 5: ESTIMAR A VELOCIDADE E A DENSIDADE
    
    if vfut <= BP:
        S = FFSadj
    else:
        S = FFSadj - ((FFSadj - Cadj / Dc) * (vfut - BP) ** a) / (Cadj - BP) ** a 
        
    D = vfut / S
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
    
    LOS = pega_los (D)
    
    print ("O nível de serviço é \"%c\"!" %LOS)
    
    resultados.append( [ano, LOS])
   
print (*resultados, sep='\n')