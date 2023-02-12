# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# from flask_sqlalchemy import SQLAlchemy
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
#
#
#
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import func
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
#
# class Score(db.Model):
#     genreid = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Float)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.genreid'))
#     user = db.relationship('User', backref=db.backref('scores', lazy='dynamic'))
#
# class User(db.Model):
#     genreid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#
# def get_avg_score(page):
#     avg_score_query = db.session.query(func.avg(Score.value).label('average_score')).join(User).paginate(page=page, per_page=10)
#     return avg_score_query.items[0][0]
#
#
# # avg_score_query = db.session.query(func.avg(ratings_tbl.rating).label('average_score')).join(movies_tbl).paginate(page=page,
# #                                                                                                          per_page=24)
# #     print(f"First avg ==> {avg_score_query.items[0][0]}")
# #     print(f"First avg ==> {avg_score_query.items}")
#
# # one working code
#     genre_list=[]
#     # for mg_rec in movies_genre_r:
#     #     print(f"mov_rec ==> {mg_rec.genres}")
#     #     genre_list = genre_list+str(mg_rec.genres).split('|')
#     # uni_genre = list(dict.fromkeys(genre_list))


print('''Python / Web scraping / Git / Airflow / AWS / Linux / Pandas / Numpy / MongoDB / Automation / CI-CD /
PostgreSQL / Keras / Tensorflow / JSON / Anaconda / Neural Networks and Deep Learning / Docker / Power BI,
Power Query / Matplotlib / SQL / Machine Learning / Jupyter Notebook / OpenCV / MySQL / Python + Selenium /
Selenium WebDriver / BeautifulSoup / AWS lambda / serverless / TensorFlow / Convolutional Neural Networks / Data
Visualization / Github / GItLab / Object-Oriented Programming / Data Preprocessing / HTML / Windows / Test
automation / Data ETL / Extract Transform Load (ETL) / Microsoft Powerpoint / Google Cloud Platform (GCP) / Cloud
platform: AWS, GCP etc. / Apache kafka / Apache Airflow / Data analysis and visualization tools (R, Python) / Power apps:
Power BI / CI/CD using Jenkins / Selenium Web Driver / Debian linux / Linux (terminal commands, Bash/Shell) / Point Of
Sale / JENKINS / Knowledge of pyspark / Python (matplotlib, pandas, numpy, etc) / Infrastructure Management:
Terraform / mlflow / ML pipeline experiments and tuning (MLflow)'''.replace('/', ','))
