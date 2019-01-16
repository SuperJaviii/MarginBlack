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


		datos.fecha_incorporacion = list(map(lambda x: cambiarNAN_fecha(x), datos.fecha_incorporacion))
		datos.fecha_baja = list(map(lambda x: cambiarNAN_fecha(x), datos.fecha_baja))

		datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])
		datos['month']=pd.Series([a for x in range(len(datos.index))])
		
		datos1 = datos
		
		datos = datos.drop_duplicates(subset = ["month", "id_employee"], keep = 'first')
		
		datos = datos.dropna(subset = ["month", "id_employee"])
		m = datos.merge(datos1, how = "outer", suffixes = ['','_'], indicator = True)
		mer = m.loc[m._merge.eq('right_only')]
		mer = mer.drop("_merge", axis = 1)
		
		datos = datos.reset_index(drop = True)
		
		config = configparser.ConfigParser()
		config.read("configuracion.ini")
		usuario = sys.argv[1]

		usuario = usuario.upper()
		password = config[usuario]["password"]
		user = config[usuario]["user"]
		host = config[usuario]["host"]
		dataBase = config[usuario]["dataBase"]

		engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+dataBase)

		datos['subcontrating']=pd.Series([0 for x in range(len(datos.index))])
		print(len(datos.employee_category))
		for i in range(len(datos.employee_category)):
			if str(datos.employee_category[i]) == str('SUBCONTR'):
				datos.subcontrating[i]=1
		
		engine.execute("delete from black_margin.des_persona where month = "+b+";")
		
		datos.to_sql("des_persona", engine, if_exists = "append", index = False)
		
		if usuario == "SERVIDOR":
			if path.exists('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_des_persona.xlsx'):
				rechazados = pd.read_excel('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_des_persona.xlsx')
				mer = pd.concat([rechazados, mer])
			writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_des_persona.xlsx', engine='xlsxwriter')
			mer.to_excel(writer, index=False)
			writer.save()
			

	else:
		print("El archivo que intenta consultar no existe")
			
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')
