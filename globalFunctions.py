import tkinter as tk
import hashlib
from tkinter import messagebox
import re


def createLabels(window, labels):

    for label in labels:
        tk.Label(window, text=label).pack()
        if label == 'Password' or label == 'Confirm Password':
            tk.Entry(window, textvariable=labels[label], show="*").pack()
        else:
            tk.Entry(window, textvariable=labels[label]).pack()


def hashPassword(password):

    return hashlib.sha256(password.encode()).hexdigest()


def spawnError(message):

    messagebox.showerror('Error', message)


def spawnNotification(message):

    messagebox.showinfo('Notification', message)


def spawnWarning(message):

    messagebox.showwarning('Warning', message)


def checkSQLInjection(data):

    if re.match(r'[^a-zA-Z0-9\s@./]', data):
        return True
    else:
        return False