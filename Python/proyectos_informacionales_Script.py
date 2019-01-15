import pandas as pd
import sqlalchemy
import sys
from pandas import ExcelWriter
import configparser
import os.path as path
from datetime import datetime

if path.exists("Proyectos Informacionales.xlsx"):
	datos = pd.read_excel("Proyectos Informacionales.xlsx").fillna(" ")
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
	#engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

	exist = False
	existe = engine.execute("show tables like 'proyectos_infomacionales'");
	for row in existe:
		conn = engine.connect()
		res = conn.execute('select * from proyectos_informacionales')
		df = pd.DataFrame(res.fetchall())
		conn.close()
		exist = True

	if not exist or len(df) == 0: #Creo la tabla la primera vez
		df = datos
		engine.execute("truncate proyectos_informacionales;")
		df.to_sql("proyectos_informacionales", engine, if_exists = "append", index = False)
	else:
		engine.execute("truncate proyectos_informacionales;")
		datos.to_sql("proyectos_informacionales", engine, if_exists = "append", index = False)

	conn1 = engine.connect()
	res1 = conn1.execute('select * from proyectos_informacionales')
	acumulado = pd.DataFrame(res1.fetchall())
	conn1.close()
		
	columnas = list(acumulado.columns)
	for k in range(len(columnas)):
		acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
	if usuario=='SERVIDOR':		
		writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/proyectos_informacionales_acumulado.xlsx', engine='xlsxwriter')		
		acumulado.to_excel(writer, index=False)
		writer.save()

else:
	print("El archivo que intenta consultar no existe o no existe en este directorio")