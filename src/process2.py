import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_genresList(x):
    # we will have to take out the individual genres like adventure, action, sci-fi, etc. using the following function
    gen = []
    st = " "
    for i in x:
        if i.get('name') == 'Science Fiction': #am only renaming the "Science Fiction" to "Sci-Fi" to make it the name shorter. Apart from that all other names remain the same.
            scifi = 'Sci-Fi'
            gen.append(scifi)
        else:
            gen.append(i.get('name'))
    if gen == []:
        return np.NaN
    else:
        return (st.join(gen)) #then we will join them together and return the valuse
    
def get_actor1(x):
    #let's do the same for cast
    casts = []
    for i in x:
        casts.append(i.get('name'))
    if casts == []:
        return np.NaN
    else:
        return (casts[0])
    

def get_actor2(x):
    casts = []
    for i in x:
        casts.append(i.get('name'))
    if casts == [] or len(casts)<=1:
        return np.NaN
    else:
        return (casts[1])

def get_actor3(x):
    casts = []
    for i in x:
        casts.append(i.get('name'))
    if casts == [] or len(casts)<=2:
        return np.NaN
    else:
        return (casts[2])

def get_directors(x):
    dt = []
    st = " "
    for i in x:
        if i.get('job') == 'Director':
            dt.append(i.get('name'))
    if dt == []:
        return np.NaN
    else:
        return (st.join(dt))
    
def CombineData(outfile):
    """Extract 2017 data and clean it up to match up with 2016 format, and then combine them.
    """
    credits = pd.read_csv('../lib/contents/credits.csv')
    meta = pd.read_csv('../lib/contents/movies_metadata.csv')

    meta['release_date'] = pd.to_datetime(meta['release_date'], errors = 'coerce')

    #format the date
    meta['year'] = meta['release_date'].dt.year

    # Getting only 2017 movies as we already have movies up to the year 2016 in data 1 processed file. 
    # We don't have enough data for the movies from 2018, 2019 and 2020. 
    # We'll deal with it in the upcoming preprocessing files
    new_meta = meta.loc[meta.year == 2017,['genres','id','title','year']]

    #converting the "id" to integer
    new_meta['id'] = new_meta['id'].astype(int)

    #add the new_meta data to the credit data. They all have "id" so we can merge on that.
    data = pd.merge(new_meta, credits, on='id')

    # we will convert the "genre", "cast" and "crew" column into a list. if we observe it carefully, we will realised that it's a list containing dictionary. 
    import ast
    data['genres'] = data['genres'].map(lambda x: ast.literal_eval(x))  #the "literal_eval" helps to convert the string into a list
    data['cast'] = data['cast'].map(lambda x: ast.literal_eval(x))
    data['crew'] = data['crew'].map(lambda x: ast.literal_eval(x))


    #now let's apply the make_genresList function on the genre column
    data['genres_list'] = data['genres'].map(lambda x: make_genresList(x))


    #let's apply it on the cast column for the first actor
    data['actor_1_name'] = data['cast'].map(lambda x: get_actor1(x))

    #let's apply it on the cast column for the second actor
    data['actor_2_name'] = data['cast'].map(lambda x: get_actor2(x))

    data['actor_3_name'] = data['cast'].map(lambda x: get_actor3(x))

    data['director_name'] = data['crew'].map(lambda x: get_directors(x))

    #selecting only the prepared data
    movie = data.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres_list','title']]

    #drop missing values
    movie = movie.dropna(how='any')

    #renaming
    movie = movie.rename(columns={'genres_list':'genres'})
    movie = movie.rename(columns={'title':'movie_title'})

    #convert all movie titles to lower case
    movie['movie_title'] = movie['movie_title'].str.lower()

    #we will be using this information later on in the tfidvectorizor
    movie['comb'] = movie['actor_1_name'] + ' ' + movie['actor_2_name'] + ' '+ movie['actor_3_name'] + ' '+ movie['director_name'] +' ' + movie['genres']

    old = pd.read_csv('../lib/data1.csv')

    old['comb'] = old['actor_1_name'] + ' ' + old['actor_2_name'] + ' '+ old['actor_3_name'] + ' '+ old['director_name'] +' ' + old['genres']

    #putting all datasets together
    new = old.append(movie)

    #we are dropping the duplicated valuse and keeping only the last one, so that there will be only one type of a particular movie and not duplicates of same movie
    new.drop_duplicates(subset ="movie_title", keep = 'last', inplace = True)

    #saving all the data up to 2017
    new.to_csv(outfile,index=False)
    

CombineData('../lib/new_data.csv')
print('done')