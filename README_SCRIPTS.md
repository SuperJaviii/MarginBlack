README DEL SCRIPT DE SQL

Creacci�n de la base de datos black_margin y las diferentes tablas con las primary keys e �ndices necesarios. Tablas creadas:
		-Result
		-Tls
		-Empleados_csr
		-Des_persona
		-Movimiento_empleados
		-Proyectos_informacionales
		-Trimestres

Este script debe ejecutarse s�lo la primera vez, cuando no existe la base de datos ni las tablas en MySql.

README DE LOS PYTHONS

Este proyecto cuenta con 6 scripts de Python, utilizados para la lectura, carga y limpieza de los datos iniciales, adem�s de encargarse de la eliminaci�n de errores y relacionar MySQL con Python, para que las tablas queden cargadas y listas para su uso en MicroStrategy.

Todos estos Scripts requieren de librerias propias de Python, las cuales deben ser llamadas y alguna instalada previamente por el propio usuario para que todo el proceso discurra con normalidad.

Las librer�as son las siguientes:

		- Librer�a pandas, utilizada para la lectura de datos de los archivos de Excel, generar dataframes en el propio Python, usados para el trato y manipulaci�n de los datos con los que vamos a trabajar, as� como conseguir un formato adecuado de los dataframe descargados desde MySQL.
		De esta librer�a importamos de forma exclusiva uno de sus usos que es ExcelWriter empleado para la creaci�n/escritura/manipulaci�n de archivos Excel en un directorio externo al que se encuentran los datos originales.
		
		- Librer�a sqlalchemy, esta librer�a permite la interacci�n entre Python y MySQL necesaria para la carga y descarga de dataframes de un sitio a otro, para la ejecuci�n adecuada posterior de los programas/aplicaciones que dependen de estas bases de datos.
		
		- Librer�a sys, empleado en la lectura de los par�metros introducidos por pantalla por el usuario, y as� permitir unicamente la carga deseada por el mismo.
		
		-Librer�a configparser, usada para la lectura de archivos de contrase�as y as� tener acceso al Usuario de MySQL instalado en el equipo/servidor externo.

		- Librer�a os.path, permite la comprobaci�n de existencia del archivo inicial que contiene los datos inicial, los cuales ser�n usados en el proceso.
		
		- Librer�a datetime,en estos Scripts su uso es exclusivo para obtener la fecha y hora del d�a de la carga, guardada en el campo de auditor�a.

		
Adem�s en todos los Scripts, se comprueba la validez de los 
par�metros introducidos por pantalla por el usuario, a fin de que no se cometan fallos ni errores, tambi�n se comprueba la existencia del archivo excel del que se van a leer los datos.

Por otro lado se solicita la lectura del archivo de contrase�as de MySQL para el usuario indicado por el cliente en la pantalla al ejecutar el Script de Python.

Descripci�n general de los c�digos de los Scripts de Python:

En todos, se modifican los nombres originales de las columnas leidas del archivo de entrada con los datos, para que lo �nico que aparezca sea texto sin acentuar, ni simbolog�a. El �nico simbolo que se permitir� y no ser� reemplazado ser� "_" utilizado como separaci�n de palabras.

Una vez realizados los cambios anteriores, se pasa a analizar la validez de los datos, eliminando aquellos registros que sean incorrectos o incompletos, y por tanto no utiles en los an�lisis posteriores con MicroStrategy. Todos estos registros eliminados ser�n guardados en un archivo excel bajo el nombre de "rechazados_(nombre del archivo de carga).xlsx" situado en el directorio C:/Users/MicroStrategyBI/Desktop/black_margin_backup/rechazados_black_margin/


Posteriormente, se realiza la carga de los datos a MySQL, generando o actualizando la carga ya existente, con los nuevos datos introducidos.


Por �ltimo en aquellas cargas en las que se requiere un registro acumulado de las cargas, se genera un archivo excel en el directorio C:/Users/MicroStrategyBI/Desktop/black_margin_backup/historicos_black_margin/
bajo el nombre "(nombre de la carga)_acumulados.xlsx"

Este proyecto cuenta con 6 Scripts de Python:
	- trimestres.py, este realiza la carga de la tabla Trimestres.
	
	- result_Script.py que realiza la carga mensual del archivo de Result TH.
	
	- des_persona_Script.py que realiza la carga por mes de los archivo de datos que contiene la informaci�n de los empleados en proyectos del cliente, BBVA.
	
	- empleado_csr_Script.py, lleva a cabo la carga de los datos de los empleados haciendo distinci�n entre empleados propios de Everis y subcontratados, proyectos a los que computan sus horas, horas computadas, fechas de alta y baja en la compa��a,....
	
	- proyectos_informacionales_Script.py, realiza la carga del archivo que contiene el nombre del proyecto y su descripci�n en ese momento, esta carga puede ser actualizada en caso de que aparezca un nuevo proyecto o alguno finalice y se desee eliminar de la carga anterior.
	
	- TLS_Script.py, de forma mensual este Script lleva a cabo la carga de  datos de los empleados que computan horas ese mes en proyectos del BBVA en la tabla tls, incluyendo sus horas de computo. Adem�s, este script hace una comparativa entre meses para determinar las entradas y salidas en cada mes, cargando estos datos en la tabla movimiento_empleados.
	


	
	
	
