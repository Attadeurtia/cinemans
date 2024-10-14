import firebase_admin
from firebase_admin import credentials, firestore
from scraper import get_movie_info, get_movie_info2

# Initialiser l'application Firebase
cred = credentials.Certificate("data/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)


def upload_to_firestore(data):
    db = firestore.client()  # Utilise firestore.client() pour se connecter à Firestore
    collection_ref = db.collection('movies')

    for movie in data:
        doc_ref = collection_ref.document(movie['id'])
        doc = doc_ref.get()
        if not doc.exists:
            doc_ref.set(movie)
        else:
            showtimes_and_versions = get_movie_info2(movie)
            doc_ref.update(showtimes_and_versions)

    return "Données sauvegardées avec succès", 200

if __name__ == "__main__":
    url = 'https://www.allocine.fr/seance/salle_gen_csalle=W7201.html'  # Remplace par l'URL appropriée
    url2 = "https://www.allocine.fr/seance/salle_gen_csalle=P8501.html" #Cinéaste
    movies_info = get_movie_info(url)
    movies_info = get_movie_info(url2)

    # Uploader les données dans Firestore
    upload_to_firestore(movies_info)
