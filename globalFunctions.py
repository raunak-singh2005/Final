import tkinter as tk
import hashlib
from tkinter import messagebox


def createLabels(window, labels):
    """
    Create labels for the window
    :param window:
    :param labels:
    :return:
    """

    for label in labels:
        tk.Label(window, text=label).pack()
        if label == 'Password' or label == 'Confirm Password':
            tk.Entry(window, textvariable=labels[label], show="*").pack()
        else:
            tk.Entry(window, textvariable=labels[label]).pack()


def hashPassword(password):
    """
    Hashes the password using SHA256
    :param password:
    :return: Hashed Password
    """

    return hashlib.sha256(password.encode()).hexdigest()


def spawnError(message):
    """
    Spawn an error message box
    :param message:
    :return:
    """

    messagebox.showerror('Error', message)


def spawnNotification(message):
    """
    Spawn a notification message box
    :param message:
    :return:
    """

    messagebox.showinfo('Notification', message)

def spawnWarning(message):
    """
    Spawn a warning message box
    :param message:
    :return:
    """

    messagebox.showwarning('Warning', message)