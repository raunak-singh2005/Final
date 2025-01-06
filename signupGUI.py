from globalFunctions import *
from databaseFunctions import userSignup


def signupGUI():
    signupWindow = tk.Tk()
    signupWindow.title("Signup")
    signupWindow.geometry("300x320")
    signupWindow.resizable(False, False)

    labels = {
        'Username': tk.StringVar(),
        'Password': tk.StringVar(),
        'Confirm Password': tk.StringVar(),
        'Date of Birth': tk.StringVar(),
        'Email': tk.StringVar(),
        'Phone Number': tk.StringVar()
    }

    createLabels(signupWindow, labels)

    def onSignup():
        signupWindow.destroy()
        if labels['Password'].get() == labels['Confirm Password'].get():
            userSignup(labels['Username'].get(), labels['Password'].get(), labels['Date of Birth'].get(), labels['Email'].get(), labels['Phone Number'].get())
            spawnNotification("Signup Successful")
        else:
            spawnError("Passwords do not match")

    signupButton = tk.Button(signupWindow, text="Signup", command=onSignup)
    signupButton.pack()

    signupWindow.mainloop()

signupGUI()