CREATE DATABASE administracion CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE administracion;

CREATE TABLE Configuracion_Restaurante (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_Restaurante VARCHAR(100) NOT NULL,
    Direccion TEXT NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Correo_Contacto VARCHAR(100) NOT NULL,
    Horario_Apertura TIME NOT NULL,
    Horario_Cierre TIME NOT NULL,
    Moneda VARCHAR(10) DEFAULT 'MXN',
    Impuesto DECIMAL(5,2) DEFAULT 16.00,
    Tiempo_Reserva_Min INT DEFAULT 30,
    Politica_Cancelacion TEXT,
    Fecha_Actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO Configuracion_Restaurante (Nombre_Restaurante, Direccion, Telefono, Correo_Contacto, Horario_Apertura, Horario_Cierre, Moneda, Impuesto, Tiempo_Reserva_Min, Politica_Cancelacion) VALUES
('Sabores Mexicanos', 'Av. Revolución 123, Col. Centro, CDMX', '+525512345678', 'contacto@saboresmexicanos.com', '08:00:00', '22:00:00', 'MXN', 16.00, 30, 'Cancelaciones con 24 horas de anticipación.'),
('La Parrilla Norteña', 'Calle Hidalgo 45, Monterrey, NL', '+528112345678', 'contacto@parrillanortena.com', '12:00:00', '23:00:00', 'MXN', 16.00, 20, 'Cancelaciones con 12 horas de anticipación.'),
('Bistró Francés', 'Av. Juárez 89, Guadalajara, JAL', '+523312345678', 'info@bistrofrances.com', '09:00:00', '21:00:00', 'MXN', 16.00, 15, 'Cancelaciones con 6 horas de anticipación.');


SELECT * FROM Configuracion_Restaurante;

CREATE TABLE Sucursales (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Direccion TEXT NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Responsable_ID INT,
    Horario_Apertura TIME NOT NULL,
    Horario_Cierre TIME NOT NULL,
    Estatus ENUM('Activa', 'Inactiva', 'En Mantenimiento') DEFAULT 'Activa',
    Fecha_Apertura DATE,
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (Responsable_ID) REFERENCES Configuracion_Restaurante(ID) ON DELETE SET NULL
);

INSERT INTO Sucursales (Nombre, Direccion, Telefono, Responsable_ID, Horario_Apertura, Horario_Cierre, Estatus, Fecha_Apertura) VALUES
('Sabores Mexicanos Polanco', 'Av. Presidente Masaryk 123, Polanco, CDMX', '+525512345679', 1, '09:00:00', '23:00:00', 'Activa', '2015-06-15'),
('La Parrilla Norteña Centro', 'Calle Morelos 56, Monterrey, NL', '+528112345679', 2, '12:00:00', '23:00:00', 'Activa', '2018-03-20'),
('Bistró Francés Chapultepec', 'Av. Chapultepec 200, Guadalajara, JAL', '+523312345679', 3, '09:00:00', '21:00:00', 'Activa', '2019-09-10');


SELECT * FROM Sucursales;

CREATE TABLE Permisos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Codigo VARCHAR(50) NOT NULL UNIQUE,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    Modulo VARCHAR(50) NOT NULL,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Permisos (Codigo, Nombre, Descripcion, Modulo) VALUES
('VER_MENU', 'Ver menú', 'Permite ver el menú del restaurante', 'Menú'),
('EDITAR_MENU', 'Editar menú', 'Permite agregar, modificar o eliminar platillos', 'Menú'),
('GESTIONAR_RESERVAS', 'Gestionar reservaciones', 'Permite confirmar, modificar o cancelar reservaciones', 'Reservaciones');


SELECT * FROM Permisos;

CREATE TABLE Roles (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(25) NOT NULL UNIQUE,
    Descripcion TEXT,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Sucursal_ID INT,
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE SET NULL
);

INSERT INTO Roles (Nombre, Descripcion, Fecha_Creacion, Fecha_Actualizacion) VALUES
('Mesero', 'Atiende mesas y toma pedidos', '2025-06-07', '2025-08-01'),
('Cocinero', 'Prepara los platillos del menú', '2025-06-08', '2025-08-01'),
('Administrador', 'Gestiona todas las operaciones del restaurante', '2025-06-09', '2025-08-01');

SELECT * FROM Roles;

CREATE TABLE Roles_Permisos (
    Rol_ID INT NOT NULL,
    Permiso_ID INT NOT NULL,
    PRIMARY KEY (Rol_ID, Permiso_ID),
    FOREIGN KEY (Rol_ID) REFERENCES Roles(ID) ON DELETE CASCADE,
    FOREIGN KEY (Permiso_ID) REFERENCES Permisos(ID) ON DELETE CASCADE
);

INSERT INTO Roles_Permisos (Rol_ID, Permiso_ID) VALUES
(1, 1),
(1, 3),
(3, 2);

SELECT * FROM Roles_Permisos;

CREATE TABLE Empleados (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Rol_ID INT NOT NULL,
    Sucursal_ID INT,
    Nombre VARCHAR(25) NOT NULL,
    Apellido_P VARCHAR(20) NOT NULL,
    Apellido_M VARCHAR(20),
    Correo VARCHAR(30) NOT NULL UNIQUE,
    Contraseña VARCHAR(12) NOT NULL,
    Telefono VARCHAR(10),
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    RFC VARCHAR(13) UNIQUE,
    CURP VARCHAR(18) UNIQUE,
    Direccion TEXT,
    Fecha_Nacimiento DATE,
    Genero ENUM('Masculino', 'Femenino', 'Otro'),
    Estatus ENUM('Activo', 'Inactivo', 'Suspendido', 'Vacaciones') DEFAULT 'Activo',
    Ultimo_Acceso DATETIME,
    Salario DECIMAL(12,2),
    Tipo_Contrato ENUM('Tiempo Completo', 'Medio Tiempo', 'Temporal', 'Por Horas'),
    Fecha_Contratacion DATE,
    Fecha_Terminacion DATE,
    FOREIGN KEY (Rol_ID) REFERENCES Roles(ID),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE SET NULL
);


INSERT INTO Empleados (
    Rol_ID, Sucursal_ID, Nombre, Apellido_P, Apellido_M, Correo, Contrasena, Telefono, 
    RFC, CURP, Direccion, Fecha_Nacimiento, Genero, Estatus, Ultimo_Acceso, Salario, 
    Tipo_Contrato, Fecha_Contratacion, Fecha_Terminacion
) VALUES
(1, 1, 'Juan', 'Pérez', 'García', 'juan.perez@example.com', 'hash_contrasena1', '5512345678', 
 'PEPJ800101XXX', 'PEPJ800101HDFGRN01', 'Calle Falsa 123, CDMX', '1980-01-01', 'Masculino', 'Activo', '2025-08-01 09:00:00', 12000.00, 
 'Tiempo Completo', '2020-05-10', NULL),

(2, 2, 'María', 'López', 'Fernández', 'maria.lopez@example.com', 'hash_contrasena2', '5523456789', 
 'LOFM850202XXX', 'LOFM850202MDFRGN02', 'Av. Siempre Viva 456, Monterrey', '1985-02-02', 'Femenino', 'Activo', '2025-08-01 08:45:00', 15000.00, 
 'Tiempo Completo', '2019-11-15', NULL),

(3, 3, 'Carlos', 'Ramírez', NULL, 'carlos.ramirez@example.com', 'hash_contrasena3', '5534567890', 
 'RACJ900303XXX', 'RACJ900303HDFRGN03', 'Boulevard Central 789, Guadalajara', '1990-03-03', 'Masculino', 'Vacaciones', '2025-07-30 17:30:00', 13000.00, 
 'Medio Tiempo', '2021-01-20', '2025-12-31');




CREATE TABLE Proveedores (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_Empresa VARCHAR(100) NOT NULL,
    Contacto_Principal VARCHAR(50) NOT NULL,
    Telefono VARCHAR(15) NOT NULL,
    Correo_Electronico VARCHAR(100) NOT NULL,
    Direccion TEXT NOT NULL,
    Tipo_Proveedor VARCHAR(50) NOT NULL,
    RFC VARCHAR(13) UNIQUE,
    Plazo_Entrega INT COMMENT 'Días estimados para entrega',
    Terminos_Pago VARCHAR(50),
    Cuenta_Bancaria VARCHAR(20),
    Banco VARCHAR(50),
    Estatus ENUM('Activo', 'Inactivo', 'Suspendido') DEFAULT 'Activo',
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion DATETIME ON UPDATE CURRENT_TIMESTAMP,
    Fecha_Ultima_Compra DATETIME,
    Monto_Ultima_Compra DECIMAL(12,2),
    Notas TEXT,
    INDEX idx_nombre (Nombre_Empresa),
    INDEX idx_tipo (Tipo_Proveedor),
    INDEX idx_estatus (Estatus)
);

INSERT INTO Proveedores (
    Nombre_Empresa, Contacto_Principal, Telefono, Correo_Electronico, Direccion,
    Tipo_Proveedor, RFC, Plazo_Entrega, Terminos_Pago, Cuenta_Bancaria, Banco,
    Estatus, Fecha_Ultima_Compra, Monto_Ultima_Compra, Notas
) VALUES
('Distribuciones Alimenticias S.A.', 'Luis Martínez', '+525512345678', 'luis.martinez@distribuciones.com', 'Av. Industrial 123, CDMX',
 'Alimentos', 'DAS890123ABC', 5, 'Crédito 30 días', '1234567890123456', 'BBVA',
 'Activo', '2025-07-30', 12500.50, 'Entrega puntual y calidad garantizada.'),

('Bebidas del Valle', 'María Gómez', '+525512345679', 'maria.gomez@bebidasvalle.com', 'Calle Río 45, Guadalajara, JAL',
 'Bebidas', 'BDV900456XYZ', 3, 'Contado', '6543210987654321', 'Santander',
 'Activo', '2025-08-05', 8000.00, 'Se recomienda comprar en grandes volúmenes.'),

('Verduras Frescas S.A.', 'Carlos Sánchez', '+525512345680', 'carlos.sanchez@verdurasfrescas.com', 'Camino Real 789, Monterrey, NL',
 'Verduras', 'VFS780912QWE', 7, 'Crédito 15 días', '7894561230789456', 'Banorte',
 'Activo', '2025-07-28', 4300.75, 'Proveedores locales, productos orgánicos.');


SELECT * FROM Proveedores;

CREATE TABLE Proveedores_Categorias (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Tipo_de_producto TEXT,
    Estatus ENUM('Activa', 'Inactiva') DEFAULT 'Activa'
);

INSERT INTO Proveedores_Categorias (Nombre, Tipo_de_producto, Estatus) VALUES
('Alimentos Secos', 'Cereales, legumbres, harinas, especias', 'Activa'),
('Bebidas', 'Refrescos, jugos, aguas, alcohólicas', 'Activa'),
('Verduras y Frutas', 'Productos frescos, orgánicos y locales', 'Activa');

CREATE TABLE Proveedores_Categorias_Rel (
    Proveedor_ID INT NOT NULL,
    Categoria_ID INT NOT NULL,
    PRIMARY KEY (Proveedor_ID, Categoria_ID),
    FOREIGN KEY (Proveedor_ID) REFERENCES Proveedores(ID) ON DELETE CASCADE,
    FOREIGN KEY (Categoria_ID) REFERENCES Proveedores_Categorias(ID) ON DELETE CASCADE
);

INSERT INTO Proveedores_Categorias_Rel (Proveedor_ID, Categoria_ID) VALUES
(1, 1), 
(2, 2),  
(3, 3); 

CREATE TABLE Mesas (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Numero_Mesa VARCHAR(10) NOT NULL,
    Capacidad INT NOT NULL,
    Ubicacion ENUM('Interior', 'Terraza', 'Barra', 'Privada') NOT NULL,
    Estatus ENUM('Disponible', 'Ocupada', 'Reservada', 'Mantenimiento') DEFAULT 'Disponible',
    Fecha_Ultimo_Uso DATETIME,
    UNIQUE KEY (Sucursal_ID, Numero_Mesa),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE CASCADE
);

INSERT INTO Mesas (Sucursal_ID, Numero_Mesa, Capacidad, Ubicacion, Estatus, Fecha_Ultimo_Uso) VALUES
(1, 'M1', 4, 'Interior', 'Disponible', '2025-08-05 20:30:00'),
(1, 'M2', 2, 'Terraza', 'Ocupada', '2025-08-09 19:45:00'),
(2, 'M1', 6, 'Barra', 'Reservada', '2025-08-07 21:15:00'),
(2, 'M3', 4, 'Interior', 'Disponible', NULL),
(3, 'M1', 8, 'Privada', 'Mantenimiento', '2025-08-01 18:00:00');

CREATE TABLE Zonas_Restaurante (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Capacidad_Maxima INT,
    Descripcion TEXT,
    Estatus ENUM('Activa', 'Inactiva') DEFAULT 'Activa',
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE CASCADE
);

INSERT INTO Zonas_Restaurante (Sucursal_ID, Nombre, Capacidad_Maxima, Descripcion, Estatus) VALUES
(1, 'Zona Interior', 40, 'Área principal con mesas en interior', 'Activa'),
(1, 'Terraza', 20, 'Espacio al aire libre para fumadores', 'Activa'),
(2, 'Barra Principal', 15, 'Barra con servicio directo de bebidas', 'Activa'),
(3, 'Salón Privado', 10, 'Área exclusiva para eventos privados', 'Activa');

CREATE TABLE Clientes (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(25) NOT NULL,
    Apellido_P VARCHAR(20) NOT NULL,
    Apellido_M VARCHAR(20),
    Correo VARCHAR(30) UNIQUE,
    Contrasena VARCHAR(12),
    Telefono VARCHAR(10),
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Nacimiento DATE,
    Genero ENUM('Masculino', 'Femenino', 'Otro', 'Prefiero no decir'),
    Preferencias TEXT,
    Restricciones_Alimenticias TEXT,
    Ultima_Visita DATETIME,
    Estatus ENUM('Activo', 'Inactivo', 'Bloqueado') DEFAULT 'Activo',
    Fecha_Ultima_Actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO Clientes (
    Nombre, Apellido_P, Apellido_M, Correo, Contrasena, Telefono, Fecha_Nacimiento, Genero, Preferencias, Restricciones_Alimenticias, Ultima_Visita, Estatus
) VALUES
('Ana', 'Gómez', 'López', 'ana.gomez@example.com', 'hash_contra1', '5512345678', '1990-05-12', 'Femenino', 'Vegana', 'Sin gluten', '2025-07-30 19:00:00', 'Activo'),
('Luis', 'Martínez', NULL, 'luis.martinez@example.com', 'hash_contra2', '5523456789', '1985-11-23', 'Masculino', 'Prefiere comida picante', NULL, '2025-08-01 20:30:00', 'Activo'),
('Sofía', 'Ramírez', 'Pérez', 'sofia.ramirez@example.com', 'hash_contra3', '5534567890', '1995-07-07', 'Prefiero no decir', 'Sin lactosa', NULL, NULL, 'Activo');

select * from Clientes;

CREATE TABLE Clientes_Direcciones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Cliente_ID INT NOT NULL,
    Alias VARCHAR(50) NOT NULL,
    Direccion TEXT NOT NULL,
    Codigo_Postal VARCHAR(10),
    Ciudad VARCHAR(50),
    Estado VARCHAR(50),
    Pais VARCHAR(50) DEFAULT 'México',
    Referencias TEXT,
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID) ON DELETE CASCADE
);

