import pandas as pd
import pymysql
import sqlalchemy

datos = pd.read_excel("Proyectos Informacionales TD.xlsx").fillna(" ")
datos.columns = list(map(lambda x: x.lower().replace(" ", "_").replace("+","plus"), datos.columns))

engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/margin')

datos.to_sql("proyectos_informacionales", engine, if_exists = "append", index = False)