from enum import Enum

class Genre(Enum):
    Drama = 18
    Comedia = 35
    Scifi = 878


# TODO: id, name, imagem, birth_date
class Artista:
    def __init__(self, id, name, popularity = None, birth_date=None, profile_path=None):
        self.id = id
        self.name = name
        self.popularity = popularity
        self.birth_date = birth_date
        self.profile_path = profile_path


class TMDBMovie:
    def __init__(self, 
            id, 
            title, 
            popularity=None,
            poster_path=None,
            release_date=None,
            genres=None
        ):
        self.id = id
        self.title = title
        self.popularity = popularity
        self.poster_path = poster_path
        self.release_date = release_date
        self.genres = genres