INSERT INTO Clientes_Direcciones (
    Cliente_ID, Alias, Direccion, Codigo_Postal, Ciudad, Estado, Pais, Referencias
) VALUES
(1, 'Casa', 'Calle Falsa 123, Col. Centro', '06000', 'Ciudad de México', 'CDMX', 'México', 'Frente al parque'),
(1, 'Trabajo', 'Av. Reforma 456, Piso 12', '06600', 'Ciudad de México', 'CDMX', 'México', 'Edificio Torre Reforma'),
(2, 'Casa', 'Calle Luna 789, Col. Norte', '64000', 'Monterrey', 'Nuevo León', 'México', 'Cerca del estadio'),
(3, 'Casa', 'Av. Siempre Viva 101, Col. Sur', '44100', 'Guadalajara', 'Jalisco', 'México', 'Cerca de la plaza principal');

CREATE TABLE Reservaciones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Cliente_ID INT NOT NULL,
    Sucursal_ID INT NOT NULL,
    Mesa_ID INT,
    Fecha_Hora DATETIME NOT NULL,
    Duracion_Estimada INT DEFAULT 90 COMMENT 'Duración en minutos',
    Numero_Personas INT NOT NULL,
    Estatus ENUM('Confirmada', 'Pendiente', 'Cancelada', 'No Presentó') DEFAULT 'Confirmada',
    Notas TEXT,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Empleado_ID INT,
    Requerimientos_Especiales TEXT,
    Codigo_Reserva VARCHAR(12) UNIQUE,
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID),
    FOREIGN KEY (Mesa_ID) REFERENCES Mesas(ID),
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID)
);

