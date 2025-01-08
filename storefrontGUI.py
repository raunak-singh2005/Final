from globalFunctions import *
from databaseFunctions import getProducts
from databaseFunctions import getUserName
from databaseFunctions import getProductStock
from databaseFunctions import updateProductStock
from PIL import Image, ImageTk
import os
import sys


def viewDescription(description, productID):
    """
    This function creates a new window to display the description of the product
    :param description:
    :param productID:
    :return:
    """
    descriptionWindow = tk.Toplevel()
    descriptionWindow.title('Description')
    descriptionWindow.geometry('400x500')

    productImagePath = os.path.join('Images', f'{productID}.jpg')

    if os.path.exists(productImagePath):
        image = Image.open(productImagePath)
        image = image.resize((200, 200))
        productImage = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(descriptionWindow, image=productImage)
        imageLabel.image = productImage
        imageLabel.pack()

    tk.Label(descriptionWindow, text='description').pack()
    tk.Label(descriptionWindow, text=description, wraplength = 350, justify='left').pack()
    tk.Button(descriptionWindow, text='Close', command=descriptionWindow.destroy).pack()


def createStoreFront(cart, User_ID):
    """
    This function creates the storefront window
    :param cart:
    :param User_ID:
    :return:
    """
    userName = getUserName(User_ID)

    storefront = tk.Tk()
    storefront.title('Storefront')
    storefront.geometry('910x600')

    navFrame = tk.Frame(storefront, bg='black', height=50, padx=10)
    navFrame.pack(fill='x')

    tk.Label(navFrame, text='Store Front', fg='white', bg='black', font=('Arial', 14, 'bold')).pack(side='left')
    tk.Label(navFrame, text='Welcome ' + userName, fg='white', bg='black', font=('Arial', 12)).pack(side='right')

    searchFrame = tk.Frame(storefront, bg='white', height=50, padx=10, pady=10)
    searchFrame.pack(fill='x')

    searchVar = tk.StringVar()
    tk.Entry(searchFrame, textvariable=searchVar, font=('Arial', 12), width=50).pack(side='left', padx=5)
    tk.Button(searchFrame, text='Search', command=lambda: searchProducts(searchVar.get()), font=('Arial', 12)).pack(side='right', padx=5)

    # Add category filter buttons
    categories = ['Electronics', 'Clothing', 'Books', 'Toys', 'Food']
    for category in categories:
        tk.Button(searchFrame, text=category, command=lambda c=category: searchProducts('', c)).pack(side='left', padx=5)

    # Add clear button
    tk.Button(searchFrame, text='Clear', command=lambda: clearSearch(), font=('Arial', 12)).pack(side='left', padx=5)

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

    def searchProducts(query='', category=None):
        query = query.lower()
        if category:
            filteredProducts = [product for product in getProducts() if category.lower() in product[5].lower()]
        else:
            filteredProducts = [product for product in getProducts() if query in product[1].lower() or query in product[5].lower()]
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

            productImagePath = os.path.join('Images', str(productID) + '.jpg')

            productContainer = tk.Frame(scrollableFrame, bg='white', padx=10, pady=10, bd=1, relief='solid')
            productContainer.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky='nsew')

            if os.path.exists(productImagePath):
                image = Image.open(productImagePath)
                image = image.resize((150, 150))
                productImage = ImageTk.PhotoImage(image)
                imageLabel = tk.Label(productContainer, image=productImage)
                imageLabel.image = productImage
                imageLabel.pack(pady=5)
                imageRef.append(productImage)
            else:
                tk.Label(productContainer, text='No Image').pack(pady=5)

            tk.Label(productContainer, text=productName, font=('Arial', 12, 'bold')).pack(pady=5)
            tk.Label(productContainer, text=f'£{productPrice}', font=('Arial', 10)).pack(pady=5)
            tk.Button(productContainer, text='Add to Cart', command=lambda p=product: addToCart(cart, p)).pack(pady=5)
            tk.Button(productContainer, text='Description',
                      command=lambda d=productDescription, pid=productID: viewDescription(d, pid)).pack()

    def clearSearch():
        searchVar.set('')
        displayProducts(getProducts())

    products = getProducts()
    displayProducts(products)

    tk.Button(storefront, text='Checkout', command=lambda c=cart: checkout(c)).pack()

    storefront.mainloop()


def addToCart(cart, item):
    """
    This function adds an item to the cart
    :param cart:
    :param item:
    :return:
    """
    productID = item[0]
    currentStock = getProductStock(productID)
    cartQuantity = sum(1 for i in cart if i[0] == productID)

    if cartQuantity < currentStock:
        cart.append(item)
        spawnNotification("Item added to cart")
    else:
        spawnWarning("Not enough stock available")


def checkout(cart):
    """
    This function displays the cart and allows the user to checkout
    :param cart:
    :return:
    """
    if not cart:
        spawnWarning("Cart is empty")
        return

    showCart(cart)


def showCart(cart):
    """
    This function displays the cart
    :param cart:
    :return:
    """
    cartWindow = tk.Tk()
    cartWindow.title('Cart')
    cartWindow.geometry('800x600')

    tk.Label(cartWindow, text='Your Cart', font=('Arial', 16, 'bold')).pack(pady=10)

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
        total = round(total, 2)
        spawnNotification(f'Total amount: £{total}')
        cart.clear()
        cartWindow.destroy()
        sys.exit()

    for _, (productID, details) in enumerate(cartSummary.items(), start=1):
        productName = details['product']
        productPrice = details['price']
        quantity = details['quantity']

        productContainer = tk.Frame(cartWindow, bd=1, relief='solid', padx=10, pady=10)
        productContainer.pack(fill='x', pady=5)

        tk.Label(productContainer, text=productName, font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w')
        tk.Label(productContainer, text=f'£{productPrice} x {quantity}', font=('Arial', 12)).grid(row=0, column=1, sticky='e')
        tk.Button(productContainer, text='+', command=lambda pid=productID: incrementQuantity(pid)).grid(row=0, column=2, padx=5)
        tk.Button(productContainer, text='-', command=lambda pid=productID: decrementQuantity(pid)).grid(row=0, column=3, padx=5)
        tk.Button(productContainer, text='Remove', command=lambda pid=productID: decrementQuantity(pid)).grid(row=0, column=4, padx=5)

    total = sum([details['price'] * details['quantity'] for details in cartSummary.values()])
    total = round(total, 2)
    totalFrame = tk.Frame(cartWindow, bd=1, relief='solid', padx=10, pady=10)
    totalFrame.pack(fill='x', pady=10)

    tk.Label(totalFrame, text=f'Total: £{total}', font=('Arial', 14, 'bold')).pack(side='right')

    tk.Button(cartWindow, text='Checkout', command=finalCheckout, font=('Arial', 12, 'bold')).pack(pady=10)

    cartWindow.mainloop()
