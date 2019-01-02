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
	datos = pd.read_excel("TLs_" +b+ ".xlsx")

	def cambiarNAN(x):
		if str(x) == "?":
			return (0)
		else:
			return x

	datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(","").replace(")","").replace("mes","month"), datos.columns))
	datos.columns = list(map(lambda x: x.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos.columns))
	
	datos.horas_estabilizacion = list(map(lambda x: cambiarNAN(x), datos.horas_estabilizacion))
	
	
	i = 0
	while str(datos.month[i]) == "nan":
		i+=1

	datos = datos.fillna(datos.month[i])

	engine = sqlalchemy.create_engine('mysql+pymysql://root:everis@localhost:3307/black_margin')
	#engine = sqlalchemy.create_engine('mysql+pymysql://root:password@localhost/world')
	datos.to_sql("tls", engine,if_exists = "append", index = False)
	
	conn=engine.connect()
	res=conn.execute('select * from tls')
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
				
				df[i:i+1].to_sql("tls", engine, if_exists= "replace",index=False)
				primero=1
			elif (i==len(lista)-1):
				df[i:].to_sql("tls", engine, if_exists= "append",index=False)
			else: 
				df[i:i+1].to_sql("tls", engine, if_exists= "append",index=False)	

	
	if primero==0:
		datos.to_sql("tls", engine,if_exists = "replace", index = False)
	else:
		
		datos.to_sql("tls", engine,if_exists = "append", index = False)
	
	conn1=engine.connect()
	res1=conn1.execute('select * from tls')
	df1=pd.DataFrame(res1.fetchall())
	conn1.close()
	
	columnas1= list(df1.columns)
	for k in range(len(columnas1)):
		df1 = df1.rename(columns={columnas1[k]:str(datos.columns[k])})
		
	df2=df1.sort_values(by='month', ascending=True)
	
	df2.to_sql("tls", engine, if_exists = "replace", index = False)
	
	
	
	existe = engine.execute("show tables like 'tls'");
	for row in existe:
		if not row:
			engine.execute('ALTER TABLE margin.tls CHANGE COLUMN project project VARCHAR(45) NOT NULL ,CHANGE COLUMN persona persona VARCHAR(45) NOT NULL, CHANGE COLUMN month month BIGINT(20) NOT NULL, ADD PRIMARY KEY (project, persona, month);') 
	
	conn1=engine.connect()
	res1=conn1.execute('select * from tls')
	acumulado=pd.DataFrame(res1.fetchall())
	conn1.close()
	
	columnas= list(acumulado.columns)
	for k in range(len(columnas)):
		acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
		
	aux = acumulado
	writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/tls_acumulado.xlsx', engine='xlsxwriter')
	
	
	acumulado.to_excel(writer, index=False)

	writer.save()
	
	columnasBuenas = ["id_employee", "persona"]
					 
	columnasTotal =list(aux.columns)

	for e in columnasBuenas:
		columnasTotal.remove(e)
		

	aux = aux.drop(columnasTotal, axis=1)
	aux1=aux.sort_values(by='id_employee')
	
	aux2 =aux1.drop_duplicates(subset='id_employee',keep='last')
	
	aux2.to_sql("des_persona", engine, if_exists = "replace", index= False)
	
	writer1 = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/des_persona.xlsx', engine='xlsxwriter')
	
	
	
	aux2.to_excel(writer1, index=False)

	writer1.save()

else:
	print('La fecha introducida no es válida. Intentelo de nuevo')