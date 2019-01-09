#CREATE DATABASE black_margin;
#USE black_margin;
CREATE TABLE `tls` (
  `project` varchar(20) NOT NULL,
  `proyecto` varchar(20) DEFAULT NULL,
  `persona` varchar(200) DEFAULT NULL,
  `horas_estabilizacion` bigint(20) DEFAULT NULL,
  `id_employee` integer(20) NOT NULL,
  `month` integer(6) NOT NULL,
  PRIMARY KEY (id_employee, project, `month`)  
  );
  CREATE INDEX idx_nombre_persona ON tls (persona);
  
CREATE TABLE `empleado_csr` (
  `month` integer(6) NOT NULL,
  `expense_month_adjusted` integer(6) DEFAULT NULL,
  `employee_category` varchar(20) DEFAULT NULL,
  `project` varchar(20) NOT NULL,
  `id_employee` integer NOT NULL,
  `hours` integer DEFAULT NULL,
  PRIMARY KEY (id_employee, project, `month`)  
 );
 CREATE INDEX idx_employee_category ON empleado_csr (employee_category);
   
  
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
  PRIMARY KEY (id_employee));
  CREATE INDEX idx_fecha_baja ON des_persona (fecha_baja);
  
  
  