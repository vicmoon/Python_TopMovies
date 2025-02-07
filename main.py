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
# import my_secrets
import os 
 




app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

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
    review = Column(String(250), nullable=True)
    img_url = Column(String(250), nullable=False)

    __table_args__ = (
        UniqueConstraint('title', name='uq_movie_title'),
    )

    

class NewMovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # year = StringField("Year", validators=[DataRequired()])
    # description = StringField('Description',validators=[DataRequired()])
    # review = StringField("Review", validators=[DataRequired()])
    # img_url= StringField("Cover", validators=[DataRequired()])
    submit = SubmitField('Add')


class EditMovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    review= StringField('Review',validators=[DataRequired()])
    submit = SubmitField('Update')


#create tables 

with app.app_context():
    db.create_all()

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
        print("Form submitted!")  # Debugging

        MOVIE_TITLE = form.title.data.strip()
        print("Movie title:", MOVIE_TITLE)  # Debugging

        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={MOVIE_TITLE}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error fetching movie data:", response.status_code)
            return "Error fetching movie data", 500 

        data = response.json()
        # print("Data received:", data)  # Debugging

        if data["results"]:
            movie_data = data['results']
            # print("Movies found:", movie_data)  # Debugging

            return render_template("select.html", movies=movie_data)

    return render_template("add.html", form=form)


@app.route("/add/<int:movie_id>")
def add_movie_id(movie_id):
     
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    response = requests.get(url)

    if response.status_code != 200:
         return "Error fetching the movie", 500
    
    

    movie_data = response.json()
    year=movie_data.get("release_date", "Unknown")
    year = year[:4] if year and len(year) >= 4 else "Unknown"
    new_movie = Movie(
                title=movie_data["title"], 
                year= year,
                description=movie_data.get("overview", "No data available"), 
                review=None,  # ✅ This prevents the NOT NULL error
                img_url=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data.get("poster_path") else None
            )
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('home'))



@app.route("/edit/<int:movie_id>", methods = ['GET', 'POST'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = EditMovieForm(obj=movie)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.description = form.description.data
        movie.review = form.review.data 
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
