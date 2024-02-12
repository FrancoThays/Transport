"""
TAREFA 02 - OBJETIVO 03

THAYS FRANCO

"""

#IMPORTS
import sqlite3 as lite 
import pathlib as pl
import time
import datetime

#DADOS

db_file = pl.Path("..\RESULTADOS\dados.sqlite")
output_file = pl.Path("..\RESULTADOS\objetivo_03.csv")

#PROCEDIMENTO

start_time = time.time()

conn = lite.connect(db_file)
cur = conn.cursor()

output = open(output_file, "w")
output.write("posto;timestamp;vhp;fhp\n")

cur.execute("SELECT MIN(strftime('%Y-%m-%d %H', timestamp)), MAX(strftime('%Y-%m-%d %H', timestamp)) FROM dados")
result = cur.fetchall()
min_ts_string = result[0][0]
max_ts_string = result[0][1]
#print (min_ts_string)
#print (max_ts_string)
ts_inicio = datetime.datetime.strptime(min_ts_string, '%Y-%m-%d %H')
ts_fim = datetime.datetime.strptime(max_ts_string, '%Y-%m-%d %H')
#print(ts_inicio)
#print(ts_fim)

cur.execute("SELECT DISTINCT posto FROM dados ORDER BY posto")
postos = [i[0] for i in cur.fetchall()]
#postos = [1]

for posto in postos:
    
    print("posto = %d" % posto)
    
    ts_ini_corrente = ts_inicio
    ts_fim_corrente = ts_inicio + datetime.timedelta(hours=1)
    
    vhp = 0
    ts_pico = ''
    
    while ts_fim_corrente <= ts_fim + datetime.timedelta(hours=1):
        
        sql_ini = ts_ini_corrente.strftime("%Y-%m-%d %H:%M")
        #print(sql_ini)
        sql_fim = ts_fim_corrente.strftime("%Y-%m-%d %H:%M")
        
        select_string = "SELECT COUNT(*) FROM dados WHERE posto=%d AND timestamp>='%s' AND timestamp<'%s'"%(
        posto, sql_ini, sql_fim)
        #print(select_string)
        cur.execute(select_string)
        
        volume = cur.fetchall()[0][0]
        
        #print("timestamp = %s; volume = %d" % (sql_ini, volume))
        
        if volume > vhp:
            vhp = volume
            ts_pico = sql_ini
            
            v_max_15 = 0
            
            for i in range(4):
                
                ts_15_ini = ts_ini_corrente + datetime.timedelta(minutes=15 * i)
                ts_15_fim = ts_ini_corrente + datetime.timedelta(minutes=15 * (i + 1))
                sql_15_ini = ts_15_ini.strftime("%Y-%m-%d %H:%M")
                sql_15_fim = ts_15_fim.strftime("%Y-%m-%d %H:%M")
                
                select_string = "SELECT COUNT(*) FROM dados WHERE posto=%d AND timestamp>='%s' AND timestamp<'%s'"%(
                posto, sql_ini, sql_15_fim)
                #print(select_string)
                cur.execute(select_string)
                v_15 = cur.fetchall()[0][0]
                
                if v_15 > v_max_15:
                    v_max_15 = v_15
                    
            fhp = vhp / (4 * v_max_15)
            
        ts_ini_corrente = ts_ini_corrente + datetime.timedelta(minutes=1)
        ts_fim_corrente = ts_fim_corrente + datetime.timedelta(minutes=1)
        
    output.write("%02d;%s;%s;%0.3f\n" % (posto, ts_pico, vhp, fhp))
    
output.close()
cur.close()
conn.close()

result_02 = open("..\RESULTADOS\Objetivo_02.csv", "r")
result_03 = open( output_file, "r")

conta = 0 
for line_02 in result_02.readlines():

    line_03 = result_03.readline()

    #print("line_02 = %s" %line_02)
    #print("line_03 = %s" % line_03)    
    
    if conta > 0:
        
        posto = line_02.split( ";" )[0]
        
        volume_02 = int( line_02.split(";") [2] )
        volume_03 = int( line_03.split(";") [2] )
        
        diferenca = (volume_03 - volume_02) / volume_02 * 100
        
        print (f"Posto {posto}: diferença = {diferenca} %.")
        
    conta += 1
    
    
    

print ("Tempo de execução = %f segundos." % (time.time() - start_time))
        