The solution is a simple console program.

init.py creates the database and populates it with test data
    
    an optional argument can be provided to set the number of orders to be created, default value is 5000
        example: python init.py 1000000
    
    
erp.py contains functions for making queries:

    to list all products, use the 'lp' argument
        example: python erp.py lp

    to list orders, use the 'lo' argument with optional limit (default is 30)
        example: python erp.py lo 100

    to see a detailed view of an order, use the 'od' argument with order_id
        example: python erp.py od 123

    to see related product, use the 'rp' argument with order_id and product_id
        example: python erp.py rp 1 BT001

    to see an overview of data in the database, use the 'stats' argument
        example: python erp.py stats