"""
TAREFA 02 - OBJETIVO 04

THAYS FRANCO

"""

#IMPORTS
import sqlite3 as lite 
import pathlib as pl
import time

#DADOS

db_file = pl.Path("..\Resultados\dados.sqlite")
output_file = pl.Path("..\Resultados\objetivo_04.csv")

classes = ["moto", "carro", "cam_leve", "cam_pesado", "especial"]

#PROCEDIMENTO

start_time = time.time()

conn = lite.connect(db_file)
cur = conn.cursor()

output = open(output_file,"w")
output.write("posto;%s\n" % ";".join(classes))

cur.execute("SELECT DISTINCT posto FROM dados")
postos = [i[0] for i in cur.fetchall()]

for posto in postos:
    output.write("%02d" %posto)
    for classe in classes:
        cur.execute("SELECT COUNT(*) FROM dados WHERE posto=%d AND classe='%s'" % (posto, classe))
        volume = cur.fetchall ()[0][0]
        output.write(";%d" % volume)
    output.write("\n")
    
    
output.close()
cur.close()
conn.close()

    
print ("Tempo de execução = %f segundos." % (time.time() - start_time))    
    
