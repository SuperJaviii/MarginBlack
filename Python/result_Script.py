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
	if path.exists(b + "_Result TH.xlsx"):
		datos = pd.read_excel(b + "_Result TH.xlsx")
		datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(", "").replace(")", "")
							.replace("%","porcentaje").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos.columns))

		 
		columnasBuenas = ["month", "project", "sector", "un", "external_subcontrating_revenue",
						 "external_subcontrating_cost", "net_revenue", "total_expenses_plus_csr",
						 "service_rendered_revenue", "other_expenses_cost", "service_rendered_cost",
						 "commercial_margin_gap", "commercial_margin_gap_porcentaje", "contract_margin_gap", "contract_margin_gap_porcentaje"]
						 
		columnasTotal =list(datos.columns)

		for e in columnasBuenas:
			columnasTotal.remove(e)
			

		datos = datos.drop(columnasTotal, axis=1)
		datos = datos.fillna(0.0)
		datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])
		datos = datos[datos['project'].str.contains("-000193-", case=True)]

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
		existe = engine.execute("show tables like 'result'");
		for row in existe:
			conn = engine.connect()
			res = conn.execute('select * from result')
			df = pd.DataFrame(res.fetchall())
			conn.close()
			exist = True

		if not exist: #Creo la tabla la primera vez
			df = datos
			df.to_sql("result", engine, if_exists = "append", index = False)
		else:
			columnas = list(df.columns)
			for k in range(len(columnas)):
				df = df.rename(columns={columnas[k]:str(datos.columns[k])})

			if a in list(df.month): #Si tengo que actualizar la tabla con datos que SI estan en la base
				df = df.drop(df[df['month'] == a].index)

			df1 = pd.concat([df,datos])
			df2 = df1.sort_values(by='month', ascending=True)
			df2.to_sql("result", engine, if_exists = "replace", index = False)

		
		engine.execute("SET @@global.max_allowed_packet = 8388608;")
		existe = engine.execute("show tables like 'result'");
		for row in existe:
			engine.execute('ALTER TABLE ' +dataBase+'.result CHANGE COLUMN month month BIGINT(20) NOT NULL, CHANGE COLUMN project project VARCHAR(45) NOT NULL, ADD PRIMARY KEY (month, project);') 
		
		conn1=engine.connect()
		res1=conn1.execute('select * from result')
		acumulado=pd.DataFrame(res1.fetchall())
		conn1.close()
		
		columnas= list(acumulado.columns)
		for k in range(len(columnas)):
			acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
			
		if usuario == "SERVIDOR":
			writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/result_acumulado.xlsx', engine='xlsxwriter')
			acumulado.to_excel(writer, index=False)
			writer.save()
			
	else:
		print("El archivo que intenta consultar no existe porque la fecha no coincide o no existe en este directorio")
else:
	print("La fecha introducida no es válida. Intentelo de nuevo")
