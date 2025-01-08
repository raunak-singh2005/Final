from globalFunctions import *
from databaseFunctions import userSignup


def signupGUI():

    # initialise the signup GUI

    # function to handle signup
    def onSignup():
        # check if passwords match
        if labels['Password'].get() == labels['Confirm Password'].get():
            userSignup(labels['Username'].get(), labels['Password'].get(), labels['Date of Birth [dd/mm/yyyy]'].get(), labels['Email'].get(), labels['Phone Number'].get())
            signupWindow.destroy()
        else:
            # spawn an error message
            spawnError('Passwords do not match')

    # create the signup window
    signupWindow = tk.Tk()
    signupWindow.title('Signup')
    signupWindow.geometry('400x400')
    signupWindow.configure(background='white')

    tk.Label(signupWindow, text='Signup', font=('Arial', 20, 'bold'), bg='white').pack(pady=20)

    # dictionary to store labels and their respective values
    labels = {
        'Username': tk.StringVar(),
        'Password': tk.StringVar(),
        'Confirm Password': tk.StringVar(),
        'Date of Birth [dd/mm/yyyy]': tk.StringVar(),
        'Email': tk.StringVar(),
        'Phone Number': tk.StringVar()
    }

    createLabels(signupWindow, labels)

    # create a signup button
    signupButton = tk.Button(signupWindow, text='Signup', command=onSignup, font=('Arial', 14, 'bold'), bg='blue', fg='white', bd=2, relief='solid')
    signupButton.pack(pady=20)

    signupWindow.mainloop()

