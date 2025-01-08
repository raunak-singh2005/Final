from globalFunctions import *
from databaseFunctions import getProducts
from databaseFunctions import getUserName
from databaseFunctions import getProductStock
from databaseFunctions import updateProductStock
from databaseFunctions import placeOrder
from PIL import Image, ImageTk
import os
import sys


def viewDescription(description, productID):

    # Function to display the description of a product
    descriptionWindow = tk.Toplevel()
    descriptionWindow.title('Description')
    descriptionWindow.geometry('400x500')

    # Get the image path
    productImagePath = os.path.join('Images', f'{productID}.jpeg')

    # Display the image
    if os.path.exists(productImagePath):
        image = Image.open(productImagePath)
        image = image.resize((200, 200))
        productImage = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(descriptionWindow, image=productImage)
        imageLabel.image = productImage
        imageLabel.pack()

    # Display the description
    tk.Label(descriptionWindow, text='Description:').pack()
    tk.Label(descriptionWindow, text=description, wraplength = 350, justify='left').pack()
    tk.Button(descriptionWindow, text='Close', command=descriptionWindow.destroy).pack()


def createStoreFront(cart, User_ID):

    # Function to create the storefront

    def searchProducts(query='', category=None):

        # Function to search for products
        query = query.lower()

        # Filter products based on search query
        if category:
            filteredProducts = [product for product in getProducts() if category.lower() in product[5].lower()]
        else:
            # Filter products based on search query
            filteredProducts = [product for product in getProducts() if
                                query in product[1].lower() or query in product[5].lower()]
        displayProducts(filteredProducts)

    def displayProducts(products):

        # Function to display products
        for widget in scrollableFrame.winfo_children():
            widget.destroy()

        # Enumerate through the products
        for i, product in enumerate(products):
            # Get the product details
            productID = product[0]
            productName = product[1]
            productPrice = product[2]
            productDescription = product[4]

            # Get the image path
            productImagePath = os.path.join('Images', str(productID) + '.jpeg')

            # Create the product container
            productContainer = tk.Frame(scrollableFrame, bg='white', padx=10, pady=10, bd=1, relief='solid')
            productContainer.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky='nsew')

            # Display the product image
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

            # Display the product details
            tk.Label(productContainer, text=productName, font=('Arial', 12, 'bold')).pack(pady=5)
            tk.Label(productContainer, text=f'£{productPrice}', font=('Arial', 10)).pack(pady=5)
            tk.Button(productContainer, text='Add to Cart', command=lambda p=product: addToCart(cart, p)).pack(pady=5)
            tk.Button(productContainer, text='Description',
                      command=lambda d=productDescription, pid=productID: viewDescription(d, pid)).pack()

    def clearSearch():

        # Function to clear the search bar
        searchVar.set('')
        displayProducts(getProducts())

    userName = getUserName(User_ID)

    # Create the storefront window
    storefront = tk.Tk()
    storefront.title('Storefront')
    storefront.geometry('910x600')

    # Create the navigation bar
    navFrame = tk.Frame(storefront, bg='black', height=50, padx=10)
    navFrame.pack(fill='x')

    # Display the store front and the user name
    tk.Label(navFrame, text='Store Front', fg='white', bg='black', font=('Arial', 14, 'bold')).pack(side='left')
    tk.Label(navFrame, text='Welcome ' + userName, fg='white', bg='black', font=('Arial', 12)).pack(side='right')

    # Create the search bar
    searchFrame = tk.Frame(storefront, bg='white', height=50, padx=10, pady=10)
    searchFrame.pack(fill='x')

    # Add search bar
    searchVar = tk.StringVar()
    tk.Entry(searchFrame, textvariable=searchVar, font=('Arial', 12), width=50).pack(side='left', padx=5)
    tk.Button(searchFrame, text='Search', command=lambda: searchProducts(searchVar.get()), font=('Arial', 12)).pack(side='right', padx=5)

    # Add category filter buttons
    categories = ['BMX', 'Mountain', 'Electric', 'Kids', 'Sports']
    for category in categories:
        tk.Button(searchFrame, text=category, command=lambda c=category: searchProducts('', c)).pack(side='left', padx=5)

    # Add clear button
    tk.Button(searchFrame, text='Clear', command=lambda: clearSearch(), font=('Arial', 12)).pack(side='left', padx=5)

    # Create the product frame
    productFrame = tk.Frame(storefront, bg='white')
    productFrame.pack(fill='both', expand=True)

    # Create the scrollable frame
    canvas = tk.Canvas(productFrame, bg='white')
    scrollbar = tk.Scrollbar(productFrame, orient='vertical', command=canvas.yview)
    scrollableFrame = tk.Frame(canvas, bg='white')

    # Bind the scrollable frame to the canvas
    scrollableFrame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create the window
    canvas.create_window((0, 0), window=scrollableFrame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    imageRef = []

    # Display the products
    products = getProducts()
    displayProducts(products)

    # Create the cart button
    tk.Button(storefront, text='Checkout', command=lambda c=cart, i=User_ID: checkout(i,c)).pack()

    storefront.mainloop()


def addToCart(cart, item):

    # Function to add an item to the cart
    productID = item[0]

    # Check if the product is in stock
    currentStock = getProductStock(productID)
    cartQuantity = sum(1 for i in cart if i[0] == productID)

    # Handle stock availability
    if cartQuantity < currentStock:
        cart.append(item)
        spawnNotification("Item added to cart")
    else:
        spawnWarning("Not enough stock available")


def checkout(userID, cart):

    # Function to initiate the checkout process
    if not cart:
        spawnWarning("Cart is empty")
        return

    showCart(userID, cart)


def showCart(userID, cart):

    # Function to display the cart

    def updateCart():

        # Function to update the cart window
        cartWindow.destroy()
        showCart(userID, cart)

    def incrementQuantity(productID):

        # Function to increment the quantity of a product in the cart
        currentStock = getProductStock(productID)
        cartQuantity = sum(1 for i in cart if i[0] == productID)

        # Handle stock availability
        if cartQuantity < currentStock:
            for item in cart:
                if item[0] == productID:
                    cart.append(item)
                    updateCart()
                    break
        else:
            spawnWarning("Not enough stock available")

    def decrementQuantity(productID):

        # Function to decrement the quantity of a product in the cart
        for item in cart:
            if item[0] == productID:
                cart.remove(item)
                updateCart()
                break

    def finalCheckout():

        # Function to finalise the checkout process
        # Get stock availability
        for productID, details in cartSummary.items():
            quantity = details['quantity']
            currentStock = getProductStock(productID)

            # Handle stock availability
            if quantity > currentStock:
                spawnWarning(f"Not enough stock available for product ID {productID}")
                return

        # Update the stock
        for productID, details in cartSummary.items():
            quantity = details['quantity']
            updateProductStock(productID, quantity)

        # Handle total math
        total = sum([details['price'] * details['quantity'] for details in cartSummary.values()])
        total = round(total, 2)

        # Display total
        spawnNotification(f'Total amount: £{total}')

        # Add Record to Sales Table
        placeOrder(userID, cart, total)
        cart.clear()
        cartWindow.destroy()
        sys.exit()

    # Create the cart window
    cartWindow = tk.Tk()
    cartWindow.title('Cart')
    cartWindow.geometry('800x600')

    tk.Label(cartWindow, text='Your Cart', font=('Arial', 16, 'bold')).pack(pady=10)

    # Create a dictionary to store the cart summary
    cartSummary = {}

    # Populate the cart summary
    for item in cart:
        productID = item[0]
        if productID in cartSummary:
            cartSummary[productID]['quantity'] += 1
        else:
            cartSummary[productID] = {'product': item[1], 'price': item[2], 'quantity': 1}

    # Display the cart summary
    for _, (productID, details) in enumerate(cartSummary.items(), start=1):
        # Get the product details
        productName = details['product']
        productPrice = details['price']
        quantity = details['quantity']

        # Create the product container
        productContainer = tk.Frame(cartWindow, bd=1, relief='solid', padx=10, pady=10)
        productContainer.pack(fill='x', pady=5)

        # Display the product details
        tk.Label(productContainer, text=productName, font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w')
        tk.Label(productContainer, text=f'£{productPrice} x {quantity}', font=('Arial', 12)).grid(row=0, column=1, sticky='e')
        tk.Button(productContainer, text='+', command=lambda pid=productID: incrementQuantity(pid)).grid(row=0, column=2, padx=5)
        tk.Button(productContainer, text='-', command=lambda pid=productID: decrementQuantity(pid)).grid(row=0, column=3, padx=5)
        tk.Button(productContainer, text='Remove', command=lambda pid=productID: decrementQuantity(pid)).grid(row=0, column=4, padx=5)

    # Total Math
    total = sum([details['price'] * details['quantity'] for details in cartSummary.values()])
    total = round(total, 2)

    # Create the total frame
    totalFrame = tk.Frame(cartWindow, bd=1, relief='solid', padx=10, pady=10)
    totalFrame.pack(fill='x', pady=10)

    # Display the total amount
    tk.Label(totalFrame, text=f'Total: £{total}', font=('Arial', 14, 'bold')).pack(side='right')

    tk.Button(cartWindow, text='Checkout', command=finalCheckout, font=('Arial', 12, 'bold')).pack(pady=10)

    cartWindow.mainloop()
