import argparse
import csv
import names
import random

"""
LOAD DATA LOCAL INFILE 'user.csv' INTO TABLE user
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'item.csv' INTO TABLE item
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS
(item_name, price_usd);

LOAD DATA LOCAL INFILE 'student.csv' INTO TABLE student
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'community_member.csv' INTO TABLE community_member
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;
"""

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
        writer.writerow([i, get_name(), get_bool(), get_bool(), get_bool(), get_bool(), 10000])
        if i < 2150000+2:
            community_wr.writerow([i, "1111222233334444", "2026-12-00"])
        elif i< 2150000+5:
            community_wr.writerow([i, None, None, None])
        else:
            student_wr.writerow([i, 1000])


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
