-- What are the food items, ordered by how often I order them (decreasing)? 
-- This is important for making a front-end that is customizable and has 
-- the most common items appearing first. we also want to include
-- items that were never ordered. so we add one of each order
-- NOTE: LEFT join is preserving the order here.

-- get the appropriate values we actually want
SELECT item_id, item_name, price_usd FROM
(
    -- on the combined values, count them and sort
    SELECT item_id, COUNT(item_id)-1 AS num FROM
    (
        -- this gets the items in order of orders
        SELECT item_id 
        FROM orders NATURAL JOIN user NATURAL JOIN orders_items 
        WHERE username='pranav'
            UNION ALL 
        -- this adds an element for each item on menu
        SELECT item_id FROM item
    ) AS temp
    GROUP BY item_id
    ORDER BY num DESC
) AS or_items NATURAL LEFT JOIN item;

-- What price was order 13 after tax?
SELECT ROUND(SUM(price_usd)*1.1, 2) AS final_price 
FROM orders NATURAL JOIN orders_items NATURAL JOIN item 
WHERE order_id=13;

-- what nutrients did I get from order 13?


-- what are the total nutrients I got today?
