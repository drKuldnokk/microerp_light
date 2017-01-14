import sqlite3
from sys import argv

def related_products(order_id, product_id):
    ''' related products (order_id, product_id) '''
    
    c = sqlite3.connect("erp.db")
    cursor = c.cursor()
    cursor.execute('''
        SELECT OL.product, P.name, TOTAL(quantity) AS popularity
        FROM OrderLine AS OL
        JOIN Product AS P
            on P.id = OL.product
        WHERE product in (SELECT product FROM OrderLine WHERE salesOrder = {})
            AND product <> '{}'
        GROUP BY OL.product, P.name
        ORDER BY popularity DESC;
        '''.format(order_id, product_id))
    print
    print "Listing related products for order id: {}, product id: {}".format(order_id, product_id)
    print 
    print '{:<20}{:<50}{:<10}'.format("ID", "NAME", "POPULARITY")
    print "-" * 80
    for product in cursor.fetchall():
        print '{:<20}{:<50}{:<10}'.format(product[0], product[1], product[2])
    print
    
    
def product_list():
    ''' all products ordered by popularity '''
    
    c = sqlite3.connect("erp.db")
    cursor = c.cursor()
    cursor.execute('''
        SELECT P.id, P.name, TOTAL(OL.quantity) AS popularity
        FROM Product AS P
        LEFT OUTER JOIN OrderLine AS OL 
            ON OL.product = P.id 
        GROUP BY P.id, P.name
        ORDER BY popularity DESC;
        ''')
    print
    print "Listing all products"
    print 
    print '{:<20}{:<50}{:<10}'.format("ID", "NAME", "POPULARITY")
    print "-" * 80
    for product in cursor.fetchall():
        print '{:<20}{:<50}{:<10}'.format(product[0], product[1], product[2])
    print
    
    
def order_list(limit):
    ''' all orders with line counts '''
    
    c = sqlite3.connect("erp.db")
    cursor = c.cursor()
    cursor.execute('''
        SELECT salesOrder, count(*) AS lineCount
        FROM OrderLine 
        GROUP BY salesOrder 
        ORDER BY RANDOM()
        LIMIT {};
        '''.format(limit))
    print
    print "Listing {} random orders".format(limit)
    print 
    print '{:<10}{:<10}'.format("ID", "LINES")
    print "-" * 80
    for product in cursor.fetchall():
        print '{:<10}{:<10}'.format(product[0], product[1])
    print
        
def order_detail(order_id):
    ''' detailed view of an order with lines '''
    
    c = sqlite3.connect("erp.db")
    cursor = c.cursor()
    cursor.execute("""
        SELECT P.id, P.name, OL.quantity
        FROM OrderLine AS OL
        JOIN Product AS P
            ON OL.product = P.id
        WHERE OL.salesOrder = '{}'
        """.format(order_id))
    print
    print "Order id: {}".format(order_id)
    print
    print "lines:"
    print '{:<20}{:<50}{:<10}'.format("PRODUCT", "NAME", "QUANTITY")
    print "-" * 80
    for line in cursor.fetchall():
        print '{:<20}{:<50}{:<10}'.format(line[0], line[1], line[2])
    print
    
def stats():
    '''database stats'''
    
    c = sqlite3.connect("erp.db")
    cursor = c.cursor()
    print
    print "database stats:"
    print
    
    cursor.execute("SELECT count(*) FROM Product")
    for stats in cursor.fetchall():
        print "    {} products".format(stats[0])
        
    cursor.execute("SELECT count(*) FROM SalesOrder")
    for stats in cursor.fetchall():
        print "    {} sales orders".format(stats[0])
        
    cursor.execute("SELECT count(*) FROM OrderLine")
    for stats in cursor.fetchall():
        print "    {} order lines".format(stats[0])
    print
    
def print_help():
    print
    print "-" * 80
    print
    print "to list all products, use the 'lp' argument"
    print "    ex: 'python erp.py lp'"
    print
    print "to list all orders, use the 'lo' argument with optional limit (default is 30)"
    print "    ex: 'python erp.py lo 100'"
    print
    print "to see a detailed view of an order, use the 'od' argument with order_id"
    print "    ex: 'python erp.py od 123'"
    print
    print "to see related products, use the 'rp' argument with order_id and product_id"
    print "    ex: 'python erp.py rp 1 BT001'"
    print
    print "to see an overview of data in the database, use the 'stats' argument"
    print "    ex: 'python erp.py stats'"
    print
    print "-" * 80
    print 
    
def handle_error(command):
    print "Incorrect arguments for command %s" % command
    print_help()
                
def main():
    if len(argv) >= 2:
        command = argv[1]
        if command == "rp":
            if len(argv) >= 4:
                related_products(order_id=argv[2], product_id=argv[3])
            else:
                handle_error(command)
        elif command == "lp":
            product_list()
        elif command == "lo":
            limit = 30
            if len(argv) >= 3 and argv[2].isdigit():
                limit = int(argv[2])
            order_list(limit)
        elif command == "od":
            if len(argv) >= 3:
                order_detail(order_id=argv[2])
            else:
                handle_error(command)
        elif command == "stats":
            stats()
        else:
            print_help()
    else:
        print_help()
    
main()