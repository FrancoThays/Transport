# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 16:24:07 2022
TAREFA 02 OBJETIVO 01

@author: thays
"""
#IMPORTS

import glob
import sqlite3 as lite
import pathlib as pl
import time


#DADOS

#input_dir = "C:\Users\thays\OneDrive\Desktop\AULA\00. PROG. COMP. APL. TRANSPORTES\ATIVIDADES\TAREFA 02\DADOS\dados_0112" #forma absoluta
input_dir = pl.Path("..\DADOS\dados_0112") #forma relativa
db_file = pl.Path ("..\RESULTADOS\dados.sqlite")

#PROCEDIMENTO

start_time = time.time()

conn = lite.connect (db_file)
cur = conn.cursor()

#Criando a conexão com o banco de dados
cur.execute ("DROP TABLE IF EXISTS dados")
cur.execute ("CREATE TABLE dados (posto integer, faixa integer, timestamp text, velocidade real, comprimento real)")

#Carregando os dados
file_names = glob.glob ("%s/*.txt" %input_dir)

for file_name in file_names:

    print (file_name)

    posto = int(file_name.split('.')[-2].split('_')[-1])

    for line in open (file_name, "r").readlines() [1:]:

        line = line.replace("\n","")
        partes = line.split(";")
        faixa = int(partes[0])
        timestamp = partes[2]
        velocidade = float (partes[3])
        comprimento = float(partes[4])

        insert_string = "INSERT INTO dados (posto, faixa, timestamp, velocidade, comprimento) VALUES (%d, %d, '%s', %f, %f)" % (posto, faixa, timestamp, velocidade, comprimento)
        #print (insert_string)
        cur.execute(insert_string)

cur.execute ("ALTER TABLE dados ADD COLUMN classe text")
cur.execute ("UPDATE dados SET classe = 'moto' WHERE comprimento < 3")
cur.execute ("UPDATE dados SET classe = 'carro' WHERE comprimento >= 3 AND comprimento < 7")
cur.execute ("UPDATE dados SET classe = 'cam_leve' WHERE comprimento >= 7 AND comprimento < 15")
cur.execute ("UPDATE dados SET classe = 'cam_pesado' WHERE comprimento >= 15 AND comprimento < 20")
cur.execute ("UPDATE dados SET classe = 'especial' WHERE comprimento >= 20")

cur.execute ("COMMIT")
cur.execute ("CREATE INDEX dados_idx ON dados(posto,timestamp)")

cur.close()
conn.close()

print( "Tempo de execução = %f segundos." % (time.time() - start_time))



