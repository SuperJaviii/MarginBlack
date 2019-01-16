import pandas as pd
import sqlalchemy
import sys
from pandas import ExcelWriter
import configparser
import os.path as path
from datetime import datetime

if path.exists("trimestres.xlsx"):
	datos = pd.read_excel("trimestres.xlsx")
	datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(","").replace(")","")
	.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos.columns))
	datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])

	config = configparser.ConfigParser()
	config.read("configuracion.ini")
		
	usuario = sys.argv[1]

	usuario = usuario.upper()
	password = config[usuario]["password"]
	user = config[usuario]["user"]
	host = config[usuario]["host"]
	dataBase = config[usuario]["dataBase"]

	engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+dataBase)

	exist = False
	existe = engine.execute("show tables like 'trimestres'");
	for row in existe:
		conn = engine.connect()
		res = conn.execute('select * from trimestres')
		df = pd.DataFrame(res.fetchall())
		conn.close()
		exist = True

	if not exist or len(df) == 0: #Creo la tabla la primera vez
		df = datos
		engine.execute("truncate trimestres;")
		df.to_sql("trimestres", engine, if_exists = "append", index = False)
	else:
		engine.execute("truncate trimestres;")
		datos.to_sql("trimestres", engine, if_exists = "append", index = False)
		
	conn1 = engine.connect()
	res1 = conn1.execute('select * from trimestres')
	acumulado = pd.DataFrame(res1.fetchall())
	conn1.close()
		
	columnas = list(acumulado.columns)
	for k in range(len(columnas)):
		acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
	if usuario=='SERVIDOR':		
		writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/trimestres.xlsx', engine='xlsxwriter')		
		acumulado.to_excel(writer, index=False)
		writer.save()

else:
	print("El archivo que intenta consultar no existe o no existe en este directorio")