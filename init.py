import sqlite3
import random
from sys import argv

con = sqlite3.connect("erp.db")

# create schema
with open("schema.sql") as f:
    con.executescript(f.read())

# test data - products
product_attributes = [
    ["Television", "Radio", "Washing machine", "Blender", "Phone", "Toaster", "Camera"],
    ["Sony", "Samsung", "Philips", "Bosch", "Toschiba", "Pioneer", "NEC"],
    ["X9000", "GX2000", "Z900", "XT750"],
    ["red", "yellow", "orange", "pink"],
]

def word_generator(alphabets, previous_letters=[]):
    for letter in alphabets[0]:
        letters = previous_letters + [letter]
        if len(alphabets) == 1:
            yield " ".join(letters)
        else:
            for word in word_generator(alphabets[1:], letters):
                yield word

counts = {}                
for product_name in word_generator(product_attributes):
    id_prefix = "".join(e[0] for e in product_name.upper().split())
    if id_prefix in counts:
        counts[id_prefix] += 1
    else:
        counts[id_prefix] = 1
    num = str(counts[id_prefix])
    id = ''.join([id_prefix, "0" * (8 - len(id_prefix) - len(num)), num])
    con.execute("INSERT INTO Product (id, name) VALUES ('%s', '%s');" % (id, product_name))
    con.commit()

# test data - orders
n_orders = 5000
if len(argv) >= 2 and argv[1].isdigit():
    n_orders = int(argv[1])

for n in xrange(n_orders):
    cursor = con.cursor()
    cursor.execute("INSERT INTO SalesOrder DEFAULT VALUES")
    order_id = cursor.lastrowid
    cursor.execute("""SELECT id 
        FROM Product 
        WHERE id IN (
            SELECT id 
            FROM Product 
            ORDER BY RANDOM() 
            LIMIT %s
        )""" % random.randint(1, 30))
    products = cursor.fetchall()
    for product in products:
        qty = random.randint(1, 100)
        cursor.execute("""INSERT INTO OrderLine (salesOrder, product, quantity) 
            VALUES ({}, '{}', {})""".format(order_id, product[0], qty))
    con.commit()
con.close()