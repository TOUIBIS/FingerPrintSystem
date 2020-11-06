from firebase import firebase
firebase = firebase.FirebaseApplication('https://fingerprinter-d905e.firebaseio.com/', None)
result = firebase.put('/Personnes',"idP",123)
#print result

