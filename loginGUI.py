from databaseFunctions import userLogin
from globalFunctions import *
from storefrontGUI import createStoreFront


def loginGUI():

    # initialise the login GUI

    # function to handle login
    def onLogin():
        # hash the password
        hashPass = hashPassword(labels['Password'].get())
        user_ID = userLogin(labels['Email'].get(), hashPass)
        if user_ID:
            # close the login window
            loginWindow.destroy()
            spawnNotification('Login Successful')
            # create the storefront
            cart = []
            createStoreFront(cart, user_ID)
        else:
            # spawn an error message
            spawnError('Login Failed')

    # create the login window
    loginWindow = tk.Tk()
    loginWindow.title('Login')
    loginWindow.geometry('400x300')
    loginWindow.configure(background='white')

    tk.Label(loginWindow, text='Login', font=('Arial', 20, 'bold'), bg='white').pack(pady=20)

    # dictionary to store labels and their respective values
    labels = {
        'Email': tk.StringVar(),
        'Password': tk.StringVar()
    }

    createLabels(loginWindow, labels)

    # create a login button
    loginButton = tk.Button(loginWindow, text='Login', command=onLogin, font=('Arial', 14, 'bold'), bg='blue', fg='white', bd=2, relief='solid')
    loginButton.pack(pady=20)

    loginWindow.mainloop()

