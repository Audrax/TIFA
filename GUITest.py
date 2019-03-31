#Written by Matthew (Audrax) Yam

import os
import base64
import tkinter as tk
import pickle
from tkinter import filedialog
from tkinter import ttk
from base64 import b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

backend = default_backend()
filePaths = []
fileNumber = 0

#Main Windows
main = tk.Tk()
main.title('TifaCrypt')
main.geometry('650x450')

#Left Frame
frame = tk.Frame(main)
frame.pack(side = 'left', expand = 'true', fill = 'both')

#Right Frame
rightFrame = tk.Frame(main)
rightFrame.pack(side='right', expand = 'true', fill = 'both')

#List Box
fileList = tk.Listbox(frame)
fileList.pack(padx = 10, pady = 10, expand = 'true', fill = 'both')

#File Select Window
def userContent():
    fileSelect = tk.Toplevel()
    fileSelect.withdraw()
    fileSelect.grab_set()
    file_path = filedialog.askopenfilenames(parent = fileSelect)
    fileSelect.grab_release()
    file_path_lst = fileSelect.tk.splitlist(file_path)
    filePaths.append(file_path_lst)
    print(filePaths)
    fileNumber = len(file_path_lst)
    #DEBUG
    #print(fileNumber)
    #DEBUG
    i = 0
    while (i != fileNumber):
        fileList.insert(i+1, file_path_lst[i])
        i = i+1
    fileList.pack()

#Encrypt Window
def fileEncrypt():
    fileOk = True
    encrypt = tk.Toplevel()
    encrypt.grab_set()
    encrypt.withdraw()
    fileSave = filedialog.asksaveasfilename(parent = encrypt, defaultextension = '.tfa')
    encrypt.grab_release()
    #Checks if name is OK
    if (fileSave == ''):
        fileOk = False
        fileCheck = tk.Toplevel()
        fileCheck.title('Error')
        fileCheck.geometry("%dx%d%+d%+d" % (200, 50, 200, 100))
        fileCheck.grab_set()
        fileWarn = tk.Label(fileCheck, text = 'You need to provide a valid name')
        fileWarn.pack()
        fileConfirm = tk.Button(fileCheck, text = 'Ok', command = fileCheck.destroy, width = 10)
        fileConfirm.pack()
    #Password Prompt Window
    if (fileOk == True):
        password = tk.Toplevel()
        password.title('Encrypt')
        password.geometry("%dx%d%+d%+d" % (325, 125, 200, 100))
        password.grab_set()
        passwordText = tk.Label(password, text = 'Password: ')
        passwordText.grid(padx = 10, pady = 10, row = 0, column = 0)
        #Password Show Button
        show = tk.IntVar()
        passwordShow = tk.Checkbutton(password, text = 'Show Password', variable = show)
        passwordShow.grid(row = 1, column = 0)
        if (show == 1):
            passwordPrompt = tk.Entry(password)
            passwordPrompt.grid(padx = 10, pady = 10, row = 0, column = 1)
        else:
            passwordPrompt = tk.Entry(password, show = '*')
            passwordPrompt.grid(padx = 10, pady = 10, row = 0, column = 1)
        passwordKey = passwordPrompt.get()
        #Password Ok Button
        passwordAccept = tk.Button(password, text = 'Ok', width = 10, command = password.destroy)
        passwordAccept.grid(padx = 10, pady = 20, row = 2, column = 1)
        progressBar = tk.ttk.Progressbar(password, orient = 'horizontal', length = 150, mode = 'determinate')
        progressBar.grid(padx = 10, pady = 20, row = 2, column = 0)
        #Encryption
        x = 0
        files = []
        passwordEncode = str.encode(passwordKey)
        salt = os.urandom(16)
        #DEBUG
        #print(salt)
        #DEBUG
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(passwordEncode))
        f = Fernet(key)
        encryptedFile = []
        while (x != fileNumber):
            files[x] = open(filePaths[x], 'rb')
            x = x + 1
            encryptedFile = f.encrypt(files[x])
            files.close()
        export = open(fileSave, 'wb')
        pickle.dump(encryptedFile, export)
        export.close()
    
#Buttons
add = tk.Button(rightFrame, text = 'Add', height = 2, command = userContent)
add.pack(padx = 10, pady = 5, fill = 'both')

remove = tk.Button(rightFrame, text = 'Remove', height = 2, command=lambda fileList=fileList: fileList.delete(tk.ANCHOR))
remove.pack(padx = 10, pady = 5, fill = 'both')

encrypt = tk.Button(rightFrame, text = 'Encrypt', height = 2, command = fileEncrypt)
encrypt.pack(padx = 10, pady = 5, fill = 'both')

decrypt = tk.Button(rightFrame, text = 'Decrypt', height = 2)
decrypt.pack(padx = 10, pady = 5, fill = 'both')

exitPrgm = tk.Button(rightFrame, text = 'Exit', height = 2, command = main.destroy)
exitPrgm.pack(padx = 10, pady = 5, fill = 'both')

main.mainloop()
