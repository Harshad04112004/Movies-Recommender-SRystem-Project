from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load files
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_df = pd.DataFrame(movies)

# Function to get poster url
def get_poster(movie_index):
    poster_path = movies_df.iloc[movie_index].get("poster_path", None)

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"


# Recommendation function
def recommend(movie):
    movie = movie.strip()

    if movie not in movies_df['title'].values:
        return []

    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []

    for i in movies_list:
        title = movies_df.iloc[i[0]].title
        poster = get_poster(i[0])

        recommendations.append({
            "title": title,
            "poster": poster
        })

    return recommendations


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend_movie():
    movie_name = request.form.get("movie")

    movie_recs = recommend(movie_name)

    return render_template('recommend.html', movie=movie_name, recommendations=movie_recs)


if __name__ == "__main__":
    app.run(debug=True)
