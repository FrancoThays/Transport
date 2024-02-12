'''
Classe para organizar as funcionalidades de um par OD
Thays
2022-04-26
'''

#====================================================
#IMPORTS
import psycopg2
from math import inf
from pathlib import Path

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

class ParOD:

    def __init__(self, dados):

        origem = dados[0]
        destino = dados[1]
        demanda = dados[2]


        #Estabelecimento da conexão
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cur = conn.cursor()

        print("Processando par OD: %d, %d" % (origem.get_zona(), destino.get_zona()))

        cur.execute("SELECT * FROM pgr_dijkstra ('SELECT id, source, target, cost, reverse_cost FROM edges', %d, %d, False)" % (origem.get_vertice(), destino.get_vertice()))
        result = cur.fetchall()
        #print(*result, sep="\n")

        self.caminho = [str(item[3]) for item in result]

        if len(self.caminho) != 0:
            self.caminho.remove('-1')
            self.custo = float(result[-1][-1])
        else:
            self.custo = inf