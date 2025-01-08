from databaseFunctions import userLogin
from globalFunctions import *
from storefrontGUI import createStoreFront


def loginGUI():
    """
    This function creates the login window for the user to login
    """
    loginWindow = tk.Tk()
    loginWindow.title('Login')
    loginWindow.geometry('400x300')
    loginWindow.configure(background='white')

    tk.Label(loginWindow, text='Login', font=('Arial', 20, 'bold'), bg='white').pack(pady=20)

    labels = {
        'Email': tk.StringVar(),
        'Password': tk.StringVar()
    }

    createLabels(loginWindow, labels)

    def onLogin():
        hashPass = hashPassword(labels['Password'].get())
        user_ID = userLogin(labels['Email'].get(), hashPass)
        if user_ID:
            loginWindow.destroy()
            spawnNotification('Login Successful')

            cart = []
            createStoreFront(cart, user_ID)
        else:
            spawnError('Login Failed')

    loginButton = tk.Button(loginWindow, text='Login', command=onLogin, font=('Arial', 14, 'bold'), bg='blue', fg='white', bd=2, relief='solid')
    loginButton.pack(pady=20)

    loginWindow.mainloop()

