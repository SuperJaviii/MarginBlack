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

		if len(datos) > 0:
			datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("-","_").replace("+","plus").replace("(","").replace(")","")
			.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("mes","month"), datos.columns))
			
			datos.horas_estabilizacion = list(map(lambda x: cambiarNAN(x), datos.horas_estabilizacion))
			datos['auditoria']=pd.Series([datetime.now() for x in range(len(datos.index))])
			
			datos1 = datos
			
			datos = datos.drop_duplicates(subset = ["id_employee", "month", "project"], keep = 'first')
			
			datos = datos.dropna(subset = ["id_employee", "month" , "project"])
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
			
			engine.execute("delete from black_margin.tls where month = "+b+";")
			try:
				datos.to_sql("tls", engine, if_exists = "append", index = False)
			except:
				print("Error en el formato de la tabla, revise el excel y vuelva a realizar la tabla.")
			
			# Para obtener las personas que salen o entran cada mes
			
			conn1 = engine.connect()
			res1 = conn1.execute('select * from tls')
			acumulado= pd.DataFrame(res1.fetchall())
			meses=engine.execute("SELECT month from black_margin.tls group by month;")
			
			conn1.close()
			meses_list=[]
			for i in meses:
				meses_list.append(i)
			meses_list=list(map(lambda x: str(x).replace(" ", "").replace("-","").replace("(","").replace(")","").replace(",",""), meses_list))
			
			
			
			columnas = list(acumulado.columns)
			for k in range(len(columnas)):
				acumulado = acumulado.rename(columns={columnas[k]:str(datos.columns[k])})
				
			primer_valor=meses_list[0]
			ultimo_valor=meses_list[len(meses_list) - 1]
			
			acumulado_final = acumulado.drop(["project","proyecto","horas_estabilizacion","persona","auditoria","month"],axis=1)
			resultado_final = pd.DataFrame()
			i=0
			while (primer_valor != ultimo_valor):
				siguiente_valor = meses_list[i+1]
				datos2 = acumulado_final[acumulado.month == int(primer_valor)]
				datos3 = acumulado_final[acumulado.month == int(siguiente_valor)]
				
				combinacion = datos2.merge(datos3, how = "outer", suffixes = ['','_'], indicator = True)
				
				entradas=combinacion.loc[combinacion._merge.eq('right_only')] 
				salidas=combinacion.loc[combinacion._merge.eq('left_only')]
				entradas=entradas.drop("_merge", axis = 1)

				entradas = entradas.drop_duplicates(subset = ["id_employee"], keep = 'first')
				
				entradas['variations'] = 0
				entradas['month'] = siguiente_valor
				
				salidas=salidas.drop("_merge", axis = 1)
				
				salidas = salidas.drop_duplicates(subset = ["id_employee"], keep = 'first')

					
				salidas['variations'] = 1
				salidas['month'] = primer_valor
				
				resultado = pd.concat([salidas,entradas])
				resultado_final = pd.concat([resultado_final,resultado])
				
				primer_valor=siguiente_valor
				i += 1

		
			resultado_final['auditoria']=datetime.now() 
						
			#try:
			engine.execute("truncate movimiento_empleados;")
			resultado_final.to_sql("movimiento_empleados", engine, if_exists = "append", index = False)
			#except:
			#	print("Error en el formato de la tabla, revise el excel y vuelva a realizar la tabla. asjadjajdasjdsja")
				
			if usuario=='SERVIDOR':
				writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/tls_acumulado.xlsx', engine='xlsxwriter')
				datos.to_excel(writer, index=False)
				writer.save()
				if path.exists('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_tls.xlsx'):
					rechazados = pd.read_excel('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_tls.xlsx')
					mer = pd.concat([rechazados, mer])
					
				writer = pd.ExcelWriter('C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/rechazados_tls.xlsx', engine='xlsxwriter')
				mer.to_excel(writer, index=False)
				writer.save()
		else:
			print("El excel no contiene datos.")
	else:
		print("El archivo que intenta consultar no existe porque la fecha no coincide o no existe en este directorio")	
else:
	print('La fecha introducida no es válida. Intentelo de nuevo')