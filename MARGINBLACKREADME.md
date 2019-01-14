README CUADRO DE MANDO "MARGIN BLACK"

El cuadro de mando del Visual Inght del proyecto "MarginBlack" consta, a fecha 15-01-2019, de cuatro pestañas 
que se detallan en el presente documento.

PESTAÑA 1: "PORTADA"

En la primera pestaña se pueden distinguir tres visualizaciones, junto a dos KPI (creados en un cuadro de texto 
debido a limitaciones técnicas) que aparecen en la parte superior derecha.
 
A continuacion se describe la informacion que cada elemento ofrece.

* KPI "Empleados": Muestra el numero actual de empleados que componen el area de everis BBVA.

* KPI "Beneficio": Muestra el beneficio total del conjunto de proyectos que conforman el area de BBVA desde abril 
		   hasta la actualidad. En un futuro, cuando haya datos de más meses, este KPI mostrara el 
		   beneficio total del ultimo año.

* Visualización "INGRESOS": Se compone de un grafico de barras y una linea de tendencia.
			    El grafico de barras permite visualizar los ingresos que se han obtenido en el mes de octubre. 
			    A medida que se vaya teniendo acceso a los datos de los meses siguientes se ira añadiendo la 
			    información. Finalmente tiene que quedar el agregado del ingreso en el año presente de cada 
			    proyecto. 
			    El eje que escala esta informacion es el de la izquierda, y la magnitud es Euros.
			    La linea verde indica el valor del "comercial margin black" de cada proyecto. 
			    El eje que escala esta informacion es el de la derecha, y la magnitud es un porcentaje.


* Visualizacion "EMPLEADOS": Se compone de un grafico de barras compuesto apilado y una linea de tendencia.
			     El grafico de barras muestra el numero de empleados. La seccion verde indica el numero de 
			     empleados internos de Everis que trabajan en proyectos de BBVA, mientras que la seccion
			     violeta representa el numero de empleados subcontratados de éste mismo área. 
			     La linea de tendencia permite visualizar la suma de los dos anteriores, devolviendo el 
			     numero de empleados totales del area de BBVA.
			     Ambas visualizaciones estan distribuidas por mes, por lo que la informacion que ofrecen
			     es mensual.

* Visualizacion "TOP CONTRACT MARGIN GAP": Se trata de un grafico de barras horizontales. En él se muestra en el eje y 
					   el codigo del proyecto y en el eje x el valor del "contract margin gap".
					   Se han filtrado los proyectos que tenian un valor de 0 en este parámetro y se
					   han ordenado de mayor a menor. 


FILTROS: Las visualizaciones "INGRESOS" y "EMPLEADOS" funcionan simultaneamente como filtros una sobre otra. Desde la 
	 primera se puede filtrar sobre la segunda y viceversa. 
	 De esta manera, si se hace click en uno de los proyectos que se muestran en "INGRESOS", la grafica "EMPLEADOS" 
	 representará el numero de empleados totales, internos y subcontratados de ese proyecto en concreto.
	 Por otra parte, si se hace click en alguno de los meses que aparecen en "EMPLEADOS" se obtendra en "INGRESOS" 
	 lo correspondiente al mes seleccionado.

Nota: Actualmente sólo se tienen datos de "INGRESOS" del mes de octubre, por lo que el filtro aplicado sobre esta 
      visualizacion no tendra utilidad hasta que se actualice la base de datos con la informacion de los meses posteriores.



PESTAÑA 2: "HEADCOUNT"

La segunda pestaña se compone de 3 visualizaciones. Dos cuadriculas con informacion y un grafico de barras con linea de 
tendencia.

* Visualizacion "NUMERO DE EMPLEADOS POR PROYECTO": En esta cuadricula se puede encontrar el numero de empleados de los que 
						    consta o ha constado cada proyecto en los ultimos meses, asi como el 
						    codigo, area, y sector al que pertenecen. El primer campo de la tabla
						    indica el mes y el año en formato "aaaamm".

* Visualizacion "EMPLEADOS EN PROYECTOS": Es una cuadricula donde aparecen los detalles de los empleados que conforman cada 
					  proyecto. 
					  Se muestra en primer lugar el proyecto al que pertenece (aquellos donde ha imputado 
					  horas), seguido de numero de empleado, apellidos, nombre y categoria.

