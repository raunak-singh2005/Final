import sqlite3
import re
from datetime import datetime
import hashlib


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

    birth_date = datetime.strptime(DOB, '%d/%m/%Y')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age >= 18:
        return int(birth_date.day), int(birth_date.month), int(birth_date.year)
    else:
        return None


def hashPassword(password):
    """
    Hashes the password using SHA256
    :param password:
    :return: Hashed Password
    """

    return hashlib.sha256(password.encode()).hexdigest()


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

    ageData = validateAndTransformAge(DOB)
    if ageData is None:
        print('User is under 18')
        return False

    elif not validateEmail(email):
        print('Email is invalid')
        return False

    elif not validatePassword(password):
        print('Password is invalid')
        return False

    print('User data is valid')

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


def getUserName(user_ID):
    """
    Gets the username of the user
    :param user_ID:
    :return: Username
    """

    conn, cursor = initDB()

    cursor.execute('SELECT User_Name FROM "main"."UserInformation" WHERE User_ID = ?', user_ID)
    userName = cursor.fetchall()

    closeDB(conn, cursor)

    return userName


def getDOB(user_ID):
    """
    Gets the age of the user
    :param user_ID:
    :return: day, month, year
    """

    conn, cursor = initDB()

    cursor.execute('SELECT DOB_Day, DOB_Month, DOB_Year FROM "main"."UserInformation" WHERE User_ID = ?', user_ID)
    day,month,year = cursor.fetchall()

    closeDB(conn, cursor)

    return day, month, year


def getEmail(User_ID):
    """
    Gets the email of the user
    :param User_ID:
    :return: Email
    """

    conn, cursor = initDB()

    cursor.execute('SELECT Email_Address FROM "main"."UserInformation" WHERE User_ID = ?', User_ID)
    email = cursor.fetchall()

    closeDB(conn, cursor)

    return email


def getPhoneNumber(User_ID):
    """
    Gets the phone number of the user
    :param User_ID:
    :return: Phone Number
    """

    conn, cursor = initDB()

    cursor.execute('SELECT Phone_Number FROM "main"."UserInformation" WHERE User_ID = ?', User_ID)
    phoneNumber = cursor.fetchall()

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
