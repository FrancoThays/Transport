'''
Classe para organizar as informações dos centroides
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

class Centroide:

    def __init__(self, zona):

        self.zona = zona

        #Estabelecimento da conexão
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT id_vertice FROM centroides WHERE zona=%d" %zona)
        self.id_vertice = cur.fetchall()[0][0]

    def get_zona(self):
        return self.zona

    def get_vertice(self):
        return self.id_vertice
