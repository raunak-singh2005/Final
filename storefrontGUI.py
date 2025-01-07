from globalFunctions import *
from databaseFunctions import getProducts
from databaseFunctions import getUserName
from databaseFunctions import getProductStock
from databaseFunctions import updateProductStock
from PIL import Image, ImageTk
import os
import sys


def viewDescription(description, productID):
    descriptionWindow = tk.Toplevel()
    descriptionWindow.title('Description')
    descriptionWindow.geometry('400x500')

    productImagePath = os.path.join('Images', f'{productID}.png')

    if os.path.exists(productImagePath):
        image = Image.open(productImagePath)
        image = image.resize((200, 200))
        productImage = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(descriptionWindow, image=productImage)
        imageLabel.image = productImage
        imageLabel.pack()

    tk.Label(descriptionWindow, text='description').pack()
    tk.Label(descriptionWindow, text=description, wraplength = 350, justify='left').pack()


def createStoreFront(cart, User_ID):

    userName = getUserName(User_ID)

    storefront = tk.Tk()
    storefront.title('Storefront')
    storefront.geometry('800x600')

    navFrame = tk.Frame(storefront, bg='black', height=50)
    navFrame.pack(fill='x')

    tk.Label(navFrame, text='Store Front').pack(side='left')
    tk.Label(navFrame, text='Welcome ' + userName).pack(side='right')

    searchFrame = tk.Frame(storefront, bg='white', height=50)
    searchFrame.pack(fill='x')

    searchVar = tk.StringVar()
    tk.Entry(searchFrame, textvariable=searchVar).pack(side='left')
    tk.Button(searchFrame, text='Search', command=lambda: searchProducts(searchVar.get())).pack(side='right')

    productFrame = tk.Frame(storefront, bg='white')
    productFrame.pack(fill='both', expand=True)

    canvas = tk.Canvas(productFrame, bg='white')
    scrollbar = tk.Scrollbar(productFrame, orient='vertical', command=canvas.yview)
    scrollableFrame = tk.Frame(canvas, bg='white')

    scrollableFrame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    canvas.create_window((0, 0), window=scrollableFrame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    imageRef = []

    def searchProducts(query):
        query = query.lower()
        filteredProducts = [product for product in getProducts() if query in product[1].lower()]
        displayProducts(filteredProducts)

    def displayProducts(products):
        for widget in scrollableFrame.winfo_children():
            widget.destroy()

        for i, product in enumerate(products):
            productID = product[0]
            productName = product[1]
            productPrice = product[2]
            productStock = product[3]
            productDescription = product[4]

            productImagePath = os.path.join('Images', str(productID) + '.png')

            productContainer = tk.Frame(scrollableFrame, bg='white')
            productContainer.grid(row=i // 3, column = i % 3, sticky='nsew')

            if os.path.exists(productImagePath):
                image = Image.open(productImagePath)
                image = image.resize((150,150))
                productImage = ImageTk.PhotoImage(image)
                imageLabel = tk.Label(productContainer,image=productImage)
                imageLabel.image = productImage
                imageLabel.pack()
                imageRef.append(productImage)

            else:
                tk.Label(productContainer, text='No Image').pack()

            tk.Label(productContainer, text=productName).pack()
            tk.Label(productContainer, text=f'£{productPrice}').pack()
            tk.Button(productContainer, text='Add to Cart', command=lambda p=product: addToCart(cart,p)).pack()
            tk.Button(productContainer, text='Description', command=lambda d=productDescription, pid=productID: viewDescription(d,pid)).pack()

    products = getProducts()
    displayProducts(products)

    tk.Button(storefront, text='Checkout', command=lambda c=cart: checkout(c)).pack()

    storefront.mainloop()


def addToCart(cart, item):
    productID = item[0]
    currentStock = getProductStock(productID)
    cartQuantity = sum(1 for i in cart if i[0] == productID)

    if cartQuantity < currentStock:
        cart.append(item)
        spawnNotification("Item added to cart")
    else:
        spawnWarning("Not enough stock available")


def checkout(cart):
    if not cart:
        spawnWarning("Cart is empty")
        return

    showCart(cart)


def showCart(cart):
    cartWindow = tk.Tk()
    cartWindow.title('Cart')
    cartWindow.geometry('800x600')

    tk.Label(cartWindow, text='Your Cart').pack()

    cartSummary = {}
    for item in cart:
        productID = item[0]
        if productID in cartSummary:
            cartSummary[productID]['quantity'] += 1
        else:
            cartSummary[productID] = {'product': item[1], 'price': item[2], 'quantity': 1}

    def updateCart():
        cartWindow.destroy()
        showCart(cart)

    def incrementQuantity(productID):
        currentStock = getProductStock(productID)
        cartQuantity = sum(1 for i in cart if i[0] == productID)

        if cartQuantity < currentStock:
            for item in cart:
                if item[0] == productID:
                    cart.append(item)
                    updateCart()
                    break
        else:
            spawnWarning("Not enough stock available")

    def decrementQuantity(productID):
        for item in cart:
            if item[0] == productID:
                cart.remove(item)
                updateCart()
                break

    def finalCheckout():
        for productID, details in cartSummary.items():
            quantity = details['quantity']
            currentStock = getProductStock(productID)

            if quantity > currentStock:
                spawnWarning(f"Not enough stock available for product ID {productID}")
                return

        for productID, details in cartSummary.items():
            quantity = details['quantity']
            updateProductStock(productID, quantity)

        total = sum([details['price'] * details['quantity'] for details in cartSummary.values()])
        spawnNotification(f'Total amount: £{total}')
        cart.clear()
        cartWindow.destroy()
        sys.exit()

    for _, (productID, details) in enumerate(cartSummary.items(), start=1):
        productName = details['product']
        productPrice = details['price']
        quantity = details['quantity']

        productContainer = tk.Frame(cartWindow)
        productContainer.pack()

        tk.Label(productContainer, text=productName).pack(side='left')
        tk.Label(productContainer, text=f'£{productPrice} x {quantity}').pack(side='left')
        tk.Button(productContainer, text='+', command=lambda pid=productID: incrementQuantity(pid)).pack(side='left')
        tk.Button(productContainer, text='-', command=lambda pid=productID: decrementQuantity(pid)).pack(side='left')

    total = sum([details['price'] * details['quantity'] for details in cartSummary.values()])
    totalFrame = tk.Frame(cartWindow, bd=1)
    totalFrame.pack(fill='x')

    tk.Label(totalFrame, text=f'Total: £{total}').pack(side='right')

    tk.Button(cartWindow, text='Checkout', command=finalCheckout).pack()


createStoreFront([], 3)