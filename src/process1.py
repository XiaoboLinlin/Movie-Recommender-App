import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def CleanDataTo2016(outfile):
    """ Clean data up to 2016
    
    """
    data = pd.read_csv('../lib/datasets/movie_metadata.csv')
    data = data.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]

    data['actor_1_name'] = data['actor_1_name'].replace(np.nan, 'unknown')
    data['actor_2_name'] = data['actor_2_name'].replace(np.nan, 'unknown')
    data['actor_3_name'] = data['actor_3_name'].replace(np.nan, 'unknown')
    data['director_name'] = data['director_name'].replace(np.nan, 'unknown')

    data['genres'] = data['genres'].str.replace('|', ' ')
    data['movie_title'] = data['movie_title'].str.lower()

    # removing the null terminating char at the end
    data['movie_title'] = data['movie_title'].apply(lambda x : x[:-1])
    #let's save the processed dataset
    data.to_csv(outfile,index=False)

CleanDataTo2016('../lib/data1.csv')
print('done')
    