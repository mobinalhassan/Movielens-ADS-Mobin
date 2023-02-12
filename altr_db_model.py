import os
from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
PATH_TO_DB = os.path.join(basedir, 'movies25M.db')
print(f"Path to DB ==> {PATH_TO_DB}")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH_TO_DB}'
db = SQLAlchemy(app)


class cal_rate_tbl(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    avg_rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer)


def create_cal_rate_table():
    engine = create_engine(f'sqlite:///{PATH_TO_DB}')
    conn = engine.connect()
    inspector = inspect(engine)
    with app.app_context():
        if 'cal_rate_tbl' in inspector.get_table_names():
            print("cal_rate_tbl table already exists")
        else:
            db.create_all()
            insert_query = text(
                "INSERT INTO cal_rate_tbl (movieId, avg_rating, rating_count) SELECT movieId, AVG(rating), COUNT(rating) FROM ratings_tbl GROUP BY movieId")
            conn.execute(insert_query)
        conn.close()


create_cal_rate_table()


# Creating the movie model
class Movie(db.Model):
    __tablename__ = 'movies_tbl'
    movieid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genres = db.Column('genres', db.String(500))


# # Creating the genre model
# class Genre(db.Model):
#     __tablename__ = 'genres_tbl'
#     genreid = db.Column(db.Integer, primary_key=True)
#     movieid = db.Column(db.Integer, db.ForeignKey('movies_tbl.movieid'))
#     genre = db.Column(db.String)
#
#
# # Function to split genres and populate genres_tbl
# def populate_genres_tbl():
#     engine = create_engine(f'sqlite:///{PATH_TO_DB}')
#     conn = engine.connect()
#     inspector = inspect(engine)
#     with app.app_context():
#         if 'genres_tbl' in inspector.get_table_names():
#             print("genres_tbl table already exists")
#         else:
#             db.create_all()
#             movies = Movie.query.all()
#             for movie in movies:
#                 genres = movie.genres.split('|')
#                 for genre in genres:
#                     genre_record = Genre(movieid=movie.movieid, genre=genre)
#                     db.session.add(genre_record)
#             db.session.commit()
#         conn.close()
#
#
# populate_genres_tbl()



class GenreInfo(db.Model):
    __tablename__ = 'genre_info_tbl'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), unique=True)

class Genres(db.Model):
    __tablename__ = 'genres_tbl'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies_tbl.movieid'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre_info_tbl.genre_id'))


with app.app_context():
    engine = create_engine(f'sqlite:///{PATH_TO_DB}')
    conn = engine.connect()
    inspector = inspect(engine)
    if 'genre_info_tbl' in inspector.get_table_names():
        print("genre_info_tbl table already exists")
    else:
        # Populate the genre_info_tbl
        genre_names = set()
        for movie in Movie.query.all():
            genres = movie.genres.split('|')
            for genre in genres:
                genre_names.add(genre)

        for genre_name in genre_names:
            genre_info = GenreInfo(genre_name=genre_name)
            db.session.add(genre_info)

        db.session.commit()

    if 'genres_tbl' in inspector.get_table_names():
        print("genres_tbl table already exists")
    else:
        # Populate the genres_tbl
        for movie in Movie.query.all():
            genres = movie.genres.split('|')
            for genre in genres:
                genre_info = GenreInfo.query.filter_by(genre_name=genre).first()
                genre = Genres(movie_id=movie.movieid, genre_id=genre_info.genre_id)
                db.session.add(genre)

        db.session.commit()






# Now genres_tbl has been split and Now I want to create indexing in movies_tbl on movieid and title and want to drop genres column from movies_tbl, then want to create index in genres_tbl on
# What is the difference between indexing like this
#  __table_args__ = (
#         db.Index('ix_genres', genres),
#     )
#
# or indexing by sending parameter
# movieid = db.Column(db.Integer, db.ForeignKey('movies_tbl.movieid'), index=True)
