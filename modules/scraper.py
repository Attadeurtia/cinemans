import requests
from bs4 import BeautifulSoup
import re



def info_film(url):
    
    response = requests.get(url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.content, "html.parser")

        # Extraire le titre de la page
        div = soup.find("div", class_="titlebar-title titlebar-title-xl")
        # Vérifier si l'élément a été trouvé
        if div is not None:
            # Extraire le texte
            text = div.text
            print(f"Titre: {text}")
        else:
            print("L'élément <div> n'a pas été trouvé.")

        # Trouver le réalisateur dans la balise meta
        director_meta = soup.find("meta", property="video:director")
        director_name = (
            director_meta["content"]
            if director_meta and "content" in director_meta.attrs
            else "Réalisateur non trouvé"
        )

        print(f"Redirecteur: {director_name}")

        # Trouver la section des informations du film
        info_div = soup.find("div", class_="meta-body-info")

        if info_div:
            # Récupérer la date de sortie
            release_date = (
                info_div.find("span", class_="blue-link").text.strip()
                if info_div.find("span", class_="blue-link")
                else "Date non trouvée"
            )

            # Récupérer la durée
            duration = [
                span for span in info_div.find_all("span") if span.text.strip() != ""
            ]
            duration_text = (
                duration[1].text.strip() if len(duration) > 1 else "Durée non trouvée"
            )

            # Récupérer les genres
            genre_links = info_div.find_all("span", class_="dark-grey-link")
            # affiche = info_div.find_all('a', class_='xXx dark-grey-link')
            genres = [genre.text for genre in genre_links]  # Récupérer les noms des genres
        else:
            release_date = "Informations non trouvées"
            duration_text = "Informations non trouvées"
            genres = []

        # Utiliser une expression régulière pour trouver la durée
        duration_match = re.search(r"(\d+\s*h\s*\d+\s*min)", info_div.prettify())

        if duration_match:
            duration = duration_match.group(1)  # Récupérer le texte correspondant
        else:
            print("Durée non trouvée")

        print(f"Durée: {duration}")
        print(f"Date de sortie: {release_date}")
        print(f"Durée: {duration_text}")
        print(f'Genres: {", ".join(genres)}')


    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")

    film_data = {
        "titre": text,
        "realisateur": director_name,
        "date_de_sortie": release_date,
        "duree": duration_text,
        "genres": genres,
    }

    return film_data

print(info_film("https://www.allocine.fr/film/fichefilm_gen_cfilm=197214.html"))


