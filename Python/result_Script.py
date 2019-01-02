import pandas as pd
import pymysql
import sqlalchemy
import sys
from pandas import ExcelWriter

while True:
	try:
		a = int(input(u"Introducir una fecha en formato año y mes(aaaamm): "))
		break
	except ValueError:
		print (u"Lo sentimos. La fecha introducida no cumple el formato. Intentelo de nuevo :")
b=str(a)	

if (len(b)==6):	
	datos = pd.read_excel(b + "_Result TH.xlsx")
	datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(", "").replace(")", ""), datos.columns))
	datos.columns = list(map(lambda x: x.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos.columns))

	 
	columnasBuenas = ["month", "project", "sector", "un", "external_subcontrating_revenue",
					 "external_subcontrating_cost", "net_revenue", "total_expenses_plus_csr",
					 "service_rendered_revenue", "other_expenses_cost", "service_rendered_cost"]
					 
	columnasTotal =list(datos.columns)

	for e in columnasBuenas:
		columnasTotal.remove(e)
		

	datos = datos.drop(columnasTotal, axis=1)
	datos = datos.fillna(0.0)
	
	datos = datos[datos['project'].str.contains("-000193-", case=True)]
	
	engine = sqlalchemy.create_engine('mysql+pymysql://root:everis@localhost:3307/black_margin')
	#engine = sqlalchemy.create_engine('mysql+pymysql://root:password@localhost/world')
	
	datos.to_sql("result", engine, if_exists = "append", index = False)
	
	conn=engine.connect()
	res=conn.execute('select * from result')
	df=pd.DataFrame(res.fetchall())
	conn.close()
	
	columnas= list(df.columns)
	for k in range(len(columnas)):
		df = df.rename(columns={columnas[k]:str(datos.columns[k])})
	
	primero = 0
	lista=list(df['month'])
	for i in range(len(lista)):
		if lista[i] != a:
			if primero==0:
				
				df[i:i+1].to_sql("result", engine, if_exists= "replace",index=False)
				primero=1
			elif (i==len(lista)-1):
				df[i:].to_sql("result", engine, if_exists= "append",index=False)
			else: 
				df[i:i+1].to_sql("result", engine, if_exists= "append",index=False)	

	if primero==0:
		datos.to_sql("result", engine,if_exists = "replace", index = False)
	else:
		
		datos.to_sql("result", engine,if_exists = "append", index = False)
		
	conn1=engine.connect()
	res1=conn1.execute('select * from result')
	df1=pd.DataFrame(res1.fetchall())
	conn1.close()
	
	columnas1= list(df1.columns)
	for k in range(len(columnas1)):
		df1 = df1.rename(columns={columnas1[k]:str(datos.columns[k])})
		
	df2=df1.sort_values(by='month', ascending=True)
	
	df2.to_sql("result", engine, if_exists = "replace", index = False)
	
	engine.execute("SET @@global.max_allowed_packet = 8388608;")
	existe = engine.execute("show tables like 'result'");
	for row in existe:
		if not row:
			engine.execute('ALTER TABLE margin.result CHANGE COLUMN month month VARCHAR(45) NOT NULL, CHANGE COLUMN project project VARCHAR(45) NOT NULL, ADD PRIMARY KEY (month, project);') 
	
	conn1=engine.connect()
	res1=conn1.execute('select * from result')
	acumulado=pd.DataFrame(res1.fetchall())
	conn1.close()
	
	columnas= list(acumulado.columns)
	for k in range(len(columnas)):
		acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
		
	
	writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/result_acumulado.xlsx', engine='xlsxwriter')
	
		
	
	acumulado.to_excel(writer, index=False)

	writer.save()
else:
	print("La fecha introducida no es válida. Intentelo de nuevo")
