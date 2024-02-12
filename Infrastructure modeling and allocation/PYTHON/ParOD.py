'''
Classe para organizar as funcionalidades de um par OD
Thays
2022-04-26
'''


#====================================================
#IMPORTS
import psycopg2

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

    def __init__(self, origem, destino, demanda):

        #Estabelecimento da conexão
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cur = conn.cursor()

        print("Processando Par OD: %d, %d" % (origem.get_zona(), destino.get_zona()))


        cur.execute("SELECT * FROM pgr_dijkstra('SELECT id, source, target, cost, reverse_cost FROM edges', %d, %d, False)" %(origem.get_vertice(), destino.get_vertice()))

        result = cur.fetchall()
        print(*result, sep="\n")


        caminho = [str(item[3]) for item in result]
        if len(caminho) != 0:
            update_string = "UPDATE edges SET volume=volume+1 WHERE id IN (%s)" % ",".join(caminho)
            #print(update_string)
            cur.execute(update_string)