import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client
from os import environ, path, listdir

client = Client(f"{environ.get("DASK_IP")}:8786")

print(listdir('.'))
print(listdir('data'))

try:
    ratings = dd.read_csv('data/u.data.csv', delimiter='\t', header=None, names=['user_id', 'item_id', 'rating', 'timestamp'], encoding='UTF-8')
    items = dd.read_csv('data/u.item.csv', delimiter='|', header=None, usecols=[0, 1], names=['item_id', 'title'], encoding='ISO-8859-1')
    users = dd.read_csv('data/u.user.csv', delimiter='|', header=None, names=['user_id', 'age', 'gender', 'occupation', 'zip_code'], encoding='ISO-8859-1')

    data = ratings.merge(items, on='item_id').merge(users, on='user_id')

    rating_avg = data.groupby('item_id')['rating'].mean().compute()

    top_movies = rating_avg.sort_values(ascending=False).head(10).index

    top_movies_data = data[data['item_id'].isin(top_movies)]

    occupation_ratings = top_movies_data.groupby(['occupation', 'title'])['rating'].mean().compute()

    print("Películas con más votaciones:")
    print(rating_avg.sort_values(ascending=False).head(10))

    print("\nRanking de ocupaciones para las películas top:")
    print(occupation_ratings)
except Exception as e:
    print(e)
