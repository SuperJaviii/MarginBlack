CREATE DATABASE black_margin;
USE black_margin;

#**************************************************************************************************************


#Se crea tabla de horas cargadas por empleado, proyecto y fecha con el nombre tls
#Esta tabla se usa para ver el nº de empleados en cada mes en proyectos BBVA y las horas cargadas en OneERP
CREATE TABLE `tls` (
  `project` varchar(20) NOT NULL,
  `proyecto` varchar(20) DEFAULT NULL,
  `persona` varchar(200) DEFAULT NULL,
  `horas_estabilizacion` bigint(20) DEFAULT NULL,
  `id_employee` integer(20) NOT NULL,
  `month` integer(6) NOT NULL,
  `auditoria` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_employee, project, `month`)  
  );
	CREATE INDEX idx_nombre_persona ON tls (persona);


#Se crea la tabla de horas de cierre por empleado, proyecto y fecha  
CREATE TABLE `empleado_csr` (
  `month` integer(6) NOT NULL,
  `expense_month_adjusted` integer(6) DEFAULT NULL,
  `employee_category` varchar(20) DEFAULT NULL,
  `project` varchar(20) NOT NULL,
  `id_employee` integer NOT NULL,
  `hours` integer DEFAULT NULL,
  `auditoria` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_employee, project, `month`)  
 );
	CREATE INDEX idx_employee_category ON empleado_csr (employee_category);
   
  
#Se crea la tabla des_persona como tabla de dimensiones para ampliar información de los empleados 
CREATE TABLE `des_persona` (
  `id_employee` 	integer NOT NULL,
  `nombre` 			varchar(100) DEFAULT NULL,
  `apellidos` 		varchar(200) DEFAULT NULL,
  `employee_category` varchar(20) DEFAULT NULL,
  `rol` 			varchar(20) DEFAULT NULL,
  `tipo` 			varchar(20),
  `unidad_de_negocio` varchar(40) DEFAULT NULL,
  `fecha_incorporacion` date DEFAULT NULL,
  `fecha_baja` 		date DEFAULT NULL,
  `tarifa_` 		float DEFAULT NULL,
  `csr` 			double DEFAULT NULL,
  `porcentaje_cm` 	float DEFAULT NULL,
  `project` 		varchar(20) DEFAULT NULL,
  `descripcion_2` 	varchar(40) DEFAULT NULL,
  `area` 			varchar(20) DEFAULT NULL,
  `tecnologia` 		varchar(20) DEFAULT NULL,
  `subcontrating` 	integer(1) DEFAULT NULL,
  `auditoria` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_employee,rol, project));
	CREATE INDEX idx_fecha_baja ON des_persona (fecha_baja);
  
  
#Se crea la tabla de hechos result que contiene datos económicos de los proyectos BBVA 
  CREATE TABLE `result` (
  `month` integer(6) NOT NULL,
  `sector` varchar(10) DEFAULT NULL,
  `un` varchar(20) DEFAULT NULL,
  `project` varchar(20) NOT NULL,
  `service_rendered_revenue` double DEFAULT NULL,
  `external_subcontrating_revenue` double DEFAULT NULL,
  `net_revenue` double DEFAULT NULL,
  `external_subcontrating_cost` double DEFAULT NULL,
  `other_expenses_cost` double DEFAULT NULL,
  `service_rendered_cost` double DEFAULT NULL,
  `total_expenses_plus_csr` double DEFAULT NULL,
  `contract_margin_gap` double DEFAULT NULL,
  `contract_margin_gap_porcentaje` double DEFAULT NULL,
  `commercial_margin_gap` double DEFAULT NULL,
  `commercial_margin_gap_porcentaje` float DEFAULT NULL,
  `auditoria` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (project, `month`));
	CREATE INDEX idx_project ON result (project);
    
    
#Se crea la tabla de dimensiones proyectos_informacionales para ampliar información de los proyectos 
  CREATE TABLE `proyectos_informacionales` (
  `project` varchar(20) NOT NULL,
  `descripcion` varchar(40) DEFAULT NULL,
  `descripcion_2` varchar(40) DEFAULT NULL,
  `area` varchar(20) DEFAULT NULL,
  `auditoria` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (project));
	CREATE INDEX idx_area ON proyectos_informacionales (area);


#Se crea la tabla de dimensiones trimestres para ampliar información de las fechas 
  CREATE TABLE `trimestres` (
  `month` integer(6) NOT NULL,
  `year` year NOT NULL,
  `Q` varchar(4) DEFAULT NULL,
  `fiscal_year` year DEFAULT NULL,
  `auditoria` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`month`,`year`));
	CREATE INDEX idx_trismestre ON trimestres (Q);