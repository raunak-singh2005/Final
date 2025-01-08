import random
from databaseFunctions import *


def addSampleProducts():
    conn, cursor = initDB()

    categories = ['BMX', 'Mountain', 'Electric', 'Kids', 'Sports']

    for i in range(50):
        print(i)
        productprefix = i+1
        productName = f'Product {productprefix}'
        productPrice = round(random.uniform(10, 100), 2)
        productStock = random.randint(1, 50)
        productDescription = f'Description for Product {i}'

        cursor.execute('INSERT INTO "main"."ProductInformation" (Product_Name, Product_Price, Product_Quantity, Description, Category) VALUES (?, ?, ?, ?,?)', (productName, productPrice, productStock, productDescription, random.choice(categories)))

    commitAndCloseDB(conn, cursor)

