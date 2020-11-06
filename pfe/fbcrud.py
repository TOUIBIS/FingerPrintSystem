import pyrebase
config = {
  "apiKey": "AIzaSyC5BXaV2Xmz-AJg08kAMUXJGx82gEl_k6E",
  "authDomain": "fingerprinter-d905e.firebaseapp.com",
  "databaseURL": "https://fingerprinter-d905e.firebaseio.com",
  "storageBucket": "fingerprinter-d905e.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


data = {"name": "Mortimer 'Morty' Smith"}
db.child("Personnes").child("Morty").set(data)