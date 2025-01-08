from globalFunctions import *
from loginGUI import loginGUI
from signupGUI import signupGUI


def initGUI():

    initWindow = tk.Tk()
    initWindow.title('Welcome')
    initWindow.geometry('400x300')
    initWindow.configure(background='white')

    tk.Label(initWindow, text='Welcome', font=('Arial', 20, 'bold'), bg='white').pack(pady=20)

    def onLogin():
        initWindow.destroy()
        userID = loginGUI()

    def onSignup():
        initWindow.destroy()
        signupGUI()

    buttonFrame = tk.Frame(initWindow, bg='white')
    buttonFrame.pack(pady=20)

    loginButton = tk.Button(buttonFrame, text='Login', command=onLogin, font=('Arial', 14, 'bold'), bg='blue', fg='white', bd=2, relief='solid')
    loginButton.pack(side='left', padx=10)

    signupButton = tk.Button(buttonFrame, text='Signup', command=onSignup, font=('Arial', 14, 'bold'), bg='green', fg='white', bd=2, relief='solid')
    signupButton.pack(side='right', padx=10)

    initWindow.mainloop()

