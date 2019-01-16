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
		datos['auditoria']=pd.Series([])
		
		datos1 = datos
		
		datos = datos.drop_duplicates(subset = ["month", "project", "id_employee"], keep = 'first')
		
		datos = datos.dropna(subset = ["month", "project", "id_employee"])
		m = datos.merge(datos1, how = "outer", suffixes = ['','_'], indicator = True)
		mer = m.loc[m._merge.eq('right_only')]
		mer = mer.drop("_merge", axis = 1)
		
		if  len(mer) > 0: 
			print("Existen registros rechazados, compruebe el xlsx generado con los rechazados")
		datos = datos.reset_index(drop = True)
		#****
		mer.to_excel('duplicados_TLS.xlsx',index=False)
		#********
		
		config = configparser.ConfigParser()
		config.read("configuracion.ini")
		
		usuario = sys.argv[1]

		usuario = usuario.upper()
		password = config[usuario]["password"]
		user = config[usuario]["user"]
		host = config[usuario]["host"]
		dataBase = config[usuario]["dataBase"]

		engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+dataBase)
		
		engine.execute("delete from black_margin.tls where month = "+b+";")
		datos.to_sql("tls", engine, if_exists = "append", index = False)
			
		if usuario=='SERVIDOR':
			writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/tls_acumulado.xlsx', engine='xlsxwriter')
			df.to_excel(writer, index=False)
			writer.save()
			if path.exists('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_tls.xlsx'):
				rechazados = pd.read_excel('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_tls.xlsx')
				mer = pd.concat([rechazados, mer])
				
			writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_tls.xlsx', engine='xlsxwriter')
			mer.to_excel(writer, index=False)
			writer.save()
			
	else:
		print("El archivo que intenta consultar no existe porque la fecha no coincide o no existe en este directorio")	
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')