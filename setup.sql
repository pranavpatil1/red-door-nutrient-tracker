DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS ingr_details;
DROP TABLE IF EXISTS orders_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS community_member;
DROP TABLE IF EXISTS user;

-- a user, identified by uid, and any allergens they have
CREATE TABLE user (
    uid                 INT PRIMARY KEY,
    full_name           VARCHAR(100) NOT NULL,
    dairy_allowed       TINYINT NOT NULL,
    gluten_allowed      TINYINT NOT NULL,
    seafood_allowed     TINYINT NOT NULL,
    meat_allowed        TINYINT NOT NULL
);

-- community members can optionally store
-- credit card information with us
CREATE TABLE community_member (
    uid                 INT PRIMARY KEY,
    credit_card_num     CHAR (16),
    expiration_date     DATE,
    verification_code   CHAR(3),
    FOREIGN KEY (uid) REFERENCES user(uid) 
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- students have a declining balance, usually 10000 for anytime
CREATE TABLE student (
    uid                 INT PRIMARY KEY,
    balance             NUMERIC(7, 2) NOT NULL DEFAULT 10000,
    FOREIGN KEY (uid) REFERENCES user(uid) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK (balance >= 0)
);

-- a menu item and its price
CREATE TABLE item (
    item_id         SERIAL PRIMARY KEY,
    item_name       VARCHAR(40) NOT NULL,
    price_usd       NUMERIC(6, 2) NOT NULL,
    UNIQUE (item_name),
    CHECK (price_usd >= 0)
);

-- an order, which may contain multiple food items
CREATE TABLE orders (
    order_id        SERIAL,
    uid             INT REFERENCES user(uid),
    order_time      TIMESTAMP NOT NULL,
    PRIMARY KEY (order_id),
    UNIQUE (order_time, uid)
);

-- creates a mapping between which items are in each order
-- can't enforce that this exists for each order, so empty 
-- order is technically possible
CREATE TABLE orders_items (
    order_id        BIGINT UNSIGNED REFERENCES orders(order_id),
    item_id         BIGINT UNSIGNED REFERENCES item(item_id),
    PRIMARY KEY (order_id, item_id)
);

-- for an ingredient, such as tomatoes or rice
-- include relevant information such as
CREATE TABLE ingr_details (
    ingredient_id   SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(20) NOT NULL,
    -- macros in this ingredient (grams)
    protein         NUMERIC(6, 2) NOT NULL,
    carbs           NUMERIC(6, 2) NOT NULL,
    fats            NUMERIC(6, 2) NOT NULL,
    sugars          NUMERIC(6, 2) NOT NULL,
    -- water is hydrating (+1), tea is slightly less (0.8)
    -- coffee is dehydrating (-0.5)
    hydration_idx   NUMERIC(2, 1) NOT NULL,
    -- how much of this ingredient we measured for (e.g. 100g of carrots)
    -- units grams
    per_amt         NUMERIC(6, 2) NOT NULL,
    -- booleans for allergens
    has_gluten      TINYINT NOT NULL DEFAULT 0,
    has_dairy       TINYINT NOT NULL DEFAULT 0,
    has_seafood     TINYINT NOT NULL DEFAULT 0,
    has_meat        TINYINT NOT NULL DEFAULT 0,
    UNIQUE (ingredient_name),
    -- non-negative values for macros
    CHECK (protein >= 0),
    CHECK (carbs >= 0),
    CHECK (fats >= 0),
    CHECK (sugars >= 0),
    -- between -1 and 1
    CHECK (hydration_idx >= -1),
    CHECK (hydration_idx <= 1)
);


-- stores how much of each ingredient is in each item
-- similar problem to above where we can't enforce many-to-many
CREATE TABLE recipe (
    item_id         BIGINT UNSIGNED REFERENCES item(item_id),
    ingredient_id   BIGINT UNSIGNED REFERENCES ingr_details(ingredient_id),
    -- in grams
    amount          NUMERIC(6, 2) NOT NULL,
    PRIMARY KEY (item_id, ingredient_id)
);
