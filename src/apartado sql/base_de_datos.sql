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

INSERT INTO Configuracion_Restaurante (
    Nombre_Restaurante, 
    Direccion, 
    Telefono, 
    Correo_Contacto, 
    Horario_Apertura, 
    Horario_Cierre, 
    Moneda, 
    Impuesto, 
    Tiempo_Reserva_Min, 
    Politica_Cancelacion
) VALUES (
    'Sabores Mexicanos', 
    'Av. Revolución 123, Col. Centro, CDMX', 
    '+525512345678', 
    'contacto@saboresmexicanos.com', 
    '08:00:00', 
    '22:00:00', 
    'MXN', 
    16.00, 
    30, 
    'Cancelaciones con 24 horas de anticipación. No shows tendrán cargo del 50% del consumo estimado.'
);

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

INSERT INTO Sucursales (
    Nombre, 
    Direccion, 
    Telefono, 
    Responsable_ID, 
    Horario_Apertura, 
    Horario_Cierre, 
    Estatus, 
    Fecha_Apertura
) VALUES (
    'Sabores Mexicanos Polanco', 
    'Av. Presidente Masaryk 123, Polanco, CDMX', 
    '+525512345679', 
    1, 
    '09:00:00', 
    '23:00:00', 
    'Activa', 
    '2015-06-15'
);

SELECT * FROM Sucursales;

CREATE TABLE Permisos (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Codigo VARCHAR(50) NOT NULL UNIQUE,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    Modulo VARCHAR(50) NOT NULL,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM Permisos;

CREATE TABLE Roles (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(25) NOT NULL UNIQUE,
    Descripcion TEXT,
    Fecha_Creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
);

SELECT * FROM Roles;

CREATE TABLE Roles_Permisos (
    Rol_ID INT NOT NULL,
    Permiso_ID INT NOT NULL,
    PRIMARY KEY (Rol_ID, Permiso_ID),
    FOREIGN KEY (Rol_ID) REFERENCES Roles(ID) ON DELETE CASCADE,
    FOREIGN KEY (Permiso_ID) REFERENCES Permisos(ID) ON DELETE CASCADE
);

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

SELECT * FROM Proveedores;

CREATE TABLE Proveedores_Categorias (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Tipo_de_producto TEXT,
    Estatus ENUM('Activa', 'Inactiva') DEFAULT 'Activa'
);

CREATE TABLE Proveedores_Categorias_Rel (
    Proveedor_ID INT NOT NULL,
    Categoria_ID INT NOT NULL,
    PRIMARY KEY (Proveedor_ID, Categoria_ID),
    FOREIGN KEY (Proveedor_ID) REFERENCES Proveedores(ID) ON DELETE CASCADE,
    FOREIGN KEY (Categoria_ID) REFERENCES Proveedores_Categorias(ID) ON DELETE CASCADE
);

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

CREATE TABLE Zonas_Restaurante (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Nombre VARCHAR(50) NOT NULL,
    Capacidad_Maxima INT,
    Descripcion TEXT,
    Estatus ENUM('Activa', 'Inactiva') DEFAULT 'Activa',
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE CASCADE
);

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

-- pao pao

CREATE TABLE almacen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(30),
    costo_unitario DECIMAL(10,2) DEFAULT NULL,
    costo_total DECIMAL(12,2) NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_caducidad DATE DEFAULT NULL,
    estatus ENUM('activo','agotado','descontinuado') DEFAULT 'activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    tipo_movimiento ENUM('entrada','salida','ajuste','devolución') NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    fecha_movimiento DATE NOT NULL,
    documento_referencia VARCHAR(100),
    usuario_responsable VARCHAR(100),
    comentarios TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES almacen(id) ON DELETE CASCADE
);

-- a qui  termina pao pao

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

CREATE TABLE Ingredientes (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Categoria VARCHAR(50),
    Unidad_Medida VARCHAR(20) NOT NULL,
    Estatus ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    Fecha_Registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Menu_Ingredientes (
    Menu_ID INT NOT NULL,
    Ingrediente_ID INT NOT NULL,
    Cantidad DECIMAL(10,3) NOT NULL,
    Notas TEXT,
    PRIMARY KEY (Menu_ID, Ingrediente_ID),
    FOREIGN KEY (Menu_ID) REFERENCES Menu(ID) ON DELETE CASCADE,
    FOREIGN KEY (Ingrediente_ID) REFERENCES Ingredientes(ID) ON DELETE CASCADE
);



CREATE TABLE Inventario (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Sucursal_ID INT NOT NULL,
    Ingrediente_ID INT NOT NULL,
    Cantidad_Actual DECIMAL(10,3) NOT NULL,
    Stock_Minimo DECIMAL(10,3) NOT NULL,
    Stock_Maximo DECIMAL(10,3),
    Ultimo_Precio DECIMAL(10,2),
    Proveedor_ID INT,
    Fecha_Ultima_Entrada DATETIME,
    Fecha_Ultima_Salida DATETIME,
    Estatus ENUM('Disponible', 'Agotado', 'En Espera', 'Caducado') DEFAULT 'Disponible',
    Fecha_Caducidad DATE,
    Lote VARCHAR(50),
    FOREIGN KEY (Sucursal_ID) REFERENCES Sucursales(ID) ON DELETE CASCADE,
    FOREIGN KEY (Ingrediente_ID) REFERENCES Ingredientes(ID),
    FOREIGN KEY (Proveedor_ID) REFERENCES Proveedores(ID)
);

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

CREATE TABLE Detalle_Pedido (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Pedido_ID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (Pedido_ID) REFERENCES Pedidos(ID) ON DELETE CASCADE,
    FOREIGN KEY (ProductoID) REFERENCES Menu(ID)
);

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

CREATE TABLE Logs_Acceso (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Usuario_ID INT NOT NULL,
    Tipo_Usuario ENUM('Empleado', 'Cliente') NOT NULL,
    Accion VARCHAR(50) NOT NULL,
    Fecha_Hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    Detalles TEXT,
    Estatus ENUM('Exitoso', 'Fallido') DEFAULT 'Exitoso'
);

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

CREATE TABLE Promociones_Menu (
    Promocion_ID INT NOT NULL,
    Menu_ID INT NOT NULL,
    PRIMARY KEY (Promocion_ID, Menu_ID),
    FOREIGN KEY (Promocion_ID) REFERENCES Promociones(ID) ON DELETE CASCADE,
    FOREIGN KEY (Menu_ID) REFERENCES Menu(ID) ON DELETE CASCADE
);

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