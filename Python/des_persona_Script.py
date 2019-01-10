import pandas as pd
import pymysql
import sqlalchemy
import sys 
from pandas import ExcelWriter
import configparser
	
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

config = configparser.ConfigParser()
config.read("configuracion.ini")
	
usuario = sys.argv[1]

usuario = usuario.upper()
password = config[usuario]["password"]
user = config[usuario]["user"]
host = config[usuario]["host"]
dataBase = config[usuario]["dataBase"]

print(password)

engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+dataBase)
#engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

datos['subcontrating']=pd.Series([0 for x in range(len(datos.index))])
for i in range(len(datos.employee_category)):
	if str(datos.employee_category[i])=='SUBCONTR':
		datos.subcontrating[i]=1

		
exist = False
existe = engine.execute("show tables like 'des_persona'");
for row in existe:
	conn = engine.connect()
	res = conn.execute('select * from des_persona')
	df = pd.DataFrame(res.fetchall())
	conn.close()
	exist = True

if not exist: #Creo la tabla la primera vez
	df = datos
	df.to_sql("des_persona", engine, if_exists = "replace", index = False)
else:
	datos.to_sql("des_persona", engine, if_exists = "replace", index = False)
	
	
existe = engine.execute("show tables like 'des_persona'")
for row in existe:

	engine.execute('ALTER TABLE '+dataBase+'.des_persona CHANGE COLUMN project project VARCHAR(45) NOT NULL ,CHANGE COLUMN id_employee id_employee BIGINT(20) NOT NULL ,CHANGE COLUMN rol rol VARCHAR(45) NOT NULL, ADD PRIMARY KEY (project, id_employee,rol);') 		


