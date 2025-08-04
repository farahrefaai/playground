
-- 1. Create the seat_booked table
CREATE TABLE seat_booked (
    seat_id INT PRIMARY KEY,
    customer_name VARCHAR(10),
    is_booked BOOLEAN DEFAULT FALSE
);

-- 2. Populate the table with 20 seats (all unbooked with null customer names)
-- Method 1: Manual INSERT
INSERT INTO seat_booked (seat_id, customer_name, is_booked) 
VALUES 
    (1, NULL, FALSE), (2, NULL, FALSE), (3, NULL, FALSE), (4, NULL, FALSE), (5, NULL, FALSE),
    (6, NULL, FALSE), (7, NULL, FALSE), (8, NULL, FALSE), (9, NULL, FALSE), (10, NULL, FALSE),
    (11, NULL, FALSE), (12, NULL, FALSE), (13, NULL, FALSE), (14, NULL, FALSE), (15, NULL, FALSE),
    (16, NULL, FALSE), (17, NULL, FALSE), (18, NULL, FALSE), (19, NULL, FALSE), (20, NULL, FALSE);
