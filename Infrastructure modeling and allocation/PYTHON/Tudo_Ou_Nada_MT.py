'''
Classe para processar alocação por tudo ou nada
Thays
2022-04-26
'''

#====================================================
#IMPORTS
import psycopg2
from ParOD_MT import ParOD
from Centroide import Centroide
from Data2PG import set_mais_longo
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

        dados_demanda = []
        cur.execute("SELECT origem, destino, demanda FROM dados_od WHERE origem::integer!=destino::integer AND demanda>0")
        result = cur.fetchall()
        for item in result:
            dados_demanda.append([centroides[int(item[0])], centroides[int(item[1])], item[2]])

        #dados_demanda = [[11088, 11089, 1]]

        # Cálculo do maior caminho
        self.maior_custo = 0
        self.mais_longo = None

        pool = ThreadPool(3)
        results = pool.map(ParOD, dados_demanda)

    def dist (self, pares) -> None:

           for par in pares:
               if par.custo > self.maior_custo:
                    self.maior_custo = par.custo
                    self.mais_longo = par.caminho

               self.dist(pares)




if __name__ == "__main__":
    tudoNada = TudoNada()