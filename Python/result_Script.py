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
	if path.exists(b + "_Result TH.xlsx"):
		datos = pd.read_excel(b + "_Result TH.xlsx")

		if len(datos) > 0:
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
			datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])
			datos = datos[datos['project'].str.contains("-000193-", case=True)]

			datos1 = datos
			
			datos = datos.drop_duplicates(subset = ["month", "project"], keep = 'first')
			
			datos = datos.dropna(subset = ["month", "project"])
			m = datos.merge(datos1, how = "outer", suffixes = ['','_'], indicator = True)
			mer = m.loc[m._merge.eq('right_only')]
			mer = mer.drop("_merge", axis = 1)
			
			if  len(mer) > 0: 
				print("Existen registros rechazados, compruebe el xlsx generado con los rechazados")
		
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
			
			engine.execute("delete from black_margin.result where month = "+b+";")
			try:
				datos.to_sql("result", engine, if_exists = "append", index = False)
			except:
				print("Error en el formato de la tabla, revise el excel y vuelva a realizar la tabla.")

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
				if path.exists('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_result.xlsx'):
					rechazados = pd.read_excel('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_result.xlsx')
					mer = pd.concat([rechazados, mer])
					
				writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_result.xlsx', engine='xlsxwriter')
				mer.to_excel(writer, index=False)
				writer.save()
		else:
			print("El excel no contiene datos.")
	else:
		print("El archivo que intenta consultar no existe porque la fecha no coincide o no existe en este directorio")
else:
	print("La fecha introducida no es válida. Intentelo de nuevo")
