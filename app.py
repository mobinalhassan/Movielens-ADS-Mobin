import os
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import time
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

basedir = os.path.abspath(os.path.dirname(__file__))
PATH_TO_DB = os.path.join(basedir, 'movies25M.db')
print(f"Path to DB ==> {PATH_TO_DB}")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mobin/PycharmProjects/Movie-ADS-Mobin/movies25M.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH_TO_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class cal_rate_tbl(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    avg_rating = db.Column(db.Float)
    rating_count = db.Column(db.Integer)

    def __init__(self, movieId, avg_rating, rating_count):
        self.movieId = movieId
        self.avg_rating = avg_rating
        self.rating_count = rating_count

    __table_args__ = (
        db.Index('ix_movie_avg_rating', movieId, avg_rating),
    )


class movies_tbl(db.Model):
    __tablename__ = 'movies_tbl'
    id = db.Column('movieid', db.Integer, primary_key=True)
    title = db.Column('title', db.String(500))
    genres = db.Column('genres', db.String(500))
    # genres = 'que_gen'

    def __init__(self, title, genres):
        self.title = title
        self.genres = genres

    __table_args__ = (
        db.Index('ix_movieId_title', id, title),
    )



class ratings_tbl(db.Model):
    userId = db.Column('userId', db.Integer)
    movieId = db.Column('movieId', db.Integer, db.ForeignKey('movies_tbl.movieId'), primary_key=True)
    rating = db.Column('rating', db.String(100))
    timestamp = db.Column('timestamp')

    def __init__(self, userId, movieId, rating, timestamp):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp

    __table_args__ = (
        db.Index('ix_movie_userId_rating', movieId, userId, rating),
    )


class Genre(db.Model):
    __tablename__ = 'genres_tbl'
    id = db.Column('id', db.Integer, primary_key=True)
    genreid = db.Column('genre_id', db.Integer, primary_key=True)
    movieid = db.Column('movie_id', db.Integer, db.ForeignKey('movies_tbl.movieid'))
    # genre = db.Column(db.String)

    def __init__(self, genreid, movieid, genre):
        self.genreid = genreid
        self.movieid = movieid
        self.genre = genre

    __table_args__ = (
        db.Index('ix_movieid_genres', movieid),
    )


class GenreInfo(db.Model):
    __tablename__ = 'genre_info_tbl'
    id = db.Column('genre_id', db.Integer, primary_key=True)
    genre_name = db.Column(db.String)


def check_indexes():
    for table in db.metadata.tables.values():
        for index in table.indexes:
            print(f"Index {index.name} on table {table.name}")


check_indexes()


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    # movies_tbl_paged = movies_tbl.query.paginate(page=page, per_page=24)
    query = db.session.query(movies_tbl, func.group_concat(GenreInfo.genre_name, '|').label("genres_list")).join(Genre, movies_tbl.id == Genre.movieid).join(GenreInfo,
                                                                                            Genre.genreid == GenreInfo.id).group_by(movies_tbl.id, movies_tbl.title)

    movies_tbl_paged = query.paginate(page=page, per_page=24, error_out=False)

    print(db.engine.execute("EXPLAIN QUERY PLAN SELECT * FROM movies_tbl"))
    scroll_status = 0
    if page > 1:
        print(f"Page ==> {page}")
        scroll_status = 1
    print(f"Query return ==> {movies_tbl_paged}")
    for single in movies_tbl_paged:
        print('*'*40)
        print(single)
        print(single.movies_tbl.id)
        print(single.movies_tbl.title)
        print(single.genres_list)


    return render_template('index.html', pagination=movies_tbl_paged, scroll=scroll_status)


@app.route('/search')
def search():
    query = request.args.get('query')
    print(f'Query ==> {query}')

    # query = '(1995)'
    if not query:
        return render_template('search_results.html')

    results = movies_tbl.query.filter(movies_tbl.title.ilike('%' + query + '%')).all()
    print(f"Results ==> {results}")
    return render_template('search_results.html', results=results)

m=25000
def calculate_weighted_rating(movies, avg_rating, rating_count):
    # select the rating_avg and rating count for each movie
    # Raw query to fine avg of movie ratings SELECT AVG(rating) FROM ratings_tbl;

    # result = db.session.query(cal_rate_tbl.avg_rating, cal_rate_tbl.rating_count).filter_by(movieId=movies.id).first()
    # if result is None:
    #     return 0
    v = rating_count
    # R = result.avg_rating
    R = avg_rating
    C = 3.53
    weighted_rating = (v / (v + m) * R) + (m / (v + m) * C)
    # print(f'Weighted Rating ==> {weighted_rating}')
    return weighted_rating
    # results.append((movies, weighted_rating))
    # if result is None:
    #     return 0
    # vote_average = result.avg_rating
    #
    # vote_count = result.rating_count
    # weighted_rating = (vote_average * vote_count) / (vote_count + m)
    # print(f'Weighted Rating ==> {weighted_rating}')
    # return weighted_rating

@app.route('/filter', methods=['GET', 'POST'])
def filter_search():
    # for selecting unique Genre
    global filter_movies, heading
    filter_movies = None
    heading = None
    # genre_list = [genre.genres for genre in db.session.query(movies_tbl.genres).all()]
    # genre_list = [i for sub in genre_list for i in sub.split('|')]
    # unique_genre_list = sorted(list(set(genre_list)))

    genres = GenreInfo.query.all()
    unique_genre_list = sorted([genre.genre_name for genre in genres])

    # print(f'Unique ==> {unique_genre_list}')
    print(request.method)



    # best rated films here
    if request.method == 'POST':
        sort = request.form['sort']
        genres_wp = request.form['genres']
        limit = request.form.get('limit')
        print(f'Sort ==> {sort}')
        print(f'genres_wp ==> {genres_wp}')
        print(f'limit ==> {limit}')

        if sort == 'top':
            start_time = time.time()

            genre = db.session.query(GenreInfo).filter_by(genre_name='Comedy').first()
            print(f'Genra ==> {genre} ==> {genre.id}')
            genre_id = genre.id

            # movies = db.session.query(movies_tbl).join(Genre, movies_tbl.id == Genre.movieid).filter(Genre.genreid == genre_id).all()
            movies = db.session.query(movies_tbl, cal_rate_tbl.avg_rating, cal_rate_tbl.rating_count).join(Genre,
                                                                                                           movies_tbl.id == Genre.movieid).join(
                cal_rate_tbl, movies_tbl.id == cal_rate_tbl.movieId).filter(Genre.genreid == genre_id).all()
            print(f'Movie ==> {movies[:100]}')
            print(f'Movie ==> {len(movies)}')
            # Calculate the weighted rating of each movie and store the result in a dictionary
            weighted_ratings = {}
            movies_data_dict = {}
            for movie in movies:
                # weighted_ratings[movie.movies_tbl.id] = calculate_weighted_rating(movie.movies_tbl, movie.avg_rating,
                #                                                                   movie.rating_count)
                weighted_ratings[movie.movies_tbl.id] = [calculate_weighted_rating(movie.movies_tbl, movie.avg_rating,
                                                                                  movie.rating_count), movie.movies_tbl.title, movie.movies_tbl.genres, movie.rating_count]

                # movies_data_dict[movie.movies_tbl.id] = [movie.movies_tbl.title, ]

            print(f'Dict ==> {weighted_ratings.items()}')

            # Sort the dictionary by the weighted ratings in descending order
            sorted_weighted_ratings = sorted(weighted_ratings.items(), key=lambda x: x[1], reverse=True)

            # Get the top 10 rated movies for the genre 'Comedy'
            top_10_movies = sorted_weighted_ratings[:10]
            print(f'Top reated Movies ==> {top_10_movies}')

            filter_movies = top_10_movies
            end_time = time.time()
            print("Time taken for the top-query: ", end_time - start_time)
            for st_movie in filter_movies:
                print(st_movie)

        heading = f"Sorted By: {limit} {str(sort).upper()} rated {genres_wp} Movies"
        # print(filter_movies)
    return render_template('filter-search.html', genre_list=unique_genre_list, heading=heading,
                           filter_movies=filter_movies)


app.run(debug=True)
