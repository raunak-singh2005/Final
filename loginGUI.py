from databaseFunctions import userLogin
from globalFunctions import *


def loginGUI():
    """
    This function creates the login window for the user to login
    """
    loginWindow = tk.Tk()
    loginWindow.title("Login")
    loginWindow.geometry("300x200")
    loginWindow.configure(background="white")

    labels = {
        'Email': tk.StringVar(),
        'Password': tk.StringVar()
    }

    createLabels(loginWindow, labels)

    def onLogin():
        loginWindow.destroy()
        hashPass = hashPassword(labels['Password'].get())
        userLogin(labels['Email'].get(), hashPass)
        spawnNotification("Login Successful")

    loginButton = tk.Button(loginWindow, text="Login", command=onLogin)
    loginButton.pack()

    loginWindow.mainloop()

loginGUI()