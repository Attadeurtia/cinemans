import requests
from bs4 import BeautifulSoup
import re

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

        # Récupérer l'ID du film
        title_link = block.find('a', class_='meta-title-link')
        if title_link and 'href' in title_link.attrs:
            href = title_link['href']
            # Extraire l'ID du film de l'URL
            film_id = href.split('=')[-1]  # Récupérer l'ID après le signe '='
            #supprimer le .html
            film_id = film_id.split('.')[0]
            print(f"ID du film : {film_id}")
        
        
        # Récupérer le titre
        title_tag = block.find('h2', class_='meta-title')
        title = title_tag.get_text(strip=True) if title_tag else None

        print(title)
        
        # Récupérer les genres
        genres = []
        info_div = block.find('div', class_='meta-body-item meta-body-info')
        if info_div:
            genre_tags = info_div.find_all('span', class_='dark-grey-link')
            genres = [genre.get_text(strip=True) for genre in genre_tags]

        print(genres)

        # Récupérer les différentes dates
        date_tags = info_div.find_all('span', class_='date')
        dates = [date.get_text(strip=True) for date in date_tags] if date_tags else []

        print(dates)

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

        # Trouver toutes les images avec la classe 'thumbnail-img'
        img_tags = block.find_all('img', class_='thumbnail-img')

        # Liste pour stocker les URLs des images qui se terminent par .jpeg
        jpeg_images = []

        # Vérifier chaque image pour le lien data-src
        for img_tag in img_tags:
            if 'data-src' in img_tag.attrs:
                image_url = img_tag['data-src']
                # Vérifier si l'URL se termine par .jpeg
                if image_url.endswith('.jpg'):
                    jpeg_images.append(image_url)

        # Afficher les résultats
        print("Images .jpg trouvées :")
        for url in jpeg_images:
            print(url)

        # Stocker les informations dans un dictionnaire
        movie_info = {
            'id': film_id,
            'title': title,
            'genres': genres,
            'dates': dates,
            'duration': duration,
            'director': director,
            "showtimes": showtimes,
            'versions': list(set(versions)),  # Pour éviter les doublons
            "image": url
        }
        
        movies.append(movie_info)

    return movies


# URL de la page à scraper
url = 'https://www.allocine.fr/seance/salle_gen_csalle=P8501.html'

# Appeler la fonction pour récupérer les informations des films
movies_info = get_movie_info(url)



