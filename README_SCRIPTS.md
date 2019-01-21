README DEL SCRIPT DE SQL

Creacción de la base de datos black_margin y las diferentes tablas con las primary keys e índices necesarios. Tablas creadas:
		-Result
		-Tls
		-Empleados_csr
		-Des_persona
		-Movimiento_empleados
		-Proyectos_informacionales
		-Trimestres

Este script debe ejecutarse sólo la primera vez, cuando no existe la base de datos ni las tablas en MySql.

README DE LOS PYTHONS

Este proyecto cuenta con 6 scripts de Python, utilizados para la lectura, carga y limpieza de los datos iniciales, además de encargarse de la eliminación de errores y relacionar MySQL con Python, para que las tablas queden cargadas y listas para su uso en MicroStrategy.

Todos estos Scripts requieren de librerias propias de Python, las cuales deben ser llamadas y alguna instalada previamente por el propio usuario para que todo el proceso discurra con normalidad.

Las librerías son las siguientes:

		- Librería pandas, utilizada para la lectura de datos de los archivos de Excel, generar dataframes en el propio Python, usados para el trato y manipulación de los datos con los que vamos a trabajar, así como conseguir un formato adecuado de los dataframe descargados desde MySQL.
		De esta librería importamos de forma exclusiva uno de sus usos que es ExcelWriter empleado para la creación/escritura/manipulación de archivos Excel en un directorio externo al que se encuentran los datos originales.
		
		- Librería sqlalchemy, esta librería permite la interacción entre Python y MySQL necesaria para la carga y descarga de dataframes de un sitio a otro, para la ejecución adecuada posterior de los programas/aplicaciones que dependen de estas bases de datos.
		
		- Librería sys, empleado en la lectura de los parámetros introducidos por pantalla por el usuario, y así permitir unicamente la carga deseada por el mismo.
		
		-Librería configparser, usada para la lectura de archivos de contraseñas y así tener acceso al Usuario de MySQL instalado en el equipo/servidor externo.

		- Librería os.path, permite la comprobación de existencia del archivo inicial que contiene los datos inicial, los cuales serán usados en el proceso.
		
		- Librería datetime,en estos Scripts su uso es exclusivo para obtener la fecha y hora del día de la carga, guardada en el campo de auditoría.

		
Además en todos los Scripts, se comprueba la validez de los 
parámetros introducidos por pantalla por el usuario, a fin de que no se cometan fallos ni errores, también se comprueba la existencia del archivo excel del que se van a leer los datos.

Por otro lado se solicita la lectura del archivo de contraseñas de MySQL para el usuario indicado por el cliente en la pantalla al ejecutar el Script de Python.

Descripción general de los códigos de los Scripts de Python:

En todos, se modifican los nombres originales de las columnas leidas del archivo de entrada con los datos, para que lo único que aparezca sea texto sin acentuar, ni simbología. El único simbolo que se permitirá y no será reemplazado será "_" utilizado como separación de palabras.

Una vez realizados los cambios anteriores, se pasa a analizar la validez de los datos, eliminando aquellos registros que sean incorrectos o incompletos, y por tanto no utiles en los análisis posteriores con MicroStrategy. Todos estos registros eliminados serán guardados en un archivo excel bajo el nombre de "rechazados_(nombre del archivo de carga).xlsx" situado en el directorio C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/


Posteriormente, se realiza la carga de los datos a MySQL, generando o actualizando la carga ya existente, con los nuevos datos introducidos.


Por último en aquellas cargas en las que se requiere un registro acumulado de las cargas, se genera un archivo excel en el directorio C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/
bajo el nombre "(nombre de la carga)_acumulados.xlsx"

Este proyecto cuenta con 6 Scripts de Python:
	- trimestres.py, este realiza la carga de la tabla Trimestres.
	
	- result_Script.py que realiza la carga mensual del archivo de Result TH.
	
	- des_persona_Script.py que realiza la carga por mes de los archivo de datos que contiene la información de los empleados en proyectos del cliente, BBVA.
	
	- empleado_csr_Script.py, lleva a cabo la carga de los datos de los empleados haciendo distinción entre empleados propios de Everis y subcontratados, proyectos a los que computan sus horas, horas computadas, fechas de alta y baja en la compañía,....
	
	- proyectos_informacionales_Script.py, realiza la carga del archivo que contiene el nombre del proyecto y su descripción en ese momento, esta carga puede ser actualizada en caso de que aparezca un nuevo proyecto o alguno finalice y se desee eliminar de la carga anterior.
	
	- TLS_Script.py, de forma mensual este Script lleva a cabo la carga de  datos de los empleados que computan horas ese mes en proyectos del BBVA en la tabla tls, incluyendo sus horas de computo. Además, este script hace una comparativa entre meses para determinar las entradas y salidas en cada mes, cargando estos datos en la tabla movimiento_empleados.
	


	
	
	
