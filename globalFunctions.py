import tkinter as tk
from tkinter import ttk
import hashlib
from tkinter import messagebox
import re


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


def checkSQLInjection(data):
    """
    Checks for SQL Injection
    :param data:
    :return: Boolean
    """

    if re.match(r'[^a-zA-Z0-9\s@./]', data):
        return True
    else:
        return False