INSERT INTO Reservaciones (
    Cliente_ID, Sucursal_ID, Mesa_ID, Fecha_Hora, Duracion_Estimada, Numero_Personas, Estatus, Notas, Empleado_ID, Requerimientos_Especiales, Codigo_Reserva
) VALUES
(1, 1, 1, '2025-08-15 20:00:00', 90, 4, 'Confirmada', 'Celebración de cumpleaños', 1, 'Mesa con vista al jardín', 'RES2025081501'),
(2, 2, 5, '2025-08-16 19:30:00', 120, 2, 'Pendiente', '', 2, '', 'RES2025081602'),
(3, 3, NULL, '2025-08-17 21:00:00', 90, 3, 'Confirmada', 'Aniversario', 3, 'Decoración especial', 'RES2025081703');

CREATE TABLE Categorias_Menu (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    Estatus ENUM('Activo', 'Inactivo', 'Temporal') DEFAULT 'Activo',
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Inicio DATETIME,
    Fecha_Fin DATETIME,
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE CASCADE
);

INSERT INTO Categorias_Menu (Sucursal_ID, Nombre, Descripcion, Estatus, Fecha_Inicio, Fecha_Fin) VALUES
(1, 'Entradas', 'Platos para abrir el apetito', 'Activo', '2025-01-01', NULL),
(1, 'Platos Fuertes', 'Platillos principales de la casa', 'Activo', '2025-01-01', NULL),
(2, 'Postres', 'Dulces y postres deliciosos', 'Activo', '2025-01-01', NULL);

