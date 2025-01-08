from globalFunctions import *
import sqlite3
from datetime import datetime
import sys


def initDB():
    """
    Initializes the Database Connection and Cursor
    :return: conn, cursor
    """

    conn = sqlite3.connect('storeData.db')
    cursor = conn.cursor()
    return conn, cursor


def commitAndCloseDB(conn, cursor):
    """
    Commits and Closes the Connection and Cursor
    :param conn:
    :param cursor:
    """

    conn.commit()
    cursor.close()
    conn.close()


def closeDB(conn, cursor):
    """
    Closes the Connection and Cursor
    :param conn:
    :param cursor:
    """

    cursor.close()
    conn.close()


def validateEmail(email):
    """
    Validates the Email
    :param email:
    :return: Boolean
    """

    if re.match(r'[^@]+@[^@]+\.[^@]+', email):
        return True
    else:
        return False


def validatePassword(password):
    """
    Validates the Password
    :param password:
    :return: Boolean
    """

    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
        return False
    else:
        return True


def validateAndTransformAge(DOB):
    """
    Validates if the date of birth is over 18 years old and separates the day, month, and year.
    :param DOB: Date of birth in the format dd/mm/yyyy
    :return: Tuple (day, month, year) if valid, otherwise None
    """
    try:
        birth_date = datetime.strptime(DOB, '%d/%m/%Y')
    except ValueError:
        spawnError('Date of birth must be in the format dd/mm/yyyy')
        sys.exit()

    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age >= 18:
        return int(birth_date.day), int(birth_date.month), int(birth_date.year)
    else:
        return None


def userLogin(email, passwordHash):
    """
    Checks if the user exists in the database
    :param email:
    :param passwordHash:
    :return: User_ID if found, otherwise None
    """

    conn, cursor = initDB()

    searchUserDataTuple = (email, passwordHash)
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
    """
    Signs up the user if the data is valid
    :param userName:
    :param password:
    :param DOB:
    :param email:
    :param phoneNumber:
    :return: Boolean if validation failure
    """
    try:
        ageData = validateAndTransformAge(DOB)
        if ageData is None:
            spawnError('User must be over 18 years old')
            return False

        elif not validateEmail(email):
            spawnError('Email is invalid')
            return False

        elif not validatePassword(password):
            spawnError('Password must be at least 8 characters long and contain at least one letter and one number')
            return False

        if checkSQLInjection(userName) or checkSQLInjection(password) or checkSQLInjection(DOB) or checkSQLInjection(email) or checkSQLInjection(phoneNumber):
            spawnError('invalid input')
            return False

        passwordHash = hashPassword(password)

        conn, cursor = initDB()

        searchUserDataTuple = (email,passwordHash)
        cursor.execute('SELECT User_ID FROM "main"."UserInformation" WHERE Email_Address = ? AND Password_Hash =?',
                       searchUserDataTuple)
        user_id = cursor.fetchone()

        if user_id is not None:
            print('User already exists')
            closeDB(conn, cursor)
            return False

        insertDataTuple = (userName, passwordHash, ageData[0], ageData[1], ageData[2], email, phoneNumber)
        cursor.execute('INSERT INTO "main"."UserInformation"(User_ID, User_Name, Password_Hash, DOB_Day, DOB_Month, '
                       'DOB_Year, Email_Address, Phone_Number) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)', insertDataTuple)

        commitAndCloseDB(conn, cursor)

        print("User Created")
        spawnNotification('Signup Successful')
    except ValueError as e:
        spawnError(f'Error: {str(e)}')
        sys.exit()


def getUserName(User_ID):
    """
    Gets the username of the user
    :param User_ID:
    :return: Username
    """

    conn, cursor = initDB()

    cursor.execute('SELECT User_Name FROM "main"."UserInformation" WHERE User_ID = ?', (User_ID,))
    userName = cursor.fetchone()
    userName = userName[0]

    closeDB(conn, cursor)

    return userName


def getDOB(user_ID):
    """
    Gets the age of the user
    :param user_ID:
    :return: day, month, year
    """

    conn, cursor = initDB()

    cursor.execute('SELECT DOB_Day, DOB_Month, DOB_Year FROM "main"."UserInformation" WHERE User_ID = ?', (user_ID,))
    day,month,year = cursor.fetchone()

    day = day[0]
    month = month[0]
    year = year[0]

    closeDB(conn, cursor)

    return day, month, year


def getEmail(User_ID):
    """
    Gets the email of the user
    :param User_ID:
    :return: Email
    """

    conn, cursor = initDB()

    cursor.execute('SELECT Email_Address FROM "main"."UserInformation" WHERE User_ID = ?', (User_ID,))
    email = cursor.fetchone()

    email = email[0]
    closeDB(conn, cursor)

    return email


def getPhoneNumber(User_ID):
    """
    Gets the phone number of the user
    :param User_ID:
    :return: Phone Number
    """

    conn, cursor = initDB()

    cursor.execute('SELECT Phone_Number FROM "main"."UserInformation" WHERE User_ID = ?', (User_ID,))
    phoneNumber = cursor.fetchone()
    phoneNumber = phoneNumber[0]
    closeDB(conn, cursor)

    return phoneNumber


def getProducts():
    """
    Gets the products from the database
    :return: products
    """

    conn, cursor = initDB()
    cursor.execute('SELECT * FROM "main"."ProductInformation"')
    products = cursor.fetchall()

    closeDB(conn, cursor)

    return products


def getProductStock(productID):
    """
    Gets the stock of a product from the database
    :param productID:
    :return: stock
    """
    conn, cursor = initDB()
    cursor.execute('SELECT Product_Quantity FROM "main"."ProductInformation" WHERE ProductID = ?', (productID,))
    stock = cursor.fetchone()
    closeDB(conn, cursor)
    return stock[0]


def updateProductStock(productID, quantity):
    """
    Updates the stock of a product in the database
    :param productID:
    :param quantity:
    """
    conn, cursor = initDB()
    cursor.execute('UPDATE "main"."ProductInformation" SET Product_Quantity = Product_Quantity - ? WHERE ProductID = ?', (quantity, productID))
    commitAndCloseDB(conn, cursor)
