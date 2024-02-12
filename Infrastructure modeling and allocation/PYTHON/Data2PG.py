'''
Procedimento para inserir os dados no banco de dados
Thays
2022-04-19
'''

#=======================================================
#IMPORTS
import psycopg2
import pandas as pd
import pathlib as pl
from sqlalchemy import create_engine
import os

#=======================================================
#DADOS
user = "thays"
password = "thay"
host = "localhost"
database = "tarefa_04"

metodo_import_shape = "shp2pgsql" #valores: ogr2ogr ou shp2pgsql

matriz_file = pl.Path("../DADOS/matriz_OD_07h.csv")
edges_file = pl.Path("../DADOS/edges_filtrado/edges.shp")
centroids_file = pl.Path("../DADOS/centroides/centroides.shp")

#--------------------------------
connection_string = "dbname='%s' user='%s' host='%s' password='%s'" %(database, user, host, password)
engine = create_engine('postgresql://%s:%s@%s:5432/%s' %(user, password, host, database))

#=======================================================
#FUNÇÕES

def run(comando):
    print(comando)
    os.system(comando)

#=======================================================
#PROCEDIMENTO

# Estabelecimento da conexão
conn = psycopg2.connect(connection_string)
conn.autocommit = True
cur = conn.cursor()

# Limpando o banco
cur.execute("DROP TABLE IF EXISTS dados_od")
cur.execute("DROP TABLE IF EXISTS edges")
cur.execute("DROP TABLE IF EXISTS edges_vertices_pgr")
cur.execute("DROP TABLE IF EXISTS centroides")
cur.execute("COMMIT")

#Processando os dados de quantitativo de demanda
df_od = pd.read_csv(matriz_file)
df_od.set_index('origem', inplace=True)
df_od_colunas = df_od.stack().reset_index().rename( columns={ 'level_0':'origem', 'level_1':'destino', 0:'demanda'})
#print(df_od_colunas)
df_od_colunas.to_sql('dados_od', engine, index=False)

#Processando os dados de infraestrutura
if metodo_import_shape == "ogr2ogr":
    import_shape_string = "ogr2ogr -f  \"PostgreSQL\" PG:\"%s\" -lco GEOMETRY_NAME=geom %s" %(connection_string, edges_file)
elif metodo_import_shape == "shp2pgsql":
    import_shape_string = "shp2pgsql -S %s edges | psql -q -U %s -d %s" %(edges_file, user, database)
else:
    print("metodo_import_shape desconhecido")
    sys.exit(0)
cur.execute("COMMIT")

run(import_shape_string)
cur.execute("ALTER TABLE edges ADD COLUMN volume integer")
cur.execute("ALTER TABLE edges ADD COLUMN cost real")
cur.execute("ALTER TABLE edges ADD COLUMN reverse_cost real")
cur.execute("ALTER TABLE edges ADD COLUMN source integer")
cur.execute("ALTER TABLE edges ADD COLUMN target integer")
cur.execute("ALTER TABLE edges ADD COLUMN velocidade integer")
if metodo_import_shape == "ogr2ogr":
    cur.execute("ALTER TABLE edges RENAME COLUMN ogc_fid TO gid")
cur.execute("CREATE INDEX edges_source_idx ON edges (source)")
cur.execute("CREATE INDEX edges_target_idx ON edges (target)")
cur.execute("UPDATE edges SET velocidade = 30")
cur.execute("UPDATE edges SET velocidade = 100 WHERE highway = 'trunk'")
cur.execute("UPDATE edges SET velocidade = 80 WHERE highway = 'trunk_link'")
cur.execute("UPDATE edges SET velocidade = 80 WHERE highway = 'primary'")
cur.execute("UPDATE edges SET velocidade = 60 WHERE highway = 'primary_link'")
cur.execute("UPDATE edges SET velocidade = 70 WHERE highway = 'secondary'")
cur.execute("UPDATE edges SET velocidade = 50 WHERE highway = 'secondary_link'")
cur.execute("UPDATE edges SET velocidade = 60 WHERE highway = 'tertiary'")
cur.execute("UPDATE edges SET velocidade = 50 WHERE highway = 'tertiary_link'")
cur.execute("UPDATE edges SET velocidade = 40 WHERE highway = 'residential'")
cur.execute("UPDATE edges SET cost = 60 * (ST_Length(geom) / (1000 * velocidade ))")
cur.execute("UPDATE edges SET reverse_cost = 60 * (ST_Length(geom) / (1000 * velocidade))")
cur.execute("UPDATE edges SET reverse_cost = -1 WHERE oneway = 'yes'")
cur.execute("ALTER TABLE edges ADD COLUMN id integer")
cur.execute("UPDATE edges SET id=gid")
cur.execute("CREATE INDEX edges_idx ON edges (id)")
print("criando o grafo...")
cur.execute("SELECT pgr_createTopology('edges', 0.01, 'geom', 'gid')")
print(cur.fetchall())


#Processando os dados dos centroides
if metodo_import_shape == "ogr2ogr":
    import_shape_string = "ogr2ogr -f  \"PostgreSQL\" PG:\"%s\" -lco GEOMETRY_NAME=geom %s" %(connection_string, centroids_file)
elif metodo_import_shape == "shp2pgsql":
    import_shape_string = "shp2pgsql -S %s centroides | psql -q -U %s -d %s" %(centroids_file, user, database)
else:
    print("metodo_import_shape desconhecido")
    sys.exit(0)
run(import_shape_string)
cur.execute("ALTER TABLE centroides DROP COLUMN gid")
if metodo_import_shape == "ogr2ogr":
    cur.execute("ALTER TABLE centroides RENAME COLUMN ogc_fic TO gid")

cur.execute("ALTER TABLE centroides ADD COLUMN id_vertice integer")
cur.execute("CREATE INDEX centroides_idx ON centroides (zona)")

cur.execute("SELECT zona FROM centroides ORDER BY zona")
zonas = [item[0] for item in cur.fetchall()]

for zona in zonas:
    cur.execute("SELECT id, ST_Distance ( ( SELECT geom FROM centroides WHERE zona=%d), the_geom) AS dist FROM edges_vertices_pgr ORDER BY dist LIMIT 1" %zona)
    vertice = cur.fetchall()[0][0]
    cur.execute("UPDATE centroides SET id_vertice=%d WHERE zona=%d" % (vertice, zona))

def set_mais_longo(self, caminho) -> None:

    # Limpa o banco
    cur.execute("DROP TABLE IF EXISTS mais_longo")
    cur.execute("COMMIT")

    # Objetivo 6
    sql_q = "CREATE TABLE mais_longo AS "
    sql_q += f"SELECT * FROM edges WHERE id IN ({','.join(caminho)})"
    self.cur.execute(sql_q)
