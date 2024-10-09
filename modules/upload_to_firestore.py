import firebase_admin
from firebase_admin import credentials, firestore
from scraper import get_movie_info

# Initialiser l'application Firebase
cred = credentials.Certificate("data/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

def upload_to_firestore(data):
    db = firestore.client()  # Utilise firestore.client() pour se connecter à Firestore
    collection_ref = db.collection('movies')

    for movie in data:
        collection_ref.add(movie)

    return "Données sauvegardées avec succès", 200

if __name__ == "__main__":
    url = 'https://www.allocine.fr/seance/salle_gen_csalle=W7201.html'  # Remplace par l'URL appropriée
    url = "https://www.allocine.fr/seance/salle_gen_csalle=P8501.html" #Cinéaste
    movies_info = get_movie_info(url)

    # Uploader les données dans Firestore
    upload_to_firestore(movies_info)