CREATE TABLE Menu (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Categoria_ID INT NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10,2) NOT NULL,
    Tiempo_Preparacion INT COMMENT 'Tiempo estimado en minutos',
    Estatus ENUM('Disponible', 'Agotado', 'Descontinuado', 'Temporal') DEFAULT 'Disponible',
    Es_Destacado BOOLEAN DEFAULT FALSE,
    Nivel_Picante ENUM('Ninguno', 'Suave', 'Medio', 'Alto') DEFAULT 'Ninguno',
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Categoria_ID) REFERENCES Categorias_Menu(ID)
);

INSERT INTO Menu (Categoria_ID, Nombre, Descripcion, Precio, Tiempo_Preparacion, Estatus, Es_Destacado, Nivel_Picante) VALUES
(1, 'Guacamole', 'Delicioso guacamole fresco con totopos', 80.00, 10, 'Disponible', TRUE, 'Medio'),
(1, 'Sopa de tortilla', 'Sopa tradicional con tiras de tortilla', 65.00, 15, 'Disponible', FALSE, 'Suave'),
(2, 'Tacos al pastor', 'Tacos con carne al pastor y piña', 120.00, 20, 'Disponible', TRUE, 'Medio');

CREATE TABLE Ingredientes (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Categoria VARCHAR(50),
    Unidad_Medida VARCHAR(20) NOT NULL,
    Estatus ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Ingredientes (Nombre, Descripcion, Categoria, Unidad_Medida, Estatus) VALUES
('Aguacate', 'Fruta verde utilizada para guacamole y ensaladas', 'Frutas', 'pieza', 'Activo'),
('Tortilla de maíz', 'Base para tacos y otros platillos', 'Cereales', 'pieza', 'Activo'),
('Carne de cerdo adobada', 'Carne marinada para tacos al pastor', 'Carnes', 'gramos', 'Activo'),
('Queso fresco', 'Queso típico mexicano, suave y fresco', 'Lácteos', 'gramos', 'Activo'),
('Huevo', 'Huevo de gallina fresco', 'Huevos', 'pieza', 'Activo');

CREATE TABLE Menu_Ingredientes (
    Menu_ID INT NOT NULL,
    Ingrediente_ID INT NOT NULL,
    Cantidad DECIMAL(10,3) NOT NULL,
    Notas TEXT,
    PRIMARY KEY (Menu_ID, Ingrediente_ID),
    FOREIGN KEY (Menu_ID) REFERENCES Menu(ID) ON DELETE CASCADE,
    FOREIGN KEY (Ingrediente_ID) REFERENCES Ingredientes(ID) ON DELETE CASCADE
);

INSERT INTO Menu_Ingredientes (Menu_ID, Ingrediente_ID, Cantidad, Notas) VALUES
(1, 1, 2.000, 'Para preparar guacamole fresco'),            
(1, 4, 50.000, 'Queso fresco para acompañar'),              
(2, 2, 1.000, 'Una tortilla por sopa'),                     
(3, 3, 150.000, 'Porción de carne al pastor'),              
(3, 2, 2.000, 'Dos tortillas por taco'),
(4, 5, 1.000, 'Un huevo para preparar flan');   


CREATE TABLE CATEGORIA_ALMACEN (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    Estatus ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO CATEGORIA_ALMACEN (ID, Nombre) VALUES
(1, 'Ingredientes secos'),
(2, 'Aceites y líquidos'),
(3, 'Levaduras');

SELECT * FROM CATEGORIA_ALMACEN ORDER BY Fecha_Creacion DESC;

CREATE TABLE SUBCATEGORIA_ALMACEN (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    CategoriaID INT NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    Estatus ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoriaID) REFERENCES CATEGORIA_ALMACEN(ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO SUBCATEGORIA_ALMACEN (CategoriaID, Nombre, Descripcion, Estatus) VALUES
(1, 'Harinas', 'Harinas para panificación y repostería', 'Activo'),
(1, 'Legumbres', 'Frijoles, lentejas, garbanzos', 'Activo'),
(2, 'Aceite de Oliva', 'Aceite de oliva extra virgen', 'Activo'),
(2, 'Aceite de Canola', 'Aceite de canola refinado', 'Activo'),
(3, 'Levadura seca', 'Levadura seca para panificación', 'Activo');

CREATE TABLE Almacen (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    CATEGORIA_ALMACEN_ID INT NOT NULL,
    Cantidad DECIMAL(10,2) NOT NULL,
    Unidad_Medida VARCHAR(20) NOT NULL,
    Costo_Unitario DECIMAL(10,2) DEFAULT NULL,
    Costo_Total DECIMAL(12,2) NOT NULL,
    Fecha_Entrada DATE NOT NULL,
    Fecha_Caducidad DATE DEFAULT NULL,
    Estatus ENUM('Activo', 'Agotado', 'Descontinuado') DEFAULT 'Activo',
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CATEGORIA_ALMACEN_ID) REFERENCES CATEGORIA_ALMACEN(ID) ON DELETE CASCADE
);

INSERT INTO Almacen (Nombre, Descripcion, CATEGORIA_ALMACEN_ID, Cantidad, Unidad_Medida, Costo_Unitario, Costo_Total, Fecha_Entrada, Fecha_Caducidad, Estatus) VALUES
('Harina de trigo', 'Harina para todo uso', 1, 50.00, 'kg', 20.00, 1000.00, '2025-08-01', '2026-02-01', 'Activo'),
('Frijol negro', 'Frijol negro para guisos', 1, 30.00, 'kg', 15.00, 450.00, '2025-07-15', '2026-01-15', 'Activo'),
('Aceite de oliva extra virgen', 'Aceite premium para aderezos', 2, 20.00, 'litros', 120.00, 2400.00, '2025-07-30', '2027-07-30', 'Activo'),
('Levadura seca instantánea', 'Levadura para panadería', 3, 10.00, 'kg', 90.00, 900.00, '2025-08-05', '2026-08-05', 'Activo');

select * from Almacen;

CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    almacen_id INT,
    tipo_movimiento ENUM('entrada', 'salida') NOT NULL,
    cantidad DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    fecha_movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (almacen_id) REFERENCES Almacen(ID)
);

INSERT INTO inventario (almacen_id, tipo_movimiento, cantidad, descripcion) VALUES
(1, 'entrada', 50.00, 'Ingreso inicial de harina de trigo'),
(2, 'entrada', 30.00, 'Ingreso inicial de frijol negro'),
(3, 'entrada', 20.00, 'Ingreso inicial de aceite de oliva'),
(4, 'entrada', 10.00, 'Ingreso inicial de levadura seca');

CREATE TABLE Inventario_Movimientos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Inventario_ID INT NOT NULL,
    Tipo ENUM('Entrada', 'Salida') NOT NULL,
    Cantidad DECIMAL(10,3) NOT NULL,
    Fecha_Movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    Empleado_ID INT NOT NULL,
    Referencia VARCHAR(100) COMMENT 'Número de factura, pedido, etc.',
    Notas TEXT,
    FOREIGN KEY (Inventario_ID) REFERENCES Inventario(ID),
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID)
);

