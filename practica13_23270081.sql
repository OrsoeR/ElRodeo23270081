DROP DATABASE IF EXISTS ElRodeo;
CREATE DATABASE ElRodeo;
USE ElRodeo;

-- Tabla de Categorías
CREATE TABLE Categoria (
    idcategoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    activo BOOLEAN DEFAULT 1,  -- Campo para marcar si está activo o no
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de creación
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Fecha de modificación
) ENGINE=InnoDB;

-- Tabla de Unidades de Medida
CREATE TABLE unidades (
    idunidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    activo BOOLEAN DEFAULT 1,  -- Campo para marcar si está activo o no
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de creación
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Fecha de modificación
) ENGINE=InnoDB;

-- Tabla de Artículos
CREATE TABLE Articulos (
    codigo VARCHAR(13) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    existencia INT NOT NULL,
    unidad_id INT NOT NULL,
    categoria_id INT NOT NULL,
    activo BOOLEAN DEFAULT 1,  -- Campo para marcar si está activo o no
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de creación
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Fecha de modificación
    FOREIGN KEY (unidad_id) REFERENCES Unidades(idunidad) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (categoria_id) REFERENCES Categoria(idcategoria) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Tabla de Clientes
CREATE TABLE Clientes (
    telefono VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    rfc VARCHAR(13),
    correo VARCHAR(100),
    clave VARCHAR(255) NOT NULL, -- Se recomienda almacenar de forma encriptada
    activo BOOLEAN DEFAULT 1,  -- Campo para marcar si está activo o no
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de creación
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Fecha de modificación
) ENGINE=InnoDB;

-- Tabla de Métodos de Pago
CREATE TABLE MetodoPago (
    idmetodo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- Tabla de Ventas
CREATE TABLE Ventas (
    venta_id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    cliente_telefono VARCHAR(10) NOT NULL,
    metodo_pago_id INT NOT NULL,
    FOREIGN KEY (cliente_telefono) REFERENCES Clientes(telefono) ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (metodo_pago_id) REFERENCES MetodoPago(idmetodo) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Trigger para establecer la fecha automáticamente en Ventas
DELIMITER //
CREATE TRIGGER before_insert_ventas
BEFORE INSERT ON Ventas
FOR EACH ROW
BEGIN
    IF NEW.fecha IS NULL THEN
        SET NEW.fecha = CURDATE();
    END IF;
END;
//
DELIMITER ;

-- Tabla de Detalle de Ventas
CREATE TABLE DetalleVenta (
    detalle_id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT NOT NULL,
    articulo_codigo VARCHAR(13) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (articulo_codigo) REFERENCES Articulos(codigo) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Tabla de Movimientos de Inventario
CREATE TABLE MovimientosInventario (
    idmovimiento INT AUTO_INCREMENT PRIMARY KEY,
    articulo_codigo VARCHAR(13) NOT NULL,
    tipo ENUM('Entrada', 'Salida') NOT NULL,
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (articulo_codigo) REFERENCES Articulos(codigo) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Vista para Artículos Activos con sus Categorías y Unidades
CREATE VIEW vista_articulos AS
SELECT 
    a.codigo, a.nombre AS articulo_nombre, a.precio, a.costo, a.existencia, 
    c.nombre AS categoria, 
    u.nombre AS unidad
FROM Articulos a
JOIN Categoria c ON a.categoria_id = c.idcategoria
JOIN Unidades u ON a.unidad_id = u.idunidad
WHERE a.activo = 1;

-- Insertar datos en Categoria
INSERT INTO Categoria (nombre) VALUES 
('Monturas'), 
('Sombreros'), 
('Texanas'), 
('Cinturones'), 
('Accesorios');

-- Insertar datos en Unidades
INSERT INTO unidades (nombre) VALUES ('Pieza'), ('Metro'), ('Litro');

-- Insertar datos en Articulos
INSERT INTO Articulos (codigo, nombre, precio, costo, existencia, unidad_id, categoria_id) VALUES
('7501001234567', 'Montura Charra Clásica', 8500.00, 5000.00, 5, 1, 1),
('7501001234568', 'Sombrero Fino de Lana', 1200.00, 700.00, 15, 1, 2),
('7501001234569', 'Texana Cuero Genuino', 2500.00, 1500.00, 10, 1, 3),
('7501001234570', 'Cinturón Piel Repujado', 800.00, 400.00, 20, 1, 4),
('7501001234571', 'Espuelas de Acero Inoxidable', 950.00, 500.00, 8, 1, 5);

-- Insertar datos en Clientes
INSERT INTO Clientes (telefono, nombre, direccion, rfc, correo, clave) VALUES
('9614597357', 'Juan Pérez', 'Calle Ficticia 123, Ciudad, Estado', 'JUPE750101XYZ', 'juanperez@email.com', 'hashed_password_1'),
('9614597358', 'Ana González', 'Avenida Maluco 456, Ciudad, Estado', 'ANGO800202ABC', 'ana@email.com', 'hashed_password_2');

-- Insertar datos en Métodos de Pago
INSERT INTO MetodoPago (nombre) VALUES ('Efectivo'), ('Tarjeta de Crédito'), ('Transferencia Bancaria');

-- Insertar datos en Ventas
INSERT INTO Ventas (fecha, importe, iva, total, cliente_telefono, metodo_pago_id) VALUES
(CURDATE(), 10000.00, 1600.00, 11600.00, '9614597357', 1),
(CURDATE(), 5000.00, 800.00, 5800.00, '9614597358', 2);

-- Insertar datos en DetalleVenta
INSERT INTO DetalleVenta (venta_id, articulo_codigo, cantidad, precio, subtotal) VALUES
(1, '7501001234567', 1, 8500.00, 8500.00),
(1, '7501001234568', 2, 1200.00, 2400.00),
(2, '7501001234569', 3, 2500.00, 7500.00);

