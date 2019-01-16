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
	datos['auditoria']=pd.Series([])

	datos1 = datos
		
	datos = datos.drop_duplicates(subset = ["project"], keep = 'first')
		
	datos = datos.dropna(subset = ["project"])
	m = datos.merge(datos1, how = "outer", suffixes = ['','_'], indicator = True)
	mer = m.loc[m._merge.eq('right_only')]
	mer = mer.drop("_merge", axis = 1)
		
	if  len(mer) > 0: 
		print("Existen registros rechazados, compruebe el xlsx generado con los rechazados")
	datos = datos.reset_index(drop = True)
	#*****			
	mer.to_excel('rechazados_proyectos.xlsx',index=False)
	#*******
	
	config = configparser.ConfigParser()
	config.read("configuracion.ini")
		
	usuario = sys.argv[1]

	usuario = usuario.upper()
	password = config[usuario]["password"]
	user = config[usuario]["user"]
	host = config[usuario]["host"]
	dataBase = config[usuario]["dataBase"]

	engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+dataBase)

	conn1 = engine.connect()
	res1 = conn1.execute('select * from proyectos_informacionales')
	actualiza = pd.DataFrame(res1.fetchall())
	conn1.close()
	
	columnas = list(actualiza.columns)
	for k in range(len(columnas)):
		actualiza = actualiza.rename(columns={columnas[k]:str(datos.columns[k])})
		
	if len(actualiza) > 0:
		actualiza = actualiza.drop("auditoria", axis = 1)
		actualiza['auditoria']=pd.Series([])	
		n = datos.merge(actualiza, how = "outer", suffixes = ['','_'], indicator = True)
		ner = n.loc[n._merge.eq('left_only')]
		ner = ner.drop("_merge", axis = 1)
		ner.to_sql("proyectos_informacionales", engine, if_exists = "append", index = False)
	
	else:
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
		if path.exists('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_proyectos_informacionales.xlsx'):
				rechazados = pd.read_excel('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_proyectos_informacionales.xlsx')
				mer = pd.concat([rechazados, mer])
				
		writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_proyectos_informacionales.xlsx', engine='xlsxwriter')
		mer.to_excel(writer, index=False)
		writer.save()

else:
	print("El archivo que intenta consultar no existe o no existe en este directorio")