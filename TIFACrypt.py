#Written by Matthew (Audrax) Yam

import os
import base64
import tkinter as tk
from tkinter import filedialog
from base64 import b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

backend = default_backend()

#Prompts for password
def userPassword():
    password = input("Provide a password: ")
    return password
#Prompts for content to be encrypted
def userContent():
    print("Select file(s): ")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames(parent=root,title='Choose file(s)')
    file_path_lst = root.tk.splitlist(file_path)
    #DEBUG
    #print(file_path_lst)
    #DEBUG
    return file_path_lst
#Prompts to either encrypt or decrypt
def userChoice():
    choice = input("Encrypt or Decrypt? ")
    if choice.lower() == "encrypt":
        encrypt = True
        return encrypt
    elif choice.lower() == "decrypt":
        encrypt = False
        return encrypt
    else:
        print("Value invalid, try again.")
        userChoice()
#Prompts for name of encrypted file
def fileName():
    name = input("Name for encrypted file: ")
    return name
def encrypt():
    directories = userContent()
    fileNumber = len(directories)
    #DEBUG
    #print(fileNumber)
    #DEBUG
    password = str.encode(userPassword())
    i = 0
    content = []
    while (i != fileNumber):
        file = open(directories[i], "rb")
        content.insert(i, file.read())
        file.close()
        i = i + 1
    deletePrompt = input("Do you wish to remove the original file? ")
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
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = []
    byteDirectories = []
    encDirectories = []
    buffer = b""
    x = 0
    name = fileName()
    while (x != fileNumber):
        token.insert(x, f.encrypt(content[x]))
        buffer = buffer + token[x]
        buffer = buffer + b"startdir"
        byteDirectories.insert(x, directories[x].encode(encoding='UTF-8'))
        encDirectories.insert(x, f.encrypt(byteDirectories[x]))
        buffer = buffer + encDirectories[x]
        buffer = buffer + b"enddir"
        x = x + 1
    file = open(name + ".tfa","wb")
    file.write(buffer)
    file.write(salt)
    file.close()
    #Not working properly?
    if deletePrompt.lower() == "yes":
        isFile = os.path.isfile(directory)
        isDir = os.path.isdir(directory)
        if isFile == True:
            os.remove(directory)
        elif isDir == True:
            shutil.rmtree(directory)
        else:
            print("Error, file not removable")
    input("Done! File " + name + " created")
    exit()
def decrypt():
    print("Select file: ")
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askopenfilename(parent=root,title='Choose file')
    if ".tfa" not in directory:
        print("Not a valid file!")
        decrypt()
    else:
        passwordInput = input("Enter password: ")
        passwordDecrypt = str.encode(passwordInput)
        #File Reading
        file = open(directory, "rb")
        content = file.read()
        file.close()
        #Gets salt from last 16 chars
        salt = content[-16:]
        #DEBUG
        #print(salt)
        #DEBUG
        #Gets content w/o salt
        noSalt = content[:-16]
        #Finds number of file(s)
        encLength = content.count(b"startdir")
        #DEBUG
        #print(noSalt.count(b"enddir"))
        #print (encLength)
        #DEBUG
        nameStartPosition = []
        nameEndPosition = []
        encNames = []
        tokens = []
        k = 0
        #Finds position of start and end name tags for file(s) and isloates name tags from tokens
        while (k != encLength):
            if k == 0:
                nameStartPosition.insert(k, noSalt.find(b"startdir", 0) + 8)
                nameEndPosition.insert(k, noSalt.find(b"enddir", 0))
                encNames.insert(k, noSalt[nameStartPosition[0]:nameEndPosition[0]])
                k = k + 1
            else:
                nameStartPosition.insert(k, noSalt.find(b"startdir", nameStartPosition[k - 1]) + 8)
                nameEndPosition.insert(k, noSalt.find(b"enddir", nameEndPosition[k - 1] + 6))
                encNames.insert(k, noSalt[nameStartPosition[k]:nameEndPosition[k]])
                k = k + 1
            #DEBUG
            print(encNames)
            print (nameStartPosition)
            print (nameEndPosition)
            #DEBUG
        #Finds tokens based on the location of the startdir and enddir tags
        k = 0
        while (k != encLength):
            if k == 0:
                tokens.insert(k, noSalt[:nameStartPosition[k]])
                k = k + 1
            else:
                tokens.insert(k, noSalt[nameEndPosition[k - 1] + 6:nameStartPosition[k]])
                k = k + 1
            #DEBUG
            #print(tokens)
            #DEBUG
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(passwordDecrypt))
        f = Fernet(key)
        e = 0
        results = []
        names = []
        while e != encLength:
            results.insert(e, f.decrypt(tokens[e]))
            names.insert(e, f.decrypt(encNames[e]))
            file = open(names[e], "wb")
            file.write(results[e])
            file.close()
            strName = names[e].decode(encoding='UTF-8')
            print("Done! File " + strName + " decrypted")
            e = e + 1
        input("Press Enter to exit...")
        exit()


#Encrypt Process
if userChoice() == True:
    encrypt()
#Decrypt process
else:
    decrypt()
