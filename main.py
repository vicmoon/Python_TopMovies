from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from sqlalchemy import Column, Integer, String, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Column
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-movies-collection.db"

# init SQLAlchemy with the app 
db = SQLAlchemy(model_class=Base)
db.init_app(app)


#Define a module 

class Movie(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    year = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    review = Column(String(250), nullable=False)
    img_url = Column(String(250), nullable=False)

    __table_args__ = (
        UniqueConstraint('title', name='uq_movie_title'),
    )

#create tables 

with app.app_context():
    db.create_all()

#add new entry 

with app.app_context():
    new_movie = Movie(title="New Movie", year="2025", description="The Description", review="The Review", img_url="https://image.tmdb.org0.jpg")
    db.session.add(new_movie)
    db.session.commit()



@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
