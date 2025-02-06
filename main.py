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

    

class NewMovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    img_url= StringField("Cover", validators=[DataRequired()])
    submit = SubmitField('Update')


class EditMovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Update')


#create tables 

# with app.app_context():
#     db.create_all()

#add new entry 

# with app.app_context():
#     new_movie = Movie(title="Reservoir Dog", year="1992", description="This and that", review="I would like to see the movies", img_url="https://image.tmdb.org/t/p/w500/")
#     db.session.add(new_movie)
#     db.session.commit()


#get all entries 


@app.route("/")
def home():
    movies =Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=['GET', 'POST'])
def add_movie():
    form = NewMovieForm()


    if form.validate_on_submit():
        new_movie = Movie(title=form.title.data, year=form.year.data, description=form.description.data, review=form.review.data, img_url=form.img_url.data)
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("home"))
    
    return render_template("add.html", form=form)



@app.route("/edit/<int:movie_id>", methods = ['GET', 'POST'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = EditMovieForm(obj=movie)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie_id=movie_id)

@app.route("/delete/<int:movie_id>", methods =['GET', 'POST'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))





if __name__ == "__main__":
    app.run(debug=True)
