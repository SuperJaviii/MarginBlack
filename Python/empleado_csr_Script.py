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
	propuestas = pd.ExcelFile("Seguimiento Backlog vs CSR_External_"+b+".xlsx")

	datos = propuestas.parse("detalle empleados CSR") 
	datos_ext = propuestas.parse("detalle empleados External.Sub")

	# tipificación nombres de columnas
	datos.columns = list(map(lambda x: x.lower().replace(" ","_").replace("-","_").replace("+","plus").replace("account_month","month"), datos.columns))
	datos.columns = list(map(lambda x: x.replace("(","").replace(")","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos.columns))

	datos_ext.columns = list(map(lambda x: x.lower().replace(" ","_").replace("-","_").replace("+","plus").replace("account_month","month"), datos_ext.columns))
	datos_ext.columns = list(map(lambda x: x.replace("(","").replace(")","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"), datos_ext.columns))
	
	datos=datos.rename(columns={'employee':'id_employee'})
	datos_ext=datos_ext.rename(columns={'employee':'id_employee'})

	columnasBuenas = ["employee_category", "project", "hours","expense_month_adjusted", "month" , "id_employee"]

	columnasTotal =list(datos.columns)
	columnasTotal_ext =list(datos_ext.columns)
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
	
	#engine = sqlalchemy.create_engine('mysql+pymysql://root:password@localhost/world')
	engine = sqlalchemy.create_engine('mysql+pymysql://root:everis@localhost:3307/black_margin')

	datos.to_sql("empleado_csr", engine, if_exists = "append", index = False)
	datos_ext.to_sql("empleado_csr", engine, if_exists = "append", index = False)

	conn=engine.connect()
	res=conn.execute('select * from empleado_csr')
	df=pd.DataFrame(res.fetchall())
	conn.close()
		
	columnas= list(df.columns)
	for k in range(len(columnas)):
		df = df.rename(columns={columnas[k]:str(datos.columns[k])})
		
	df2 = df.drop_duplicates()

	df2.to_sql("empleado_csr", engine, if_exists = "replace", index = False)

	engine.execute("SET @@global.max_allowed_packet = 8388608;")
	existe = engine.execute("show tables like 'empleados_csr'");
	for row in existe:
		if not row:
			engine.execute('ALTER TABLE margin.empleados_csr CHANGE COLUMN month month BIGINT(20) NOT NULL, CHANGE COLUMN expense_month_(adjusted) expense_month_(adjusted) BIGINT(20) NOT NULL, CHANGE COLUMN project project VARCHAR(45) NOT NULL, CHANGE COLUMN id_employee id_employee BIGINT(20) NOT NULL, ADD PRIMARY KEY (month,expense_month_(adjusted), project, id_employee);') 

	conn1=engine.connect()
	res1=conn1.execute('select * from empleado_csr')
	acumulado=pd.DataFrame(res1.fetchall())
	conn1.close()
		
	columnas= list(acumulado.columns)
	for k in range(len(columnas)):
		acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})

	writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/empleados_csr_acumulado.xlsx', engine='xlsxwriter')
	acumulado.to_excel(writer, index=False)
	writer.save()
	
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')