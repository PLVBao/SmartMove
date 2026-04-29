-- =========================
-- SMARTMOVERS DATABASE
-- =========================

DROP DATABASE IF EXISTS smartmovers_db;
CREATE DATABASE smartmovers_db;
-- =========================
-- TẠO BẢNG
-- =========================

CREATE TABLE Customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    category VARCHAR(20) NOT NULL,
    CHECK (category IN ('Category 1', 'Category 2', 'Category 3'))
);

CREATE TABLE Depot (
    depot_id VARCHAR(20) PRIMARY KEY,
    location VARCHAR(100) NOT NULL
);

CREATE TABLE Product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    risk_type VARCHAR(20) NOT NULL,
    CHECK (risk_type IN ('No Risk', 'High Risk'))
);

CREATE TABLE Container (
    container_id VARCHAR(20) PRIMARY KEY,
    container_type VARCHAR(50) NOT NULL
);

CREATE TABLE TransportUnit (
    transport_unit_id VARCHAR(20) PRIMARY KEY,
    depot_id VARCHAR(20) NOT NULL,
    lorry VARCHAR(100) NOT NULL,
    driver VARCHAR(100) NOT NULL,
    assistant VARCHAR(100) NOT NULL,
    FOREIGN KEY (depot_id) REFERENCES Depot(depot_id)
);

CREATE TABLE Transport (
    transport_unit_id VARCHAR(20) NOT NULL,
    container_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (transport_unit_id, container_id),
    FOREIGN KEY (transport_unit_id) REFERENCES TransportUnit(transport_unit_id),
    FOREIGN KEY (container_id) REFERENCES Container(container_id)
);

CREATE TABLE Job (
    job_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    depot_id VARCHAR(20) NOT NULL,
    start_location VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (depot_id) REFERENCES Depot(depot_id)
);

