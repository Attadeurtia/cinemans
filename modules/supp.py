import firebase_admin
from firebase_admin import credentials, firestore

# Initialiser l'application Firebase
cred = credentials.Certificate("data/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

def delete_collection(collection_ref, batch_size):
    db = firestore.client()
    docs = collection_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(collection_ref, batch_size)

if __name__ == "__main__":
    db = firestore.client()
    collection_name = 'movies'  # Remplacez par le nom de votre collection
    collection_ref = db.collection(collection_name)

    # Supprimer tous les documents de la collection
    delete_collection(collection_ref, 10)
    print(f'Tous les documents de la collection {collection_name} ont été supprimés.')