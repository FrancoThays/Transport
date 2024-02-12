"""
TAREFA 02 - OBJETIVO 05

THAYS FRANCO

"""

#IMPORTS
import sqlite3 as lite 
import pathlib as pl
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

#DADOS

db_file = pl.Path("..\RESULTADOS\dados.sqlite")
output_file = pl.Path("..\RESULTADOS\grafico.png")

#PROCEDIMENTO

start_time = time.time()

conn = lite.connect(db_file)
cur = conn.cursor()

cur.execute("SELECT MIN(strftime('%Y-%m-%d %H', timestamp)), MAX(strftime('%Y-%m-%d %H', timestamp)) FROM dados")
result = cur.fetchall()
min_ts_string = result[0][0]
max_ts_string = result[0][1]
#print(min_ts_string)
#print(max_ts_string)
ts_inicio = datetime.datetime.strptime(min_ts_string, '%Y-%m-%d %H')
ts_fim = datetime.datetime.strptime(max_ts_string, '%Y-%m-%d %H')
print(ts_inicio)
print(ts_fim)

cur.execute("SELECT DISTINCT posto FROM dados ORDER BY posto")

postos = [i[0] for i in cur.fetchall()]
#postos = [1]

fig,ax = plt.subplots()
fig.autofmt_xdate()
ax.xaxis.set_major_formatter(DateFormatter("%m-%d %H"))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))

for posto in postos:
    
    print("posto = %d" % posto)
    
    time_sticks = []
    volume_data = []
    
    ts_ini_corrente = ts_inicio
    ts_fim_corrente = ts_inicio + datetime.timedelta(hours=1)
    
    while ts_fim_corrente <= ts_fim + datetime.timedelta(hours=1):
        
        sql_ini = ts_ini_corrente.strftime("%Y-%m-%d %H:%M")
        #print(sql_ini)
        sql_fim = ts_fim_corrente.strftime("%Y-%m-%d %H:%M")
        
        time_sticks.append(ts_ini_corrente)
        
        select_string = "SELECT COUNT(*) FROM dados WHERE posto=%d AND timestamp>='%s' AND timestamp<'%s'"%(
        posto, sql_ini, sql_fim)
        cur.execute(select_string)
        
        volume = cur.fetchall()[0][0]
        
        volume_data.append(volume)
        #print("timestamp = %s; volume = %d" % (sql_ini, volume))
        
        
        ts_ini_corrente = ts_ini_corrente + datetime.timedelta(minutes=60)
        ts_fim_corrente = ts_fim_corrente + datetime.timedelta(minutes=60)
        
    plt.plot(time_sticks, volume_data, label='%02d' % posto)
    
cur.close()
conn.close()

plt.title('variação horária')
plt.xlabel('Horas do dia')
plt.ylabel('volume horário (veh/h)')
ax.set_xlim([ts_inicio, ts_fim])

plt.grid()

plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
plt.savefig(output_file, dpi=300 , bbox_inches ='tight')

plt.close()

print("Tempo de execução = %f segundos." % (time.time() - start_time))
        
        
    
    
    