INSERT INTO Inventario_Movimientos (Inventario_ID, Tipo, Cantidad, Empleado_ID, Referencia, Notas) VALUES
(1, 'Entrada', 50.000, 1, 'FACT-1001', 'Ingreso por compra al proveedor'),
(2, 'Entrada', 30.000, 2, 'FACT-1002', 'Ingreso por compra al proveedor'),
(3, 'Entrada', 20.000, 1, 'FACT-1003', 'Ingreso por compra al proveedor'),
(4, 'Entrada', 10.000, 3, 'FACT-1004', 'Ingreso por compra al proveedor'),
(1, 'Salida', 5.000, 1, 'PED-2001', 'Salida para elaboración de pan'),
(2, 'Salida', 3.500, 2, 'PED-2002', 'Salida para platillos del menú');

CREATE TABLE Pedidos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Cliente_ID INT,
    Sucursal_ID INT NOT NULL,
    Mesa_ID INT,
    Empleado_ID INT NOT NULL,
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    Estatus ENUM('Nuevo', 'En preparación', 'Listo', 'Entregado', 'Cancelado', 'Pagado') DEFAULT 'Nuevo',
    Subtotal DECIMAL(10,2),
    Impuestos DECIMAL(10,2),
    Descuentos DECIMAL(10,2),
    Total DECIMAL(10,2),
    Notas TEXT,
    Tipo ENUM('Presencial', 'Domicilio', 'Recoger') NOT NULL,
    Metodo_Pago ENUM('Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Vale', 'Otro') NOT NULL,
    Direccion_Entrega TEXT,
    Telefono_Contacto VARCHAR(15),
    Tiempo_Estimado INT COMMENT 'Tiempo estimado en minutos',
    Fecha_Entrega DATETIME,
    Codigo_Pedido VARCHAR(15) UNIQUE,
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID),
    FOREIGN KEY (Mesa_ID) REFERENCES Mesas(ID),
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID)
);

INSERT INTO Pedidos (
    Cliente_ID, Sucursal_ID, Mesa_ID, Empleado_ID, Fecha_Hora, Estatus,
    Subtotal, Impuestos, Descuentos, Total, Notas, Tipo, Metodo_Pago,
    Direccion_Entrega, Telefono_Contacto, Tiempo_Estimado, Fecha_Entrega, Codigo_Pedido
) VALUES
(1, 1, 1, 1, '2025-08-10 13:00:00', 'Nuevo',
 200.00, 32.00, 0.00, 232.00, 'Sin picante', 'Presencial', 'Efectivo',
 NULL, '5512345678', 45, NULL, 'PED20250810001'),

