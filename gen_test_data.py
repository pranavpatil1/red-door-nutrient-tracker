import argparse
import csv
import random

# # this will create a csv for the file provided
# parser = argparse.ArgumentParser(
#                     prog='gen_test_data.py')

# parser.add_argument('file_prefix', type=str, help="file to output to")           # positional argument

def get_bool(bias=0.7):
    return 1 if random.random() < bias else 0

# def get_name():
#     return f"{names.get_first_name()} {chr(ord('A') + round(random.random() * 26))} {names.get_last_name()}"

# args = parser.parse_args()

student_f = open("student.csv", "w", newline='')
community_mb_f = open("community_member.csv", "w", newline='')

names = ['hovik', 'pranav', 'nisha', 'john']

with open ("user.csv", "w", newline='') as uf:
    # create users
    writer = csv.writer(uf)
    student_wr = csv.writer(student_f)
    community_wr = csv.writer(community_mb_f)
    """
    uid                 INT PRIMARY KEY,
    full_name           VARCHAR(100) NOT NULL,
    dairy_allowed       TINYINT NOT NULL,
    gluten_allowed      TINYINT NOT NULL,
    seafood_allowed     TINYINT NOT NULL,
    meat_allowed        TINYINT NOT NULL
    """
    writer.writerow(["UID", "Full Name", "Dairy allowed", "Gluten allowed", "Seafood allowed", "Meat allowed"])
    student_wr.writerow(["UID", "Balance"])
    community_wr.writerow(["UID", "Credit Card Num", "Expiration Date", "Verification Code"])

    for i in range(4):
        uid=2150000+i
        writer.writerow([uid, names[i], get_bool(), get_bool(), get_bool(), get_bool(), names[i], 1 if i >= 2 else 0])
        if i == 0:
            community_wr.writerow([uid, "1111222233334444", "2026-12-01", "123"])
        else:
            student_wr.writerow([uid, 1000])

student_f.close()
community_mb_f.close()

menu_items = [
    ["Avocado Toast", 6.25],
    ["Caprese", 6.95],
    ["Daily Pasta", 8.95],
    ["Daily Pasta (no meat)", 7.95]
]

with open ("item.csv", "w", newline='') as uf:
    # create users
    writer = csv.writer(uf)
    """
    item_id         SERIAL PRIMARY KEY,
    item_name       VARCHAR(20) NOT NULL,
    price_usd       NUMERIC(6, 2) NOT NULL,   
    """
    writer.writerow(["Item Name", "Price (USD)"])

    for item in menu_items:
        writer.writerow(item)


orders = [
    [i+1, 2150000+(i%4), f"2023-03-15 12:{i+10}:01"] for i in range(30)
]

with open ("orders.csv", "w", newline='') as uf:
    # create users
    writer = csv.writer(uf)
    """
    order_id        SERIAL,
    uid             INT REFERENCES user(uid),
    order_time      TIMESTAMP NOT NULL, 
    """
    writer.writerow(["Order ID", "UID", "Order Time"])

    for item in orders:
        writer.writerow(item)

orders_items = []

for i in range(1, 11):
    orders_items.append([i, ((i-1)%4)+1])

for i in range(11, 31):
    if i % 2 == 0:
        orders_items.append([i, 1])
        orders_items.append([i, 3])
    else:
        orders_items.append([i, 2])
        orders_items.append([i, 4])


with open ("orders_items.csv", "w", newline='') as f:
    writer = csv.writer(f)
    """
    order_id        BIGINT UNSIGNED REFERENCES orders(order_id),
    item_id         BIGINT UNSIGNED REFERENCES item(item_id),
    """
    writer.writerow(["Order ID", "Item ID"])

    for item in orders_items:
        writer.writerow(item)

ingr_details = [
    [1, "Flour", 0, 10, 0, 0, 0, 10, 1, 0, 0, 0],
    [2, "Tomato", 1, 6, 0, 4, 0.5, 149, 0, 0, 0, 0],
    [3, "Bread", 0, 10, 0, 3, 0, 10, 1, 0, 0, 0],
    [4, "Avocado", 3, 13, 22, 1, 0, 201, 0, 0, 0, 0],
    [5, "Meatball", 12, 5, 20, 1, 0, 85, 0, 0, 0, 1]
]

with open ("ingr_details.csv", "w", newline='') as f:
    writer = csv.writer(f)
    """
    ingredient_id   SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(20) NOT NULL,
    protein         NUMERIC(6, 2) NOT NULL,
    carbs           NUMERIC(6, 2) NOT NULL,
    fats            NUMERIC(6, 2) NOT NULL,
    sugars          NUMERIC(6, 2) NOT NULL,
    hydration_idx   NUMERIC(2, 1) NOT NULL,
    per_amt         NUMERIC(6, 2) NOT NULL,
    has_gluten      TINYINT NOT NULL DEFAULT 0,
    has_dairy       TINYINT NOT NULL DEFAULT 0,
    has_seafood     TINYINT NOT NULL DEFAULT 0,
    has_meat        TINYINT NOT NULL DEFAULT 0
    """
    writer.writerow(["ID", "Ingredient Name", "Protein (g)", "Carbs (g)", 
        "Fats (g)", "Sugars (g)", "Hydration index (-1 to 1)", 
        "Per amount (g)", "Has gluten", "Has dairy", "Has seafood", 
        "Has meat"])

    for item in ingr_details:
        writer.writerow(item)


recipe = [
    [ # avocado toast
        [3, 76], # 2 slice bread
        [4, 50] # 1 avocado
    ],
    [ # caprese
        [3, 76], # 2 slice bread
        [2, 122] # 1 tomato
    ],
    [ # daily pasta
        [1, 90], # 3/4 cup flour
        [2, 122] # 1 tomato
    ],
    [ # daily pasta with meat
        [1, 90], # 3/4 cup flour
        [2, 122], # 1 tomato
        [5, 85] # 6 meatballs? idk I don't eat meat
    ]
]

with open ("recipe.csv", "w", newline='') as f:
    writer = csv.writer(f)
    """
    item_id         BIGINT UNSIGNED REFERENCES item(item_id),
    ingredient_id   BIGINT UNSIGNED REFERENCES ingr_details(ingredient_id),
    -- in grams
    amount          NUMERIC(6, 2) NOT NULL,
    """
    writer.writerow(["Item ID", "Ingredient ID", "Amount"])

    for i in range(len(recipe)):
        for item in recipe[i]:
            writer.writerow([i + 1, item[0], item[1]])