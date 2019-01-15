import pandas as pd
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
		print (u"Lo sentimos. La fecha introducida no cumple el formato. Intentelo de nuevo")
		exit()

year = str(datetime.now())[:4]
b=str(a)
if (len(b)==6) and (int(b[4:])<13) and (int(b[4:])>0) and (int(b[:4]) <=  int(year)+1):
	if path.exists("Organigrama Proyectos Informacional BBVA.xlsx"):
		
		datos = pd.read_excel("Organigrama Proyectos Informacional BBVA.xlsx")

		def cambiarNAN_fecha(x):
			if str(x) == "NaT" or str(x) == "nan":
				return ("2099-01-01")
			elif len(str(x)) > 12 :
				fecha = str(x.year)+"-"+str(x.month)+"-"+str(x.day)
				return (fecha)
			else:
				return x
				
		datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("(","").replace(")","").replace("á","a").replace("é","e")
		.replace("í","i").replace("ó","o").replace("ú","u").replace("%","porcentaje_").replace("codigo_empleado","id_employee")
		.replace("codigo_de_proyecto","project").replace("categoria","employee_category").replace("proyecto","descripcion_2"), datos.columns))

		iter=0
		for i in range(len(datos.id_employee)):
			if str(datos.id_employee[i]) == "?" or str(datos.id_employee[i]) == "nan":
				iter = iter - 1
				datos.id_employee[i] = iter

		datos.fecha_incorporacion = list(map(lambda x: cambiarNAN_fecha(x), datos.fecha_incorporacion))
		datos.fecha_baja = list(map(lambda x: cambiarNAN_fecha(x), datos.fecha_baja))
		datos = datos.fillna(int(0))

		datos1=datos
		
		duplicados=list(datos.duplicated(subset=["month", "id_employee", "project"], keep='first'))
		
		j = 0
		duplic= False
		for i in datos.index:
			if duplicados[j]==False:
				datos1=datos1.drop(datos1[datos1.index == i].index)
			else:
				if not duplic:
					print('Existen registros duplicados, podra encontrar los duplicados en duplicados_des_persona.xlsx, revise la carga')
					duplic=True
			j+=1
				
		datos1.to_excel('duplicados_des_persona.xlsx',index=False)
		
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

		datos['subcontrating']=pd.Series([0 for x in range(len(datos.index))])
		print(len(datos.employee_category))
		for i in range(len(datos.employee_category)):
			if str(datos.employee_category[i]) == str('SUBCONTR'):
				datos.subcontrating[i]=1

		datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])
		datos['month']=pd.Series([a for x in range(len(datos.index))])
		datos = datos.drop_duplicates(subset=["month", "id_employee", "project"], keep="first")
		
		exist = False
		existe = engine.execute("show tables like 'des_persona'");
		for row in existe:
			conn = engine.connect()
			res = conn.execute('select * from des_persona')
			df = pd.DataFrame(res.fetchall())
			conn.close()
			exist = True

		if not exist or len(df) == 0: #Creo la tabla la primera vez
			df = datos
			df.to_sql("des_persona", engine, if_exists = "append", index = False)
		else:
			columnas = list(df.columns)
			for k in range(len(columnas)):
				df = df.rename(columns={columnas[k]:str(datos.columns[k])})

			if a in list(df.month): #Si tengo que actualizar la tabla con datos que SI estan en la base
				df = df.drop(df[df['month'] == a].index)

			df = pd.concat([df,datos])
			df = df.sort_values(by='month', ascending=True)
			engine.execute("truncate des_persona;")
			df.to_sql("des_persona", engine, if_exists = "append", index = False)

	else:
		print("El archivo que intenta consultar no existe")
			
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')
