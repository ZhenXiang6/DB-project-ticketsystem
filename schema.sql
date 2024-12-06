-- 建立 CATEGORY 表
CREATE TABLE CATEGORY (
    c_id SERIAL PRIMARY KEY,
    c_name VARCHAR(100) NOT NULL
);

-- 建立 ORGANIZER 表
CREATE TABLE ORGANIZER (
    o_id SERIAL PRIMARY KEY,
    o_name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(255)
);

-- 建立 EVENT 表
CREATE TABLE EVENT (
    e_id SERIAL PRIMARY KEY,
    e_name VARCHAR(100) NOT NULL,
    c_id INT NOT NULL,
    o_id INT NOT NULL,
    e_datetime TIMESTAMP NOT NULL,
    description TEXT,
    FOREIGN KEY (c_id) REFERENCES CATEGORY(c_id),
    FOREIGN KEY (o_id) REFERENCES ORGANIZER(o_id)
);

-- 建立 VENUE 表
CREATE TABLE VENUE (
    v_id SERIAL PRIMARY KEY,
    v_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    capacity INT,
    contact_info VARCHAR(255)
);

-- 建立 SEAT 表
CREATE TABLE SEAT (
    seat_id SERIAL PRIMARY KEY,
    v_id INT NOT NULL,
    section VARCHAR(50),
    row VARCHAR(10),
    number INT,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (v_id) REFERENCES VENUE(v_id)
);

-- 建立 TICKET_TYPE 表
CREATE TABLE TICKET_TYPE (
    e_id INT NOT NULL,
    t_type VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (e_id, t_type),
    FOREIGN KEY (e_id) REFERENCES EVENT(e_id)
);

-- 建立 TICKET 表，新增 seat_id
CREATE TABLE TICKET (
    t_id SERIAL PRIMARY KEY,
    e_id INT NOT NULL,
    t_type VARCHAR(50) NOT NULL,
    seat_id INT, -- 可為 NULL，表示無座位
    total_quantity INT NOT NULL,
    remaining_quantity INT NOT NULL,
    FOREIGN KEY (e_id, t_type) REFERENCES TICKET_TYPE(e_id, t_type),
    FOREIGN KEY (seat_id) REFERENCES SEAT(seat_id)
);

-- 建立 CUSTOMER 表
CREATE TABLE CUSTOMER (
    cu_id SERIAL PRIMARY KEY,
    cu_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255)
);

-- 建立 ORDER 表
CREATE TABLE "ORDER" (
    or_id SERIAL PRIMARY KEY,
    cu_id INT NOT NULL,
    or_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(50),
    FOREIGN KEY (cu_id) REFERENCES CUSTOMER(cu_id)
);

-- 建立 ORDER_DETAIL 表
CREATE TABLE ORDER_DETAIL (
    or_id INT NOT NULL,
    detail_id SERIAL PRIMARY KEY,
    t_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (or_id) REFERENCES "ORDER"(or_id),
    FOREIGN KEY (t_id) REFERENCES TICKET(t_id)
);

-- 建立 PAYMENT 表
CREATE TABLE PAYMENT (
    p_id SERIAL PRIMARY KEY,
    or_id INT NOT NULL,
    payment_method VARCHAR(50),
    p_datetime TIMESTAMP NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (or_id) REFERENCES "ORDER"(or_id)
);

-- 建立 EVENT_VENUE 表（多對多關係）
CREATE TABLE EVENT_VENUE (
    e_id INT NOT NULL,
    v_id INT NOT NULL,
    PRIMARY KEY (e_id, v_id),
    FOREIGN KEY (e_id) REFERENCES EVENT(e_id),
    FOREIGN KEY (v_id) REFERENCES VENUE(v_id)
);
