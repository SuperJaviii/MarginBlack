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
		

	- trimestres.py: Este Script se encarga de la carga de la tabla de trimestres, la cual es cargada una �nica vez al principio del trabajo, por lo que este Script debe ser ejecutado el primero, antes de comenzar con alguna carga.
	
	