(2, 2, NULL, 2, '2025-08-10 13:30:00', 'En preparación',
 350.00, 56.00, 20.00, 386.00, 'Entrega rápida, por favor', 'Domicilio', 'Tarjeta Crédito',
 'Av. Siempre Viva 456, Monterrey', '5523456789', 60, '2025-08-10 14:30:00', 'PED20250810002'),

(NULL, 3, 3, 3, '2025-08-10 14:00:00', 'Listo',
 150.00, 24.00, 0.00, 174.00, '', 'Recoger', 'Transferencia',
 NULL, '5534567890', 30, NULL, 'PED20250810003');




CREATE TABLE Caja (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Empleado_ID INT NOT NULL,
    Fecha_Apertura DATETIME NOT NULL,
    Fecha_Cierre DATETIME,
    Monto_Inicial DECIMAL(10,2) NOT NULL,
    Monto_Final DECIMAL(10,2),
    Monto_Teorico DECIMAL(10,2),
    Diferencia DECIMAL(10,2),
    Estatus ENUM('Abierta', 'Cerrada', 'En revisión') DEFAULT 'Abierta',
    Notas TEXT,
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID)
);

INSERT INTO Caja (
    Sucursal_ID, Empleado_ID, Fecha_Apertura, Fecha_Cierre, Monto_Inicial, Monto_Final,
    Monto_Teorico, Diferencia, Estatus, Notas
) VALUES
(1, 1, '2025-08-10 08:00:00', '2025-08-10 20:00:00', 5000.00, 15000.00, 14850.00, 150.00, 'Cerrada', 'Diferencia por propinas no registradas'),
(2, 2, '2025-08-10 09:00:00', NULL, 3000.00, NULL, NULL, NULL, 'Abierta', 'Caja abierta para turno de la mañana'),
(3, 3, '2025-08-09 18:00:00', '2025-08-10 02:00:00', 4000.00, 11000.00, 11000.00, 0.00, 'Cerrada', 'Turno nocturno cerrado sin diferencias');


CREATE TABLE Detalle_Pedido (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Pedido_ID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (Pedido_ID) REFERENCES Pedidos(ID) ON DELETE CASCADE,
    FOREIGN KEY (ProductoID) REFERENCES Menu(ID)
);

INSERT INTO Detalle_Pedido (
    Pedido_ID, ProductoID, Cantidad, PrecioUnitario
) VALUES
(1, 1, 2, 100.00),
(1, 3, 1, 50.00),
(2, 5, 1, 200.00),
(3, 2, 3, 50.00);

CREATE TABLE Transacciones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Caja_ID INT NOT NULL,
    Pedido_ID INT,
    Tipo ENUM('Ingreso', 'Egreso', 'Apertura', 'Cierre') NOT NULL,
    Monto DECIMAL(10,2) NOT NULL,
    Metodo_Pago ENUM('Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Vale', 'Otro') NOT NULL,
    Descripcion TEXT,
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    Empleado_ID INT NOT NULL,
    Referencia VARCHAR(100),
    Estatus ENUM('Confirmada', 'Cancelada', 'Pendiente') DEFAULT 'Confirmada',
    FOREIGN KEY (Caja_ID) REFERENCES Caja(ID),
    FOREIGN KEY (Pedido_ID) REFERENCES Pedidos(ID),
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID)
);

INSERT INTO Transacciones (
    Caja_ID, Pedido_ID, Tipo, Monto, Metodo_Pago, Descripcion, Empleado_ID, Referencia, Estatus
) VALUES
(1, 1, 'Ingreso', 300.00, 'Efectivo', 'Pago de cliente en efectivo', 1, 'REC12345', 'Confirmada'),
(1, NULL, 'Apertura', 5000.00, 'Efectivo', 'Apertura de caja con monto inicial', 1, NULL, 'Confirmada'),
(2, 2, 'Egreso', 150.00, 'Tarjeta Débito', 'Compra de insumos', 2, 'FAC56789', 'Confirmada'),
(3, 3, 'Cierre', 11000.00, 'Efectivo', 'Cierre de caja turno nocturno', 3, NULL, 'Pendiente');


CREATE TABLE Turnos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Empleado_ID INT NOT NULL,
    Fecha DATE NOT NULL,
    Hora_Entrada TIME NOT NULL,
    Hora_Salida TIME,
    descanso DATE NOT NULL,
    Estatus ENUM('Programado', 'En turno', 'Completado', 'Ausente', 'Cancelado') DEFAULT 'Programado',
    Notas TEXT,
    Horas_Extras DECIMAL(4,2) DEFAULT 0.00,
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID)
);

INSERT INTO Turnos (
    Sucursal_ID, Empleado_ID, Fecha, Hora_Entrada, Hora_Salida, descanso, Estatus, Notas, Horas_Extras
) VALUES
(1, 1, '2025-08-10', '08:00:00', '16:00:00', '2025-08-15', 'Completado', 'Turno sin incidencias', 0.00),
(2, 2, '2025-08-10', '09:00:00', NULL, '2025-08-20', 'En turno', 'Turno iniciado, pendiente salida', 1.50),
(3, 3, '2025-08-09', '18:00:00', '02:00:00', '2025-08-15', 'Completado', 'Turno nocturno con horas extras', 2.25);

CREATE TABLE Logs_Acceso (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_ID INT NOT NULL,
    Tipo_Usuario ENUM('Empleado', 'Cliente') NOT NULL,
    Accion VARCHAR(50) NOT NULL,
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    Detalles TEXT,
    Estatus ENUM('Exitoso', 'Fallido') DEFAULT 'Exitoso'
);

