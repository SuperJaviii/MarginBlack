import pandas as pd
import pymysql
import sqlalchemy
import sys 
from pandas import ExcelWriter
import configparser
import os.path as path
from datetime import datetime
while True:
	try:
		a = int(sys.argv[2])
		break
	except ValueError:
		print (u"Lo sentimos. La fecha introducida no cumple el formato. Intentelo de nuevo :")
		
year = str(datetime.now())[:4]
b=str(a)
if (len(b)==6) and (int(b[4:])<13) and (int(b[4:])>0) and (int(b[:4]) <= int(year)+1):	
	if path.exists("TLs_" +b+ ".xlsx"):
		datos = pd.read_excel("TLs_" +b+ ".xlsx")

		def cambiarNAN(x):
			if str(x) == "?" or str(x) == "nan":
				return (0)
			else:
				return x

		datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(","").replace(")","")
		.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("mes","month"), datos.columns))
		
		datos.horas_estabilizacion = list(map(lambda x: cambiarNAN(x), datos.horas_estabilizacion))
		datos = datos.fillna(b)
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
		existe = engine.execute("show tables like 'tls'");
		for row in existe:
			conn = engine.connect()
			res = conn.execute('select * from tls')
			df = pd.DataFrame(res.fetchall())
			conn.close()
			exist = True

		if not exist or len(df) == 0 : #Creo la tabla la primera vez
			df = datos
			df.to_sql("tls", engine, if_exists = "append", index = False)
		else:
			columnas = list(df.columns)
			for k in range(len(columnas)):
				df = df.rename(columns={columnas[k]:str(datos.columns[k])})

			if a in list(df.month): #Si tengo que actualizar la tabla con datos que SI estan en la base
				df = df.drop(df[df['month'] == a].index)

			df = pd.concat([df,datos])
			df = df.sort_values(by='month', ascending=True)
			df.to_sql("tls", engine, if_exists = "replace", index = False)

		
		existe = engine.execute("show tables like 'tls'");
		for row in existe:
			engine.execute('ALTER TABLE '+dataBase+'.tls CHANGE COLUMN project project VARCHAR(20) NOT NULL ,CHANGE COLUMN id_employee id_employee integer(20) NOT NULL, CHANGE COLUMN month month integer(6) NOT NULL, ADD PRIMARY KEY (month, project, id_employee);') 
			
		if usuario=='SERVIDOR':
			writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/tls_acumulado.xlsx', engine='xlsxwriter')
			df.to_excel(writer, index=False)
			writer.save()

	else:
		print("El archivo que intenta consultar no existe porque la fecha no coincide o no existe en este directorio")	
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')