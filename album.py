import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def find_album(artist, album):
    """
    Проверяет в базе данных по заданному артисту заданный альбов
    """
    session = connect_db()
    album = session.query(Album).filter(Album.artist == artist).filter(Album.album == album).first()
    return album

def is_number(a):
    try:
        int(a)
        return int(a)
    except ValueError:
        return False
def album_add(year, artist, genre, album):
    """
    принимает данные об альбоме, создает объект класса Album и добавляет его в базу
    """
    session = connect_db()
    NewAlbum = Album(year = year, artist = artist, genre = genre, album = album)
    session.add(NewAlbum)
    session.commit()