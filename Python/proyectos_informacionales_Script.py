import pandas as pd
import pymysql
import sqlalchemy
import sys
from pandas import ExcelWriter
import configparser

datos = pd.read_excel("Proyectos Informacionales.xlsx").fillna(" ")
datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(","").replace(")","")
.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos.columns))


config = configparser.ConfigParser()
config.read("configuracion.ini")
	
usuario = input(u"Introducir usario de conexion con el servidor: ")

usuario = usuario.upper()
password = config[usuario]["password"]
user = config[usuario]["user"]
host = config[usuario]["host"]
dataBase = config[usuario]["dataBase"]

print(password)

engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+dataBase)
#engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

datos.to_sql("proyectos_informacionales", engine, if_exists = "append", index = False)

conn = engine.connect()
res = conn.execute('select * from proyectos_informacionales')
df = pd.DataFrame(res.fetchall())
conn.close()
	
columnas = list(df.columns)
for k in range(len(columnas)):
	df = df.rename(columns={columnas[k]:str(datos.columns[k])})
	
df2 = df.drop_duplicates(df.columns[~df.columns.isin(['project'])],keep='last')
df2.to_sql("proyectos_informacionales", engine, if_exists = "replace", index = False)

conn1 = engine.connect()
res1 = conn1.execute('select * from proyectos_informacionales')
acumulado = pd.DataFrame(res1.fetchall())
conn1.close()
	
columnas = list(acumulado.columns)
for k in range(len(columnas)):
	acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
		
writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/proyectos_informacionales_acumulado.xlsx', engine='xlsxwriter')		
acumulado.to_excel(writer, index=False)
writer.save()