INSERT INTO Logs_Acceso (Usuario_ID, Tipo_Usuario, Accion, Detalles, Estatus) VALUES
(1, 'Empleado', 'Login', 'Inicio de sesión exitoso desde IP 192.168.1.10', 'Exitoso'),
(5, 'Cliente', 'Intento de acceso', 'Intento fallido por contraseña incorrecta', 'Fallido'),
(2, 'Empleado', 'Cambio de contraseña', 'Contraseña actualizada correctamente', 'Exitoso'),
(3, 'Cliente', 'Logout', 'Cierre de sesión desde navegador móvil', 'Exitoso');

CREATE TABLE Tickets_Soporte (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Cliente_ID INT,
    Empleado_ID INT,
    Asunto VARCHAR(50) NOT NULL,
    Descripcion TEXT NOT NULL,
    Estatus ENUM('Abierto', 'En proceso', 'Resuelto', 'Cerrado') DEFAULT 'Abierto',
    Prioridad ENUM('Baja', 'Media', 'Alta', 'Crítica') DEFAULT 'Media',
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Solucion TEXT,
    Tiempo_Resolucion INT COMMENT 'Tiempo en minutos',
    Categoria ENUM('Sistema', 'Pedido', 'Pago', 'Reserva', 'Otro'),
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID),
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID)
);

INSERT INTO Tickets_Soporte (Cliente_ID, Empleado_ID, Asunto, Descripcion, Estatus, Prioridad, Solucion, Tiempo_Resolucion, Categoria) VALUES
(1, 3, 'Problema con pago', 'No se procesó el pago con tarjeta de crédito.', 'En proceso', 'Alta', NULL, NULL, 'Pago'),
(3, NULL, 'Error en sistema', 'La aplicación se cierra inesperadamente al abrir el menú.', 'Abierto', 'Crítica', NULL, NULL, 'Sistema'),
(NULL, 2, 'Consulta sobre reserva', 'Cliente solicita cambio de fecha en reserva confirmada.', 'Resuelto', 'Media', 'Cambio realizado correctamente.', 30, 'Reserva'),
(2, 4, 'Duda en pedido', 'Cliente no recibió bebida incluida en el pedido.', 'Cerrado', 'Baja', 'Se reembolsó el monto correspondiente.', 15, 'Pedido');

CREATE TABLE Promociones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Tipo ENUM('Descuento', '2x1', 'Combo', 'Envío Gratis', 'Otro') NOT NULL,
    Valor DECIMAL(10,2),
    Fecha_Inicio DATETIME NOT NULL,
    Fecha_Fin DATETIME NOT NULL,
    Estatus ENUM('Activa', 'Inactiva', 'Pausada') DEFAULT 'Activa',
    Codigo VARCHAR(50) UNIQUE,
    Usos_Maximos INT,
    Usos_Actuales INT DEFAULT 0,
    Aplicable_A ENUM('Todo', 'Categoría', 'Productos específicos') DEFAULT 'Todo',
    Minimo_Compra DECIMAL(10,2),
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE CASCADE
);

INSERT INTO Promociones (
    Sucursal_ID, Nombre, Descripcion, Tipo, Valor, Fecha_Inicio, Fecha_Fin, Estatus,
    Codigo, Usos_Maximos, Usos_Actuales, Aplicable_A, Minimo_Compra
) VALUES
(1, 'Descuento Verano', '10% de descuento en todos los productos', 'Descuento', 10.00, '2025-07-01 00:00:00', '2025-08-31 23:59:59', 'Activa', 'VERANO10', 1000, 0, 'Todo', 100.00),
(2, 'Combo Parrillero', 'Combo especial para 2 personas con bebida incluida', 'Combo', 250.00, '2025-07-15 00:00:00', '2025-09-15 23:59:59', 'Activa', 'COMBOPARR', 500, 0, 'Productos específicos', 0.00),
(3, 'Envío Gratis', 'Envío gratis en pedidos mayores a $300', 'Envío Gratis', 0.00, '2025-08-01 00:00:00', '2025-08-31 23:59:59', 'Pausada', 'ENVIOGRATIS', 200, 0, 'Todo', 300.00);


CREATE TABLE Promociones_Menu (
    Promocion_ID INT NOT NULL,
    Menu_ID INT NOT NULL,
    PRIMARY KEY (Promocion_ID, Menu_ID),
    FOREIGN KEY (Promocion_ID) REFERENCES Promociones(ID) ON DELETE CASCADE,
    FOREIGN KEY (Menu_ID) REFERENCES Menu(ID) ON DELETE CASCADE
);

INSERT INTO Promociones_Menu (Promocion_ID, Menu_ID) VALUES
(2, 1),  
(2, 2),  
(2, 2);

CREATE TABLE Calificaciones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Cliente_ID INT NOT NULL,
    Pedido_ID INT,
    Calificacion_Comida INT CHECK (Calificacion_Comida BETWEEN 1 AND 5),
    Calificacion_Servicio INT CHECK (Calificacion_Servicio BETWEEN 1 AND 5),
    Calificacion_Ambiente INT CHECK (Calificacion_Ambiente BETWEEN 1 AND 5),
    Comentarios TEXT,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Respuesta TEXT,
    Fecha_Respuesta DATETIME,
    Estatus_Respuesta ENUM('Pendiente', 'Respondido') DEFAULT 'Pendiente',
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID),
    FOREIGN KEY (Pedido_ID) REFERENCES Pedidos(ID)
);

