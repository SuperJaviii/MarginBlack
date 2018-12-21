import pandas as pd
import pymysql
import sqlalchemy

propuestas = pd.ExcelFile("Seguimiento Backlog vs CSR_External 25.10.xlsx")

datos = propuestas.parse("detalle empleados CSR")

datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("+","plus"), datos.columns))
columnasBuenas = ["employee_category", "project", "hours","expense_month_(adjusted)", "account_month" , "employee_number"]

columnasTotal =list(datos.columns)

for e in columnasBuenas:
    columnasTotal.remove(e)


datos = datos.drop(columnasTotal, axis=1)
datos = datos.fillna(0.0)

for i in range(len(datos.employee_number)):
    if datos.employee_number[i] == "#":
        datos.employee_number[i] = (-i - 1)
		
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

datos.to_sql("empleados_csr", engine, if_exists = "append", index = False)

engine.execute("SET @@global.max_allowed_packet = 8388608;")
existe = engine.execute("show tables like 'empleados_csr'");
for row in existe:
    if not row:
        engine.execute('ALTER TABLE margin.empleados_csr CHANGE COLUMN account_month account_month BIGINT(20) NOT NULL, CHANGE COLUMN expense_month_(adjusted) expense_month_(adjusted) BIGINT(20) NOT NULL, CHANGE COLUMN project project VARCHAR(45) NOT NULL, CHANGE COLUMN employee_number employee_number BIGINT(20) NOT NULL, ADD PRIMARY KEY (account_month,expense_month_(adjusted), project, employee_number);') 
