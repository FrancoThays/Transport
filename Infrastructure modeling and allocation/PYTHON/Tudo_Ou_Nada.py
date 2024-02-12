'''
Classe para processar alocação por tudo ou nada
Thays
2022-04-26
'''

#====================================================
#IMPORTS
import psycopg2
from ParOD import ParOD
from Centroide import Centroide
import time
from multiprocessing.pool import ThreadPool

#====================================================
#DADOS
user = "thays"
password = "thay"
host = "localhost"
database = "tarefa_04"

#--------------------------------
connection_string = "dbname='%s' user='%s' host='%s' password='%s'" %(database, user, host, password)

#====================================================
#PROCEDIMENTO

class TudoNada:

    def __init__(self):

        inicio = time.time()

        print("Iniciando o processamento")

        #Estabelecimento da conexão
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("UPDATE edges SET volume=0")

        centroides = {}
        cur.execute("SELECT zona FROM centroides ORDER BY zona")
        zonas = [item[0] for item in cur.fetchall()]
        for zona in zonas:
            centroides[zona] = Centroide(zona)

        cur.execute("SELECT origem, destino, demanda FROM dados_od ")
        dados_demanda = cur.fetchall()

        #dados_demanda = [[11088, 11089, 1]]

        for item in dados_demanda:

            origem = int( item[0] )
            destino = int( item[1] )
            demanda = int( item[2] )

            if origem != destino and demanda>0:

                parOD = ParOD(centroides[origem], centroides[destino], demanda)

        print("tempo de processamento = %f segundos" % (time.time() - inicio))

if __name__ == "__main__":
    tudoNada = TudoNada()

