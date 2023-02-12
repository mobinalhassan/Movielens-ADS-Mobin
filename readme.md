# How to set up and run

### First install required packages:

```pip install -r requirements.txt```

### You can use two method
**Recommended way**
* I have uploaded altered database `.bd` file in Google Drive and you can download using this [link](https://drive.google.com/file/d/1eQa7VimGSeDPFv-3Id14K075eoHba642/view?usp=share_link). you need to download and put into the root directory of project folder.


* Secondly, you can use steps which I use to set up database file. (Note: I'm using linux and given comments are linux base)

1) Install SQlite3: ```sudo apt install sqlite3```
2) To Verify installation: ```sqlite3 --version```
3) Start sqlite with this db name, then this will point to sqlite terminal  ```sqlite3 movies25M.db```
4) Run this ```.mode csv```
5) Run these to create tables: ```.import /path_to_csv/movies.csv movies_tbl``` e.g ```.import /home/mobin/PycharmProjects/Movie-ADS-Mobin/ml-25m/movies.csv movies_tbl```
6) create tables for each csv:

 ```.import /path_to_csv/links.csv links_tbl``` 

 ```.import /path_to_csv/ratings.csv ratings_tbl``` 

 ```.import /path_to_csv/tags.csv tags_tbl``` 

7) Now run my python script to make changes in DB: ```PYTHONPATH=./ python altr_db_model.py``` or ```PYTHONPATH=./ python3 altr_db_model.py```


After setting up DB in the root of project folder then you only need to run app.py file to run web app:

```PYTHONPATH=./ python app.py``` or ```PYTHONPATH=./ python3 app.py``` 

# Bonus and Super Bonus in Notebook
File name: ```Bonus and Super bonus Task.ipynb```

### Resources:
https://www.digitalocean.com/community/tutorials/

https://pythonbasics.org/flask-sqlalchemy/

https://github.com/codewithsadee/filmlane
