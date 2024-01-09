import pyrebase

config={
  "apiKey": "AIzaSyDXa_7INUUVwo34q0cA0Ob28TAac9iM9JA",
  "authDomain": "teste-2367e.firebaseapp.com",
  "databaseURL": "https://teste-2367e-default-rtdb.firebaseio.com",
  "projectId": "teste-2367e",
  "storageBucket": "teste-2367e.appspot.com",
  "messagingSenderId": "644658226299",
  "appId": "1:644658226299:web:6129dfabe1a3e26f40aede"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