CREATE TABLE `Load` (
    load_id VARCHAR(20) PRIMARY KEY,
    job_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    transport_unit_id VARCHAR(20) NOT NULL,
    load_size VARCHAR(20) NOT NULL,
    FOREIGN KEY (job_id) REFERENCES Job(job_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (transport_unit_id) REFERENCES TransportUnit(transport_unit_id),
    CHECK (load_size IN ('small', 'medium', 'large'))
);

CREATE TABLE PaymentRule (
    customer_category VARCHAR(20) NOT NULL,
    product_risk VARCHAR(20) NOT NULL,
    load_size VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (customer_category, product_risk, load_size),
    CHECK (customer_category IN ('Category 1', 'Category 2', 'Category 3')),
    CHECK (product_risk IN ('No Risk', 'High Risk')),
    CHECK (load_size IN ('small', 'medium', 'large'))
);

-- =========================
-- DỮ LIỆU MẪU
-- =========================

INSERT INTO Customer (customer_id, name, address, phone, category) VALUES
('C001', 'ABC Chemical Co.', '12 Nguyen Trai, Ho Chi Minh City', '0901234567', 'Category 1'),
('C002', 'Green Solutions Ltd.', '45 Le Loi, Da Nang', '0902345678', 'Category 2'),
('C003', 'Mekong Industry', '78 Tran Hung Dao, Can Tho', '0903456789', 'Category 3'),
('C004', 'Sai Gon Logistics', '21 Vo Van Tan, Ho Chi Minh City', '0904567890', 'Category 1'),
('C005', 'Eastern Materials', '99 Hai Ba Trung, Ha Noi', '0905678901', 'Category 2'),
('C006', 'Blue Ocean Chemical', '15 Bach Dang, Hai Phong', '0906789012', 'Category 3'),
('C007', 'Viet Industrial Supply', '33 Pham Van Dong, Binh Duong', '0907890123', 'Category 1');

INSERT INTO Depot (depot_id, location) VALUES
('D001', 'Ho Chi Minh City'),
('D002', 'Da Nang'),
('D003', 'Can Tho'),
('D004', 'Ha Noi'),
('D005', 'Hai Phong'),
('D006', 'Binh Duong'),
('D007', 'Dong Nai'),
('D008', 'Quang Ninh'),
('D009', 'Ba Ria - Vung Tau');

INSERT INTO Product (product_id, product_name, risk_type) VALUES
('P001', 'Sulfuric Acid', 'High Risk'),
('P002', 'Ethanol', 'High Risk'),
('P003', 'Detergent Base', 'No Risk'),
('P004', 'Industrial Salt', 'No Risk'),
('P005', 'Ammonia Solution', 'High Risk'),
('P006', 'Sodium Chloride', 'No Risk'),
('P007', 'Methanol', 'High Risk');

INSERT INTO Container (container_id, container_type) VALUES
('CT001', 'Tank Container'),
('CT002', 'Dry Container'),
('CT003', 'Chemical Container'),
('CT004', 'Standard Container'),
('CT005', 'Refrigerated Chemical Container'),
('CT006', 'Liquid Chemical Container'),
('CT007', 'Hazardous Material Container');

INSERT INTO TransportUnit (transport_unit_id, depot_id, lorry, driver, assistant) VALUES
('TU001', 'D001', 'Lorry A', 'Nguyen Van A', 'Tran Van B'),
('TU002', 'D001', 'Lorry B', 'Le Van C', 'Pham Van D'),
('TU003', 'D002', 'Lorry C', 'Hoang Van E', 'Do Van F'),
('TU004', 'D003', 'Lorry D', 'Bui Van G', 'Nguyen Thi H'),
('TU005', 'D004', 'Lorry E', 'Tran Van I', 'Le Thi K'),
('TU006', 'D005', 'Lorry F', 'Pham Van L', 'Ho Van M'),
('TU007', 'D006', 'Lorry G', 'Dang Van N', 'Vo Thi O');

INSERT INTO Transport (transport_unit_id, container_id) VALUES
('TU001', 'CT001'),
('TU002', 'CT002'),
('TU003', 'CT003'),
('TU004', 'CT004'),
('TU005', 'CT005'),
('TU006', 'CT006'),
('TU007', 'CT007');

INSERT INTO Job (job_id, customer_id, depot_id, start_location, destination) VALUES
('J001', 'C001', 'D001', 'Ho Chi Minh City', 'Binh Duong'),
('J002', 'C002', 'D002', 'Da Nang', 'Quang Nam'),
('J003', 'C003', 'D003', 'Can Tho', 'Vinh Long'),
('J004', 'C004', 'D001', 'Ho Chi Minh City', 'Dong Nai'),
('J005', 'C005', 'D004', 'Ha Noi', 'Hai Phong'),
('J006', 'C006', 'D005', 'Hai Phong', 'Quang Ninh'),
('J007', 'C007', 'D006', 'Binh Duong', 'Ba Ria - Vung Tau');

INSERT INTO `Load` (load_id, job_id, product_id, transport_unit_id, load_size) VALUES
('L001', 'J001', 'P001', 'TU001', 'large'),
('L002', 'J001', 'P003', 'TU002', 'medium'),
('L003', 'J002', 'P002', 'TU003', 'small'),
('L004', 'J003', 'P004', 'TU004', 'medium'),
('L005', 'J004', 'P005', 'TU001', 'large'),
('L006', 'J005', 'P003', 'TU005', 'small'),
('L007', 'J006', 'P007', 'TU006', 'medium'),
('L008', 'J007', 'P006', 'TU007', 'large');

INSERT INTO PaymentRule (customer_category, product_risk, load_size, price) VALUES
('Category 1', 'No Risk', 'small', 100.00),
('Category 1', 'No Risk', 'medium', 150.00),
('Category 1', 'No Risk', 'large', 200.00),
('Category 1', 'High Risk', 'small', 180.00),
('Category 1', 'High Risk', 'medium', 250.00),
('Category 1', 'High Risk', 'large', 320.00),

('Category 2', 'No Risk', 'small', 120.00),
('Category 2', 'No Risk', 'medium', 170.00),
('Category 2', 'No Risk', 'large', 220.00),
('Category 2', 'High Risk', 'small', 200.00),
('Category 2', 'High Risk', 'medium', 270.00),
('Category 2', 'High Risk', 'large', 340.00),

('Category 3', 'No Risk', 'small', 140.00),
('Category 3', 'No Risk', 'medium', 190.00),
('Category 3', 'No Risk', 'large', 240.00),
('Category 3', 'High Risk', 'small', 220.00),
('Category 3', 'High Risk', 'medium', 290.00),
('Category 3', 'High Risk', 'large', 360.00);

-- =========================
-- VIEW TÍNH TỔNG CHI PHÍ THEO JOB
-- =========================

CREATE VIEW JobCost AS
SELECT
    j.job_id,
    c.customer_id,
    c.name AS customer_name,
    SUM(pr.price) AS total_cost
FROM `Load` l
JOIN Job j ON l.job_id = j.job_id
JOIN Customer c ON j.customer_id = c.customer_id
JOIN Product p ON l.product_id = p.product_id
JOIN PaymentRule pr
    ON pr.customer_category = c.category
   AND pr.product_risk = p.risk_type
   AND pr.load_size = l.load_size
GROUP BY j.job_id, c.customer_id, c.name;