INSERT INTO Calificaciones (
    Cliente_ID, Pedido_ID, Calificacion_Comida, Calificacion_Servicio, Calificacion_Ambiente, Comentarios, Estatus_Respuesta
) VALUES
(1, 1, 5, 4, 5, 'Excelente comida y buen servicio.', 'Pendiente'),
(2, 2, 4, 5, 4, 'Muy buen ambiente, pero la comida tardó.', 'Respondido'),
(3, 3, 3, 3, 3, 'Regular, esperaba más.', 'Pendiente');

CREATE TABLE Eventos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Fecha_Inicio DATETIME NOT NULL,
    Fecha_Fin DATETIME NOT NULL,
    Capacidad_Maxima INT,
    Precio_Entrada DECIMAL(10,2),
    Estatus ENUM('Programado', 'Cancelado', 'Completado') DEFAULT 'Programado',
    Requiere_Reserva BOOLEAN DEFAULT TRUE,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID)
);

INSERT INTO Eventos (
    Sucursal_ID, Nombre, Descripcion, Fecha_Inicio, Fecha_Fin, Capacidad_Maxima, Precio_Entrada, Estatus, Requiere_Reserva
) VALUES
(1, 'Noche Mexicana', 'Evento cultural con música y comida típica.', '2025-09-15 19:00:00', '2025-09-15 23:00:00', 100, 250.00, 'Programado', TRUE),
(2, 'Cena Maridaje', 'Cena especial con maridaje de vinos y platillos.', '2025-10-05 20:00:00', '2025-10-05 23:00:00', 50, 1200.00, 'Programado', TRUE),
(3, 'Brunch Dominical', 'Brunch con música en vivo y menú especial.', '2025-08-20 10:00:00', '2025-08-20 14:00:00', 80, 350.00, 'Programado', FALSE);

CREATE TABLE Eventos_Reservaciones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Evento_ID INT NOT NULL,
    Cliente_ID INT NOT NULL,
    Numero_Personas INT NOT NULL,
    Fecha_Reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    Estatus ENUM('Confirmada', 'Pendiente', 'Cancelada', 'Asistió', 'No Asistió') DEFAULT 'Confirmada',
    Monto_Pagado DECIMAL(10,2) DEFAULT 0.00,
    Notas TEXT,
    FOREIGN KEY (Evento_ID) REFERENCES Eventos(ID),
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(ID)
);

INSERT INTO Eventos_Reservaciones (
    Evento_ID, Cliente_ID, Numero_Personas, Estatus, Monto_Pagado, Notas
) VALUES
(1, 1, 4, 'Confirmada', 1000.00, 'Reserva familiar'),
(2, 2, 2, 'Pendiente', 2400.00, 'Reserva para pareja'),
(3, 3, 1, 'Cancelada', 0.00, 'Cancelación por enfermedad');

CREATE TABLE Gastos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Categoria ENUM('Nómina', 'Inventario', 'Servicios', 'Mantenimiento', 'Otros') NOT NULL,
    Descripcion TEXT NOT NULL,
    Monto DECIMAL(10,2) NOT NULL,
    Fecha_Gasto DATE NOT NULL,
    Empleado_ID INT NOT NULL,
    Metodo_Pago ENUM('Efectivo', 'Transferencia', 'Cheque', 'Tarjeta') NOT NULL,
    Proveedor_ID INT,
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID),
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID),
    FOREIGN KEY (Proveedor_ID) REFERENCES Proveedores(ID)
);

INSERT INTO Gastos (
    Sucursal_ID, Categoria, Descripcion, Monto, Fecha_Gasto, Empleado_ID, Metodo_Pago, Proveedor_ID
) VALUES
(1, 'Nómina', 'Pago de sueldos de meseros', 30000.00, '2025-07-31', 1, 'Transferencia', NULL),
(2, 'Inventario', 'Compra de ingredientes secos', 15000.00, '2025-08-02', 2, 'Cheque', 1),
(3, 'Servicios', 'Pago de electricidad', 5000.00, '2025-08-05', 3, 'Efectivo', NULL);

CREATE TABLE Reportes (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Tipo VARCHAR(50) NOT NULL,
    Parametros TEXT,
    Empleado_ID INT NOT NULL,
    Fecha_Generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Archivo VARCHAR(255),
    Estatus ENUM('Generado', 'Fallido', 'En Proceso') DEFAULT 'Generado',
    FOREIGN KEY (Empleado_ID) REFERENCES Empleados(ID)
);

INSERT INTO Reportes (Tipo, Parametros, Empleado_ID, Archivo, Estatus) VALUES
('Ventas Mensuales', '{"mes":"2025-07"}', 1, 'reporte_ventas_2025_07.pdf', 'Generado'),
('Inventario Diario', '{"fecha":"2025-08-09"}', 2, 'reporte_inventario_2025_08_09.pdf', 'En Proceso'),
('Gastos por Sucursal', '{"sucursal_id":3}', 3, NULL, 'Fallido');

CREATE TABLE Notificaciones (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_ID INT NOT NULL,
    Tipo_Usuario ENUM('Empleado') NOT NULL,
    Titulo VARCHAR(100) NOT NULL,
    Mensaje TEXT NOT NULL,
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    Leida BOOLEAN DEFAULT FALSE,
    Fecha_Lectura DATETIME,
    FOREIGN KEY (Usuario_ID) REFERENCES Empleados(ID) ON DELETE CASCADE
);

INSERT INTO Notificaciones (Usuario_ID, Tipo_Usuario, Titulo, Mensaje, Leida) VALUES
(1, 'Empleado', 'Recordatorio de reunión', 'Reunión programada para mañana a las 10:00 AM.', FALSE),
(2, 'Empleado', 'Nuevo pedido asignado', 'Tienes un nuevo pedido para atender en la sucursal.', TRUE),
(3, 'Empleado', 'Actualización de sistema', 'El sistema estará en mantenimiento este sábado.', FALSE);