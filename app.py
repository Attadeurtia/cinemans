from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('modules/data/firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def index():
    # Fetch data from Firestore
    docs = db.collection('movies').stream()
    data = [doc.to_dict() for doc in docs]

    # Pass data to the HTML template
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
