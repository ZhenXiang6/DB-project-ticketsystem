DO
$$
DECLARE
    table_name TEXT;
BEGIN
    -- 迭代所有資料表
    FOR table_name IN
        SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP TABLE IF EXISTS %I CASCADE;', table_name);
    END LOOP;
END
$$;


-- schema.sql

-- 表1: CATEGORY
CREATE TABLE IF NOT EXISTS CATEGORY (
    c_id SERIAL PRIMARY KEY,
    c_name VARCHAR(15) NOT NULL
);

-- 表2: ORGANIZER
CREATE TABLE IF NOT EXISTS ORGANIZER (
    o_id SERIAL PRIMARY KEY,
    o_name VARCHAR(50) NOT NULL,
    contact_info VARCHAR(50)
);

-- 表3: EVENT
CREATE TABLE IF NOT EXISTS EVENT (
    e_id SERIAL PRIMARY KEY,
    e_name VARCHAR(100) NOT NULL,
    c_id INT NOT NULL,
    o_id INT NOT NULL,
    e_datetime TIMESTAMP NOT NULL,
    e_location VARCHAR(100) NOT NULL,
    description TEXT,
    FOREIGN KEY (c_id) REFERENCES CATEGORY(c_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (o_id) REFERENCES ORGANIZER(o_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 表4: TICKET
CREATE TABLE IF NOT EXISTS TICKET (
    t_id SERIAL PRIMARY KEY,
    e_id INT NOT NULL,
    t_type VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    total_quantity INT NOT NULL CHECK (total_quantity >= 0),
    remain_quantity INT NOT NULL CHECK (remain_quantity >= 0),
    FOREIGN KEY (e_id) REFERENCES EVENT(e_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 表5: CUSTOMER
CREATE TABLE IF NOT EXISTS CUSTOMER (
    cu_id SERIAL PRIMARY KEY,
    cu_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL, -- 把 varchar 從 15 改成 100
    phone_number VARCHAR(50),
    address TEXT,
    pwd VARCHAR(128) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'User'
);

-- 表6: ORDER
CREATE TABLE IF NOT EXISTS "ORDER" (
    or_id SERIAL PRIMARY KEY,
    cu_id INT NOT NULL,
    or_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount > 0),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    is_canceled BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (cu_id) REFERENCES CUSTOMER(cu_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 表7: ORDER_DETAIL
CREATE TABLE IF NOT EXISTS ORDER_DETAIL (
    or_id INT NOT NULL,
    t_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal > 0),
    PRIMARY KEY (or_id, t_id),
    FOREIGN KEY (or_id) REFERENCES "ORDER"(or_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (t_id) REFERENCES TICKET(t_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 表8: PAYMENT
CREATE TABLE IF NOT EXISTS PAYMENT (
    p_id SERIAL PRIMARY KEY,
    or_id INT NOT NULL,
    payment_method VARCHAR(30) NOT NULL, -- 把 varchar 從 10 改成 30
    payment_datetime TIMESTAMP NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    FOREIGN KEY (or_id) REFERENCES "ORDER"(or_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 表9: VENUE
CREATE TABLE IF NOT EXISTS VENUE (
    v_id SERIAL PRIMARY KEY,
    v_name VARCHAR(50) NOT NULL,
    address TEXT,
    capacity INT NOT NULL CHECK (capacity > 0),
    contact_info VARCHAR(50)
);

-- 表10: EVENT_VENUE
CREATE TABLE IF NOT EXISTS EVENT_VENUE (
    e_id INT NOT NULL,
    v_id INT NOT NULL,
    arrangement TEXT,
    PRIMARY KEY (e_id, v_id),
    FOREIGN KEY (e_id) REFERENCES EVENT(e_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (v_id) REFERENCES VENUE(v_id) ON DELETE CASCADE ON UPDATE CASCADE
);


-------插入資料後確保id不會跑掉-------
SELECT setval('category_c_id_seq', COALESCE((SELECT MAX(c_id) FROM CATEGORY),0)+1, false);
SELECT setval('organizer_o_id_seq', COALESCE((SELECT MAX(o_id) FROM ORGANIZER),0)+1, false);
SELECT setval('event_e_id_seq', COALESCE((SELECT MAX(e_id) FROM EVENT),0)+1, false);
SELECT setval('ticket_t_id_seq', COALESCE((SELECT MAX(t_id) FROM TICKET),0)+1, false);
SELECT setval('customer_cu_id_seq', COALESCE((SELECT MAX(cu_id) FROM CUSTOMER),0)+1, false);
SELECT setval('"ORDER_or_id_seq"', COALESCE((SELECT MAX(or_id) FROM "ORDER"),0)+1, false);
SELECT setval('payment_p_id_seq', COALESCE((SELECT MAX(p_id) FROM PAYMENT),0)+1, false);
SELECT setval('venue_v_id_seq', COALESCE((SELECT MAX(v_id) FROM VENUE),0)+1, false);

CREATE INDEX idx_order_cu_id_or_date ON "ORDER" (cu_id, or_date);
