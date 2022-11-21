import pandas as pd
import numpy as np
from tmdbv3api import TMDb
from tmdbv3api import Movie
import json
import requests



def get_director(x):
    if " (director)" in x: #we are getting "director"
        return x.split(" (director)")[0]
    elif " (directors)" in x: #we are getting "directors" with "s"
        return x.split(" (directors)")[0]
    else:
        return x.split(" (director/screenplay)")[0] #we are getting "directors/screenplay"

def get_director(x):
    if " (director)" in x: #we are getting "director"
        return x.split(" (director)")[0]
    elif " (directors)" in x: #we are getting "directors" with "s"
        return x.split(" (directors)")[0]
    else:
        return x.split(" (director/screenplay)")[0] #we are getting "directors/screenplay"

def get_actor1(x):
    return ((x.split("screenplay); ")[-1]).split(", ")[0])


def get_actor2(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 2:
        return np.NaN
    else:
        return ((x.split("screenplay); ")[-1]).split(", ")[1])

def get_actor3(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 3:
        return np.NaN
    else:
        return ((x.split("screenplay); ")[-1]).split(", ")[2])
    
def get_year_data(year):
    link = "https://en.wikipedia.org/wiki/List_of_American_films_of_{}".format(year)
    df1 = pd.read_html(link, header=0)[2]
    df2 = pd.read_html(link, header=0)[3]
    df3 = pd.read_html(link, header=0)[4]
    df4 = pd.read_html(link, header=0)[5]

    df = df1.append(df2.append(df3.append(df4,ignore_index=True),ignore_index=True),ignore_index=True)

    tmdb = TMDb()
    tmdb.api_key = '8f644457912ac0ba2c4dcce6ca66ff6c' #add your own API key here

    tmdb_movie = Movie()
    def get_genre(x): #pass in the title of the movies
        genres = []
        result = tmdb_movie.search(x) #the title will be searched in the tmdb_movie
        movie_id = result[0].id #we will match the "id" with the "title"
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key)) #we will get the result from the IMDb data
        data_json = response.json() #we will then convert it to a json file
        if data_json['genres']: #in the json file we will only need to extract the "genre"
            genre_str = " " 
            for i in range(0,len(data_json['genres'])):
                genres.append(data_json['genres'][i]['name']) #we will then add the "genre" to the empty genre list we created above
            return genre_str.join(genres)
        else:
            np.NaN # we will return the results but if we don't find anything we will consider it as a missing value

    df['genres'] = df['Title'].map(lambda x: get_genre(str(x)))
    df_year = df[['Title','Cast and crew','genres']]

    #let's apply the above get_director function on the "Cast and crew" column
    df_year['director_name'] = df_year['Cast and crew'].map(lambda x: get_director(x))
    df_year['actor_1_name'] = df_year['Cast and crew'].map(lambda x: get_actor1(x))
    df_year['actor_2_name'] = df_year['Cast and crew'].map(lambda x: get_actor2(x))
    df_year['actor_3_name'] = df_year['Cast and crew'].map(lambda x: get_actor3(x))
    df_year = df_year.rename(columns={'Title':'movie_title'})
    new_df_year = df_year.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]
    new_df_year['actor_2_name'] = new_df_year['actor_2_name'].replace(np.nan, 'unknown')
    new_df_year['actor_3_name'] = new_df_year['actor_3_name'].replace(np.nan, 'unknown')
    new_df_year['movie_title'] = new_df_year['movie_title'].str.lower()

    new_df_year['comb'] = new_df_year['actor_1_name'] + ' ' + new_df_year['actor_2_name'] + ' '+ new_df_year['actor_3_name'] + ' '+ new_df_year['director_name'] +' ' + new_df_year['genres']
    return new_df_year


print('fetch and clean 2018 movie data from wikipedia')
new_df18 = get_year_data(2018)
print('fetch and clean 2019 movie data from wikipedia')
new_df19 = get_year_data(2019)

print('start to combine new (2018, 2019) and old data (upto 2017)')
my_df = new_df18.append(new_df19,ignore_index=True)
old_df = pd.read_csv('../lib/new_data.csv')
final_df = old_df.append(my_df,ignore_index=True)
final_df = final_df.dropna(how='any')
final_df.to_csv('../lib/final_data.csv',index=False)
print('done')



