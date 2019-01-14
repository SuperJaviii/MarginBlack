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
	if path.exists("Seguimiento Backlog vs CSR_External_"+b+".xlsx"):
		
		propuestas = pd.ExcelFile("Seguimiento Backlog vs CSR_External_"+b+".xlsx")
		datos = propuestas.parse("detalle empleados CSR") 
		datos_ext = propuestas.parse("detalle empleados External.Sub")

		# tipificación nombres de columnas
		datos.columns = list(map(lambda x: x.lower().replace(" ","_").replace("-","_").replace("+","plus").replace("(","").replace(")","")
		.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("account_month","month"), datos.columns))

		datos_ext.columns = list(map(lambda x: x.lower().replace(" ","_").replace("-","_").replace("+","plus").replace("(","").replace(")","")
		.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("account_month","month"), datos_ext.columns))

		datos = datos.rename(columns={'employee':'id_employee'})
		datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])
		datos_ext = datos_ext.rename(columns={'employee':'id_employee'})
		datos_ext['auditoria']=pd.Series([datetime.now() for x in range(len(datos_ext.index))])

		columnasBuenas = ["employee_category", "project", "hours","expense_month_adjusted", "month" , "id_employee", "auditoria"]

		columnasTotal = list(datos.columns)
		columnasTotal_ext = list(datos_ext.columns)
		for e in columnasBuenas:
			columnasTotal.remove(e)
			columnasTotal_ext.remove(e)

		datos = datos.drop(columnasTotal, axis=1)
		datos = datos.fillna(0.0)
		datos_ext = datos_ext.drop(columnasTotal_ext, axis=1)
		datos_ext = datos_ext.fillna(0.0)
		
		#filtrar datos
		datos = datos[datos['project'].str.contains("-000193-", case=True)]
		datos_ext = datos_ext[datos_ext['project'].str.contains("-000193-", case=True)]
		
		datos = pd.concat([datos,datos_ext])
		datos = datos.drop_duplicates(subset=["month", "expense_month_adjusted", "project", "id_employee"], keep="last")
		
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
		existe = engine.execute("show tables like 'empleado_csr'");
		for row in existe:
			conn = engine.connect()
			res = conn.execute('select * from empleado_csr')
			df = pd.DataFrame(res.fetchall())
			conn.close()
			exist = True
			
		if not exist or len(df) == 0: #Creo la tabla la primera vez
			df = datos
			df.to_sql("empleado_csr", engine, if_exists = "append", index = False)
		else:
			columnas = list(df.columns)
			for k in range(len(columnas)):
				df = df.rename(columns={columnas[k]:str(datos.columns[k])})

			if a in list(df.month): #Si tengo que actualizar la tabla con datos que SI estan en la base
				df = df.drop(df[df['month'] == a].index)

			df = pd.concat([df,datos])
			df = df.sort_values(by='month', ascending=True)
			df.to_sql("empleado_csr", engine, if_exists = "replace", index = False)
		
		existe = engine.execute("show tables like 'empleado_csr'");
		for row in existe:
			engine.execute('ALTER TABLE '+dataBase+'.empleado_csr CHANGE COLUMN month month integer(6) NOT NULL, CHANGE COLUMN expense_month_adjusted expense_month_adjusted integer(6) NOT NULL, CHANGE COLUMN project project VARCHAR(20) NOT NULL, CHANGE COLUMN id_employee id_employee integer(20) NOT NULL, ADD PRIMARY KEY (month, expense_month_adjusted, project, id_employee);') 

		if usuario=='SERVIDOR':
			writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/empleado_csr_acumulado.xlsx', engine='xlsxwriter')
			df.to_excel(writer, index=False)
			writer.save()
	else:
		print("El archivo que intenta consultar no existe porque la fecha no coincide o no existe en este directorio")
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')