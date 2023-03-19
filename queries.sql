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

-- what nutrients exist in order 13?
SELECT  SUM(protein_in_item(item_id)) AS total_protein,
        SUM(carbs_in_item(item_id)) AS total_carbs,
        SUM(fats_in_item(item_id)) AS total_fats,
        SUM(sugars_in_item(item_id)) AS total_sugars
FROM orders_items 
WHERE order_id = 13;
        
-- what are the total nutrients I got today?
SELECT SUM(protein_in_item(item_id)) AS total_protein,
        SUM(carbs_in_item(item_id)) AS total_carbs,
        SUM(fats_in_item(item_id)) AS total_fats,
        SUM(sugars_in_item(item_id)) AS total_sugars
FROM    (SELECT item_id
        FROM orders_items NATURAL JOIN (SELECT order_id 
                                        FROM orders 
                                        WHERE DATE(order_time) = CURDATE() and username='pranav') 
                                        AS temp1) 
        AS temp2;

-- which items have gluten? (easily expanded to other allergens)
SELECT item_name 
FROM item NATURAL JOIN recipe NATURAL JOIN (
    SELECT ingredient_id FROM ingr_details WHERE has_gluten = 1
) as temp1;

-- who is red door's most loyal customer? (who ordered the most)
SELECT username, COUNT(*) AS num_orders 
FROM orders NATURAL JOIN user 
GROUP BY uid
-- compare each of the orders to the max, list those that are equal
HAVING COUNT(*) = (
    -- find out the maximum number of orders
    SELECT MAX(num_orders) AS max_orders
    FROM (
        SELECT COUNT(*) AS num_orders 
        FROM orders NATURAL JOIN user 
        GROUP BY uid
    ) AS temp1
);