*Visualizacion "NUMERO DE EMPLEADOS": Es un grafico compuesto de barras verticales apiladas y una linea de tendencia.
				      Contiene la misma informacion que la visualizacion "EMPLEADOS" de la pestaña 1.

FILTROS: La visualizacion "NUMERO DE EMPLEADOS POR PROYECTO" se puede usar como filtro sobre "NUMERO DE EMPLEADOS" y 
	 "EMPLEADOS POR PROYECTO". Del mismo modo, "NUMERO DE EMPLEADOS" aplica filtro sobre "NUMERO DE EMPLEADOS POR 
	 PROYECTO" y "EMPLEADOS EN PROYECTOS". 
	 De esta manera, al seleccionar un mes o un proyecto en "NUMERO DE EMPLEADOS POR PROYECTO", aparecera el numero 
	 de empleados correspondiente a ese mes o proyecto en "NUMERO DE EMPLEADOS", y los detalles de los mismos en "EMPLEADOS 
	 EN PROYECTOS". 
	 Por otro lado, al seleccionar un mes en la visualizacion "NUMERO DE EMPLEADOS", apareceran solo los proyectos de 
	 ese mes en "NUMERO DE EMPLEADOS POR PROYECTO", y los empleados que formaban parte de la plantilla en dicho periodo.
	 Se puede seleccionar un mes en "NUMERO DE EMPLEADOS" y simultaneamente un proyecto en "NUMERO DE EMPLEADOS POR PROYECTO" 
	 si se quiere ver la informacion de los empleados de un solo proyecto en un mes en concreto.



PESTAÑA 3: ESTABILIZACION-CIERRE

Esta pestaña consta de una unica visualizacion a la que se le pueden aplicar tres filtros, tanto por separado como de manera 
simultanea. 

* Visualizacion "ESTABILIZACION-CIERRE": Es un grafico de barras que representa la diferencia entre las horas de estabilización 
					 y las horas de cierre de cada empleado del area BBVA. 
					 En la parte superior se pueden accionar tres filtros: MES, PROYECTO Y EMPLEADO.
						
					 Se puede seleccionar el mes/proyecto/empleado del que se desea obtener la informacion, o 
					 hacer una seleccion multiple. De esta manera, a medida que se van agregando empleados van 
					 apareciendo barras que representan a cada uno de ellos, mientras que al agregar proyectos 
					 o meses en los filtros se van sumando el total de las diferencias de horas estabilizacion 
					 y horas cierre de cada empleado que se muestre. 



PESTAÑA 4: TM/TM-1 Presupuesto:

Esta pestaña consta de dos visualizaciones a las que se le pueden aplicar dos filtros que se encuentran en la parte superior de la 
misma.

* Visualización "INGRESOS-GASTOS/NETO": Es un grafico compuesto de barras agrupadas, diferenciadas por colores y distribuidas por 
					proyecto.
					De color verde se representa la diferencia entre ingresos y gastos del proyecto que se indica 
					en el eje x, mientras que el color violeta simboliza el beneficio neto que se ha presentado en 
					el mismo. 
					La magnitud en la que estos parametros se miden es miles de Euros, tal y como indica la leyenda.

* Visualizacion "MARGEN/COMERCIAL MARGIN GAP": Es un grafico compuesto de barras con linea de tendencia, distribuido por proyecto. 
					       A traves de las barras se representa el margen, expresado en porcentaje sobre el beneficio 
					       y escalado en el eje de la izquierda.
					       Con la linea de tendencia se representa el valor del "comercial margin gap" de cada proyecto. 
					       Las unidades en las que se expresa es tambien en porcentaje, ya que se obtiene a traves de la 
					       diferencia entre margenes y éstos , 
					       y está escalado segun el eje que aparece a la izquierda de la visualización.

FILTROS: Las visualizaciones de esta pestaña no actúan como filtros. Solo funcionan como tales los que se encuentran en la parte superior 
	 de la pestaña.
	 En primer lugar hay un filtro por proyecto, que permite ver los indicadores anteriormente expuestos de uno o varios proyectos,
	 y que se aplica a las dos visualizaciones. 
	 Por otra parte hay un filtro de mes, que de momento no tiene funcionalidad ya que solo se tienen datos del mes de octubre, pero que 
	 comenzara a poder usarse cuando la base de datos del proyecto se vaya ampliando.
	 
