import random
from databaseFunctions import *


def addSampleProducts():
    conn, cursor = initDB()

    categories = ['Electronics', 'Clothing', 'Books', 'Toys', 'Food']


    for i in range(100):
        print(i)
        productName = i
        productPrice = round(random.uniform(10, 100), 2)
        productStock = random.randint(1, 50)
        productDescription = f'Description for Product {i}'

        cursor.execute('INSERT INTO "main"."ProductInformation" (Product_Name, Product_Price, Product_Quantity, Description, Category) VALUES (?, ?, ?, ?,?)', (productName, productPrice, productStock, productDescription, random.choice(categories)))

    commitAndCloseDB(conn, cursor)

addSampleProducts()