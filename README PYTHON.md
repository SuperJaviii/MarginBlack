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
		

	- trimestres.py: Este Script se encarga de la carga de la tabla de trimestres, la cual es cargada una única vez al principio del trabajo, por lo que este Script debe ser ejecutado el primero, antes de comenzar con alguna carga.
	
	
