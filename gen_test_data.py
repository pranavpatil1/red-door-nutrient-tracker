import argparse
import csv
import names
import random

# # this will create a csv for the file provided
# parser = argparse.ArgumentParser(
#                     prog='gen_test_data.py')

# parser.add_argument('file_prefix', type=str, help="file to output to")           # positional argument

def get_bool(bias=0.9):
    return 1 if random.random() < bias else 0

def get_name():
    return f"{names.get_first_name()} {chr(ord('A') + round(random.random() * 26))} {names.get_last_name()}"

# args = parser.parse_args()

student_f = open("student.csv", "w")
community_mb_f = open("community_member.csv", "w")

with open ("user.csv", "w") as uf:
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

    for i in range(2150000, 2150020):
        writer.writerow([i, get_name(), get_bool(), get_bool(), get_bool(), get_bool()])
        if i < 2150000+2:
            community_wr.writerow([i, "1111222233334444", "2026-12-01", "123"])
        else:
            student_wr.writerow([i, 1000])

student_f.close()
community_mb_f.close()

menu_items = [
    ["Avocado Toast", 6.25],
    ["Caprese", 6.95],
    ["Daily Pasta", 8.95],
    ["Daily Pasta (no meat)", 7.95]
]

with open ("item.csv", "w") as uf:
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
    [i+1, 2150000+i, f"2023-03-15 12:{i+10}:01"] for i in range(30)
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


with open ("orders_items.csv", "w") as f:
    writer = csv.writer(f)
    """
    order_id        BIGINT UNSIGNED REFERENCES orders(order_id),
    item_id         BIGINT UNSIGNED REFERENCES item(item_id),
    """
    writer.writerow(["Order ID", "Item ID"])

    for item in orders_items:
        writer.writerow(item)