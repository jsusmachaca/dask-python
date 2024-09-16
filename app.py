import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client

client = Client(":8786")

ratings = dd.read_csv('/data/u.data', delimiter='\t', header=None, names=['user_id', 'item_id', 'rating', 'timestamp'], encoding='latin1')
items = dd.read_csv('/data/u.item', delimiter='|', header=None, usecols=[0, 1], names=['item_id', 'title'], encoding='latin1')
users = dd.read_csv('/data/u.user', delimiter='|', header=None, names=['user_id', 'age', 'gender', 'occupation', 'zip_code'], encoding='latin1')

data = ratings.merge(items, on='item_id').merge(users, on='user_id')

rating_avg = data.groupby('item_id')['rating'].mean().compute()

top_movies = rating_avg.sort_values(ascending=False).head(10).index

top_movies_data = data[data['item_id'].isin(top_movies)]

occupation_ratings = top_movies_data.groupby(['occupation', 'title'])['rating'].mean().compute()

print("Películas con más votaciones:")
print(rating_avg.sort_values(ascending=False).head(10))

print("\nRanking de ocupaciones para las películas top:")
print(occupation_ratings)