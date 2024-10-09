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



def get_movie_info(url):
    # Faire une requête pour obtenir le contenu de la page
    response = requests.get(url)

    # Vérifie si la requête a réussi
    if response.status_code != 200:
        print("Erreur lors de la récupération de la page")
        return []

    # Créer un objet BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Liste pour stocker les informations des films
    movies = []

    # Trouver tous les blocs de films
    movie_blocks = soup.find_all('div', class_='card entity-card entity-card-list movie-card-theater cf hred')

    for block in movie_blocks:
        # Récupérer l'image
        #img_tag = block.find('img', class_='thumbnail-img')
        #image_url = img_tag['data-src'] if img_tag else None
        
        # Récupérer le titre
        title_tag = block.find('h2', class_='meta-title')
        title = title_tag.get_text(strip=True) if title_tag else None
        
        # Récupérer les genres
        genres = []
        info_div = block.find('div', class_='meta-body-item meta-body-info')
        if info_div:
            genre_tags = info_div.find_all('span', class_='dark-grey-link')
            genres = [genre.get_text(strip=True) for genre in genre_tags]

        # Récupérer les différentes dates
        date_tags = info_div.find_all('span', class_='date')
        dates = [date.get_text(strip=True) for date in date_tags] if date_tags else []

        # Récupérer la durée
        duration_match = re.search(r'(\d+\s*h\s*\d+\s*min)', str(info_div))
        duration = duration_match.group(1) if duration_match else None
        
        # Récupérer le réalisateur
        director_tag1 = block.find('div', class_='meta-body-direction')
        director_tag = director_tag1.find('span', class_='dark-grey-link')
        director = director_tag.get_text(strip=True) if director_tag else None

# Récupérer les horaires et la version (VO/VF)
        showtimes = []
        versions = []
        showtime_blocks = block.find_all('div', class_='showtimes-hour-block')
        for showtime in showtime_blocks:
            hour = showtime.find('span', class_='showtimes-hour-item-value')
            if hour:
                showtimes.append(hour.get_text(strip=True))
            # Vérifier si la version est mentionnée
            version_info = showtime.find('div', class_='text')
            if version_info:
                version_text = version_info.get_text(strip=True)
                if 'VF' in version_text:
                    versions.append('VF')
                elif 'VO' in version_text:
                    versions.append('VO')

        # Stocker les informations dans un dictionnaire
        movie_info = {
            'title': title,
            #'image': image_url,
            'genres': genres,
            'dates': dates,
            'duration': duration,
            'director': director,
            "showtimes": showtimes,
            'versions': list(set(versions))  # Pour éviter les doublons
        }
        
        movies.append(movie_info)

    return movies