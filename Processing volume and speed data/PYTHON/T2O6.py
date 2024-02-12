"""
TAREFA 02 - OBJETIVO 06  

THAYS FRANCO

"""

#IMPORTS
import sqlite3 as lite 
import pathlib as pl
import time

#DADOS

db_file = pl.Path("..\RESULTADOS\dados.sqlite")
output_file = pl.Path("..\RESULTADOS\objetivo_06.csv")

classes = ["moto", "carro", "cam_leve", "cam_pesado", "especial"]

#PROCEDIMENTO

start_time = time.time()

conn = lite.connect(db_file)
cur = conn.cursor()

output = open(output_file, "w")
output.write("posto; porcentagem\n")

#Utilizando o número do posto como range:
cur.execute("SELECT DISTINCT posto FROM dados ORDER BY posto")
postos = [i[0] for i in cur.fetchall()]

pa = 0 #variável para contagem de veículo de passeio
pe = 0 #variável para contagem de veículo pesado


for posto in postos:
    
    
    if posto == 5: #o posto 5 tem um horário de pico diferente
        ts_min = '2016-08-10 06:00:00'
        ts_max = '2016-08-10 07:00:00'
    else: #os demais postos tem o mesmo horário de pico
        ts_min = '2016-08-10 05:00:00'
        ts_max = '2016-08-10 06:00:00'
        
    
    for classe in classes: #para as classificações de veículos
        
        #Abaixo há a contagem de veículos baseado nas classes, já dentro dos limites de horário de pico considerando a numeração do posto da iteração:
       
        cur.execute("SELECT COUNT(*) FROM dados WHERE posto=%d AND classe='%s' AND timestamp BETWEEN '%s' AND '%s'" % (posto, classe, ts_min, ts_max))
        
        #A seguir dependendo da classe do veículo multiplicará o volume pelo coeficiente e acrescenta o valor no acumulador
        if classe == classes[0]:      
            volume = cur.fetchall ()[0][0] * 0.5 
            pa = pa + volume 
        
        elif classe == classes[1]:
            volume = cur.fetchall ()[0][0] 
            pa = pa + volume 
            
        elif classe == classes[2]:  
            volume = cur.fetchall ()[0][0] * 0.7
            pe = pe + volume 
        
        elif classe == classes[3]:
            volume = cur.fetchall ()[0][0] 
            pe = pe + volume 
            
        else:
            volume = cur.fetchall ()[0][0] * 1.5
            pe = pe + volume
            
    porcentagem = (pe/(pe + pa))*100  #calculo de porcentagem por posto baseado nos acumuladores
     
    output.write("%d;%.2f\n" %(posto,porcentagem))       
                   
   
output.close()
cur.close()
conn.close()