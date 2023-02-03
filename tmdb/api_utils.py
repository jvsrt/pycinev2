import requests
from tmdb.models import TMDBMovie, Genre, Artista
from service import Service

key = '524ab2a56edf50b5ab14ae2c843bd495'

class RequestApi:
    """
    
    Esta classe faz request para a API do tmdb,
    de acordo com funções pre-definidas do nosso app

    """
    @staticmethod
    def test():
        print('[ok] from RequestApi')

    @staticmethod
    def get_genres():
        # TODO: load data/genres.json
        pass

    @staticmethod
    def get_movie_popular_by_genre(genre: int):
        endpoint = f'https://api.themoviedb.org/3/discover/movie/?api_key={key}&certification_country=US&certification=R&sort_by=vote_count.desc&with_genres={genre}'
        r = requests.get(endpoint)
        # print(r.status_code) # deve retornar 200
        data = r.json()
        results = data['results']
        return results


    # nome do artista: "Arnold Schwarzenegger"
    # def get_artista_by_name(name)
    #     endpoint: search_person

    @staticmethod
    def get_artista(person_id: int):
        endpoint = f'https://api.themoviedb.org/3/person/{person_id}?api_key={key}'
        r = requests.get(endpoint)
        data = r.json()
        results = data
        return results

    @staticmethod
    def get_artista_by_name(query: str):
        endpoint = f'https://api.themoviedb.org/3/search/person?api_key={key}&query={query}'
        r = requests.get(endpoint)
        data = r.json()
        results = data['results']
        return results




class MovieUtils:
    """
    classe utilitaria para ser usada no fastapi
    """
    @staticmethod
    def get_genres(genre_ids):
        # TODO: gambiarra - precisa busca no tmdb todos os
        # genres... mas por enquanto...
        ids = [e.value for e in Genre]
        genres_str = [
            Genre(g).name for g in genre_ids if g in ids
            ]
        return " | ".join(genres_str)

    @staticmethod
    def get_image_path(poster_path):
        return f"https://image.tmdb.org/t/p/w185{poster_path}"

    @staticmethod
    def get_movies(genre: int):
        # obter o titulo (original_title)
        # percorremos a lista de filmes (results)
        results = RequestApi.get_movie_popular_by_genre(genre)
        movies = []  # lista que armazena os filmes
        for movie in results:
            m = TMDBMovie(
                movie['id'],
                movie['original_title'],
                genres=MovieUtils.get_genres(
                    movie['genre_ids']
                ),
                poster_path=MovieUtils.get_image_path(
                    movie['poster_path']
                )
            )
            movies.append(m)
                
        return movies

class ArtistaUtils:
    """
    classe utilitaria para ser usada no fastapi
    """

    @staticmethod
    def get_image_path(profile_path):
        return f"https://image.tmdb.org/t/p/w185{profile_path}"

    @staticmethod
    def get_artistas(query: str):
        # percorremos a lista de artistas (results)
        results = RequestApi.get_artista_by_name(query)

        artistas = []
        for artista in results:
            a = Artista(
                artista['id'],
                artista['name'],
                artista['popularity'],
                profile_path=ArtistaUtils.get_image_path(
                    artista['profile_path']
                )
            )
            artistas.append(a)
        return artistas