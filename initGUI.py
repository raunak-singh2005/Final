from globalFunctions import *
from loginGUI import loginGUI
from signupGUI import signupGUI


def initGUI():
    """
    This function creates the initial window for the user to either login or signup
    """

    initWindow = tk.Tk()
    initWindow.title("Login")
    initWindow.geometry("300x200")
    initWindow.configure(background="white")

    def onLogin():
        initWindow.destroy()
        loginGUI()

    def onSignup():
        initWindow.destroy()
        signupGUI()

    loginButton = tk.Button(initWindow, text="Login", command=onLogin)
    loginButton.pack()

    signupButton = tk.Button(initWindow, text="Signup", command=onSignup)
    signupButton.pack()

    initWindow.mainloop()
