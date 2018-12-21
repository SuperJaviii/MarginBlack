import pandas as pd
import pymysql
import sqlalchemy

datos = pd.read_excel("TLs Abril 2018.xlsx")

def cambiarNAN(x):
    if str(x) == "?":
        return (0)
    else:
        return x

datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("+","plus"), datos.columns))

datos.horas_estabilización = list(map(lambda x: cambiarNAN(x), datos.horas_estabilización))

i = 0
while str(datos.mes[i]) == "nan":
    i+=1

datos = datos.fillna(datos.mes[i])

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

datos.to_sql("tls", engine, if_exists = "append", index = False)

existe = engine.execute("show tables like 'tls'");
for row in existe:
    if not row:
        engine.execute('ALTER TABLE margin.tls CHANGE COLUMN project project VARCHAR(45) NOT NULL ,CHANGE COLUMN persona persona VARCHAR(45) NOT NULL, CHANGE COLUMN mes mes BIGINT(20) NOT NULL, ADD PRIMARY KEY (project, persona, mes);') 

