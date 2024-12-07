INSERT INTO CATEGORY (c_name) 
VALUES 
('Music'),
('Sports'),
('Theater'),
('Art'),
('Comedy');


INSERT INTO ORGANIZER (o_name, contact_info) 
VALUES 
('LiveNation', '123-456-7890'),
('EventMasters', '987-654-3210'),
('ComedyCentral', '555-555-5555'),
('ArtExpo', '222-333-4444'),
('SportsHub', '444-555-6666');

select *
from ORGANIZER;


INSERT INTO EVENT (e_name, c_id, o_id, e_datetime, e_location, description) 
VALUES 
('Rock Concert', 1, 1, '2024-12-15 20:00:00', 'Stadium A', 'A live rock music concert with famous bands.'),
('Football Match', 2, 5, '2024-12-18 17:00:00', 'Stadium B', 'Exciting football match between top teams.'),
('Broadway Show', 3, 2, '2024-12-20 19:00:00', 'Theater C', 'A popular Broadway show with stunning performances.'),
('Art Exhibition', 4, 4, '2024-12-25 10:00:00', 'Gallery D', 'An art exhibition showcasing contemporary artworks.'),
('Stand-Up Comedy', 5, 3, '2024-12-30 21:00:00', 'Comedy Club E', 'A night of stand-up comedy with famous comedians.');


INSERT INTO EVENT (e_name, c_id, o_id, e_datetime, e_location, description) 
VALUES 
('Rock Concert', 1, 1, '2024-12-15 20:00:00', 'Stadium A', 'A live rock music concert with famous bands.'),
('Football Match', 2, 5, '2024-12-18 17:00:00', 'Stadium B', 'Exciting football match between top teams.'),
('Broadway Show', 3, 2, '2024-12-20 19:00:00', 'Theater C', 'A popular Broadway show with stunning performances.'),
('Art Exhibition', 4, 4, '2024-12-25 10:00:00', 'Gallery D', 'An art exhibition showcasing contemporary artworks.'),
('Stand-Up Comedy', 5, 3, '2024-12-30 21:00:00', 'Comedy Club E', 'A night of stand-up comedy with famous comedians.');


INSERT INTO TICKET (e_id, t_type, price, total_quantity, remain_quantity) 
VALUES 
(1, 'VIP', 100.00, 200, 200),
(1, 'General', 50.00, 500, 500),
(2, 'VIP', 120.00, 150, 150),
(2, 'General', 60.00, 400, 400),
(3, 'VIP', 80.00, 100, 100),
(3, 'General', 40.00, 300, 300),
(4, 'Standard', 20.00, 150, 150),
(5, 'VIP', 70.00, 100, 100),
(5, 'General', 30.00, 500, 500);


INSERT INTO CUSTOMER (cu_name, email, phone_number, address) 
VALUES 
('Alice Zhang', 'alice@example.com', '123-987-6543', '123 Street, City A'),
('Bob Li', 'bob@example.com', '234-876-5432', '456 Avenue, City B'),
('Charlie Wang', 'charlie@example.com', '345-765-4321', '789 Road, City C'),
('Diana Chen', 'diana@example.com', '456-654-3210', '101 Blvd, City D'),
('Eve Liu', 'eve@example.com', '567-543-2109', '202 Parkway, City E');



INSERT INTO "ORDER" (cu_id, or_date, total_amount, payment_status, is_canceled) 
VALUES 
(1, '2024-12-01', 150.00, 'Pending', FALSE),
(2, '2024-12-05', 220.00, 'Completed', FALSE),
(3, '2024-12-07', 80.00, 'Pending', FALSE),
(4, '2024-12-10', 300.00, 'Completed', FALSE),
(5, '2024-12-12', 100.00, 'Pending', TRUE);


INSERT INTO ORDER_DETAIL (or_id, t_id, quantity, subtotal) 
VALUES 
(1, 1, 1, 100.00),
(1, 2, 1, 50.00),
(2, 3, 1, 120.00),
(2, 4, 1, 60.00),
(3, 5, 1, 80.00),
(4, 6, 2, 160.00),
(4, 7, 1, 20.00),
(5, 8, 1, 70.00),
(5, 9, 1, 30.00);


INSERT INTO PAYMENT (or_id, payment_method, payment_datetime, amount) 
VALUES 
(1, 'Credit Card', '2024-12-01 15:00:00', 150.00),
(2, 'PayPal', '2024-12-05 17:30:00', 220.00),
(3, 'Credit Card', '2024-12-07 14:00:00', 80.00),
(4, 'Bank Transfer', '2024-12-10 18:45:00', 300.00),
(5, 'PayPal', '2024-12-12 13:15:00', 100.00);


INSERT INTO VENUE (v_name, address, capacity, contact_info) 
VALUES 
('Stadium A', '123 Stadium Rd, City A', 5000, '123-456-7890'),
('Stadium B', '456 Arena St, City B', 3000, '234-567-8901'),
('Theater C', '789 Broadway Ave, City C', 1000, '345-678-9012'),
('Gallery D', '101 Art St, City D', 500, '456-789-0123'),
('Comedy Club E', '202 Comedy Blvd, City E', 200, '567-890-1234');


INSERT INTO EVENT_VENUE (e_id, v_id, arrangement) 
VALUES 
(1, 1, 'Stage at center, VIP section in front'),
(2, 2, 'Football field, general seating in stands'),
(3, 3, 'Stage at center, audience seating around'),
(4, 4, 'Artworks displayed along walls'),
(5, 5, 'Stage at front, audience seating around');

-- select * from EVENT_VENUE;

-- -- 刪除所有資料表裡面的內容
-- TRUNCATE TABLE ORDER_DETAIL, PAYMENT, "ORDER", EVENT_VENUE, TICKET, EVENT, CUSTOMER, VENUE, ORGANIZER, CATEGORY RESTART IDENTITY CASCADE;


-- DO $$ 
-- BEGIN
--     -- 重置所有指定的序列
--     PERFORM setval('category_c_id_seq', 1, false);
--     PERFORM setval('organizer_o_id_seq', 1, false);
--     PERFORM setval('event_e_id_seq', 1, false);
--     PERFORM setval('ticket_t_id_seq', 1, false);
--     PERFORM setval('customer_cu_id_seq', 1, false);
--     PERFORM setval('"ORDER_or_id_seq"', 1, false);
--     PERFORM setval('payment_p_id_seq', 1, false);
--     PERFORM setval('venue_v_id_seq', 1, false);
-- END $$;
