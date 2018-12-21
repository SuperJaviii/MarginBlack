import pandas as pd
import pymysql
import sqlalchemy

datos = pd.read_excel("201810_Result TH.xlsx")
datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("+","plus"), datos.columns))
 
columnasBuenas = ["month", "project", "sector", "un", "external_subcontrating_revenue",
                 "external_subcontrating_cost", "net_revenue", "total_expenses_plus_csr",
                 "service_rendered_revenue", "other_expenses_cost", "service_rendered_cost"]
				 
columnasTotal =list(datos.columns)

for e in columnasBuenas:
    columnasTotal.remove(e)
    

datos = datos.drop(columnasTotal, axis=1)
datos = datos.fillna(0.0)

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

datos.to_sql("result", engine, if_exists = "append", index = False)

engine.execute("SET @@global.max_allowed_packet = 8388608;")
existe = engine.execute("show tables like 'result'");
for row in existe:
    if not row:
        engine.execute('ALTER TABLE margin.result CHANGE COLUMN month month VARCHAR(45) NOT NULL, CHANGE COLUMN project project VARCHAR(45) NOT NULL, ADD PRIMARY KEY (month, project);') 
