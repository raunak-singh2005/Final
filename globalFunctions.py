import tkinter as tk
import hashlib
from tkinter import messagebox
import re


def createLabels(window, labels):

    # Create labels and entry fields for each label
    for label in labels:
        tk.Label(window, text=label).pack()
        if label == 'Password' or label == 'Confirm Password':
            tk.Entry(window, textvariable=labels[label], show="*").pack()
        else:
            tk.Entry(window, textvariable=labels[label]).pack()


def hashPassword(password):

    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()


def spawnError(message):

    # Spawn an error message box
    messagebox.showerror('Error', message)


def spawnNotification(message):

    # Spawn a notification message box
    messagebox.showinfo('Notification', message)


def spawnWarning(message):

    # Spawn a warning message box
    messagebox.showwarning('Warning', message)


def checkSQLInjection(data):

    # Check for SQL injection using regex
    if re.match(r'[^a-zA-Z0-9\s@./]', data):
        return True
    else:
        return False