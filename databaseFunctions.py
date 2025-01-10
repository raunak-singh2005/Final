from globalFunctions import *
import sqlite3
from datetime import datetime
import sys


def initDB():

    # initialise Database Connection
    conn = sqlite3.connect('storeData.db')
    cursor = conn.cursor()
    return conn, cursor


def commitAndCloseDB(conn, cursor):

    # commit and close Database Connection
    conn.commit()
    cursor.close()
    conn.close()


def closeDB(conn, cursor):

    # close Database Connection
    cursor.close()
    conn.close()


def validateEmail(email):

    # validate email with regex
    if re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return True
    else:
        return False


def validatePassword(password):

    # validate password with regex
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
        return False
    else:
        return True


def validateAndTransformAge(DOB):

    # validate date of birth and transform to day, month, year
    try:
        birth_date = datetime.strptime(DOB, '%d/%m/%Y')
    except ValueError:
        # handle incorrect format
        spawnError('Date of birth must be in the format dd/mm/yyyy')
        sys.exit()

    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age >= 18:
        return int(birth_date.day), int(birth_date.month), int(birth_date.year)
    else:
        return None


def userLogin(email, passwordHash):

    # handle user login
    conn, cursor = initDB()

    searchUserDataTuple = (email, passwordHash)

    # sql command to fetch user id
    cursor.execute('SELECT User_ID FROM "main"."UserInformation" WHERE Email_Address = ? AND Password_Hash =?',
                   searchUserDataTuple)

    user_ID = cursor.fetchone()

    closeDB(conn, cursor)

    if user_ID is not None:
        print('User ID: ', user_ID[0])
        return user_ID[0]
    else:
        print('user not found')


def userSignup(userName, password, DOB, email, phoneNumber):

    try:
        # Input validation
        ageData = validateAndTransformAge(DOB)
        if ageData is None:
            spawnError('User must be over 18 years old')
            return False

        elif not validateEmail(email):
            spawnError('Email is invalid')
            return False

        elif validatePassword(password):
            spawnError('Password must be at least 8 characters long and contain at least one letter and one number')
            return False

        if checkSQLInjection(userName) or checkSQLInjection(password) or checkSQLInjection(DOB) or checkSQLInjection(email) or checkSQLInjection(phoneNumber):
            spawnError('invalid input')
            return False

        passwordHash = hashPassword(password)

        conn, cursor = initDB()

        searchUserDataTuple = (email,passwordHash)

        # sql command to check if user already exists
        cursor.execute('SELECT User_ID FROM "main"."UserInformation" WHERE Email_Address = ? AND Password_Hash =?',
                       searchUserDataTuple)
        user_id = cursor.fetchone()

        if user_id is not None:
            print('User already exists')
            closeDB(conn, cursor)
            return False

        elif len(phoneNumber) != 11:
            spawnError('Phone number must be 11 digits long')
            closeDB(conn, cursor)
            return False

        insertDataTuple = (userName, passwordHash, ageData[0], ageData[1], ageData[2], email, phoneNumber)

        # sql command to insert user data
        cursor.execute('INSERT INTO "main"."UserInformation"(User_ID, User_Name, Password_Hash, DOB_Day, DOB_Month, '
                       'DOB_Year, Email_Address, Phone_Number) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)', insertDataTuple)

        commitAndCloseDB(conn, cursor)

        print("User Created")
        spawnNotification('Signup Successful')
    except ValueError as e:
        # handle errors
        spawnError(f'Error: {str(e)}')
        sys.exit()


def getUserName(User_ID):

    conn, cursor = initDB()

    # sql command to fetch username
    cursor.execute('SELECT User_Name FROM "main"."UserInformation" WHERE User_ID = ?', (User_ID,))
    userName = cursor.fetchone()
    userName = userName[0]

    closeDB(conn, cursor)

    return userName


# def getDOB(user_ID):
#
# conn, cursor = initDB()
#
# # sql command to fetch date of birth
# cursor.execute('SELECT DOB_Day, DOB_Month, DOB_Year FROM "main"."UserInformation" WHERE User_ID = ?', (user_ID,))
# day,month,year = cursor.fetchone()
#
# day = day[0]
# month = month[0]
# year = year[0]
#
# closeDB(conn, cursor)
#
# return day, month, year


# def getEmail(User_ID):
#
#     conn, cursor = initDB()
#
#     # sql command to fetch email
#     cursor.execute('SELECT Email_Address FROM "main"."UserInformation" WHERE User_ID = ?', (User_ID,))
#     email = cursor.fetchone()
#
#     email = email[0]
#     closeDB(conn, cursor)
#
#     return email


# def getPhoneNumber(User_ID):
#
#     conn, cursor = initDB()
#
#     # sql command to fetch phone number
#     cursor.execute('SELECT Phone_Number FROM "main"."UserInformation" WHERE User_ID = ?', (User_ID,))
#     phoneNumber = cursor.fetchone()
#     phoneNumber = phoneNumber[0]
#     closeDB(conn, cursor)
#
#     return phoneNumber


def getProducts():

    conn, cursor = initDB()

    # sql command to fetch products
    cursor.execute('SELECT * FROM "main"."ProductInformation"')
    products = cursor.fetchall()

    closeDB(conn, cursor)

    return products


def getProductStock(productID):

    conn, cursor = initDB()

    # sql command to fetch product stock
    cursor.execute('SELECT Product_Quantity FROM "main"."ProductInformation" WHERE ProductID = ?', (productID,))
    stock = cursor.fetchone()
    closeDB(conn, cursor)
    return stock[0]


def updateProductStock(productID, quantity):

    conn, cursor = initDB()

    # sql command to update product stock
    cursor.execute('UPDATE "main"."ProductInformation" SET Product_Quantity = Product_Quantity - ? WHERE ProductID = ?', (quantity, productID))
    commitAndCloseDB(conn, cursor)


def placeOrder(userID, cart, total):

    # handle order placement
    conn, cursor = initDB()

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Convert cart list to a string
    # Convert cart list to a string of product IDs only
    cart_str = ','.join(str(item[0]) for item in cart)

    # sql command to insert order data
    cursor.execute('INSERT INTO "main"."Sales"(User_ID, Date, Items, Total_Price) VALUES (?, ?, ?, ?)', (userID, str(date), cart_str, total))

    commitAndCloseDB(conn, cursor)


testUsername = 'testUser'
testPassword = 'TestPass12'
testDOB = '09/10/2005'
testEmail = 'test@email.com'
testPhoneNumber = '0011233445'

userSignup(testUsername, testPassword, testDOB, testEmail, testPhoneNumber)




