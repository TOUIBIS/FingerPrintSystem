from tkinter import *
from tkinter import messagebox
from fingerprint_simpletest import enroll_finger
from fingerprint_simpletest import getTempl
from fingerprint_simpletest import get_fingerprint
import adafruit_fingerprint
import pyrebase
import serial
import time
from datetime import date

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)



config = {
  "apiKey": "AIzaSyC5BXaV2Xmz-AJg08kAMUXJGx82gEl_k6E",
  "authDomain": "fingerprinter-d905e.firebaseapp.com",
  "databaseURL": "https://fingerprinter-d905e.firebaseio.com",
  "storageBucket": "fingerprinter-d905e.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)
today = date.today()
d3 = today.strftime("%m/%d/%y")+" "+ current_time
print("d3 =", d3 )
sarhadetailsliste = {"depart": d3,"idb": 1}
print(sarhadetailsliste)



def ajoutEmp():
    if nomArea.get()!= "" or matArea.get() != "":
        data = {"name" : nomArea.get()}
        db.child("Personnes/").child(matArea.get()).set(data)
        nomArea.delete(0,'end')
        matArea.delete(0,'end')
    else:
        messagebox.showinfo('Notice', 'Ajouter un nom et une matricule !')
        
def clicked():
    messagebox.showinfo('Ajout', 'Personne ajouté')
def clickedEmp():
    enroll_finger(int(matArea.get()))

def suppEmp():
    if matAreaS.get() != "":
        finger.delete_model(int(matAreaS.get()))
        db.child("Personnes/").child(matAreaS.get()).remove()
        matAreaS.delete(0,'end')
    else:
        messagebox.showinfo('Notice', 'Ajouter une matricule a supprimer !')
def pointerpd():
    x = 0
    x = get_fingerprint()
    print (x)
    if x != 0:
        
        Person = db.child("Personnes").child(x).child("name").get()
        #convertText = str(x) + " sami"
        ListeAppele.itemconfig(x-1,bg='green')
        sarhadetailsliste.update({x: Person.val() })
        print(sarhadetailsliste)
        messagebox.showinfo('Notice', 'Bien ajouté pour ce depart !')
    else:
        messagebox.showinfo('Notice', 'Essayer du nouveau !')

def validd():
    s = db.child("sarha/").get()
    print(len(s.val()))
    db.child("sarha/").child(len(s.val())).set(sarhadetailsliste)


while True:
    window = Tk()

    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()

    positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)

    window.title("Bateau 1")

    window.geometry("+{}+{}".format(positionRight, positionDown))
    #window.attributes('-fullscreen', True)

    ajoutP = Label(window, text="Ajout Personne", font=("Arial Blod",20))
    ajoutP.grid(column=1,row =0)

    suppP = Label(window, text="Supprimer", font=("Arial Blod",20))
    suppP.grid(column=3,row =0)


    nomL = Label(window, text="Nom :")
    nomArea = Entry(window)
    nomL.grid(column=0, row=1)
    nomArea.grid(column=1, row=1)


    matL = Label(window, text="Matricule :")
    matArea = Entry(window)
    matL.grid(column=0 ,row = 2)
    matArea.grid(column=1, row = 2)


    matLS = Label(window, text="Matricule :")
    matAreaS = Entry(window)
    matLS.grid(column=2 ,row = 2)
    matAreaS.grid(column=3, row = 2)

    suppbtn = Button(window, text="Supp Emprainte", command=suppEmp)
    suppbtn.grid(column=3, row=3)

    empbtn = Button(window, text="Enter Emprainte", command=clickedEmp)
    empbtn.grid(column=1, row=3)
            
    saveP = Button(window, text="Enregistrer", command=ajoutEmp)
    saveP.grid(column=0, row=4)


    fingerT = Label(window, text="Liste des ids :")
    fingerT.grid(column=0, row=5)

    Lbl = Listbox(window)
    
    for i in getTempl():
        user = db.child("Personnes").child(i).child("name").get()
        print(user.val())
        users= str(i) + " " + str(user.val())
        Lbl.insert(END,users)

    Lbl.grid(column=1, row=5)
    
    pointer = Button(window, text="Pointer", command=pointerpd)
    pointer.grid(column=2, row=5)
    
    ListeAppele = Listbox(window )
    for i in getTempl():
        user = db.child("Personnes").child(i).child("name").get()
        users= str(i) + " " + str(user.val())
        ListeAppele.insert("end",users)
        ListeAppele.itemconfig("end",bg='red')
    
    ListeAppele.grid(column=3, row=5)
    
    validerDepart = Button(window, text="Valider le depart", command=validd)
    validerDepart.grid(column=2, row=6)

    window.mainloop()
