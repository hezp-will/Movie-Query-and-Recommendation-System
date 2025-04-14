from surprise import Reader, Dataset, SVD, SVDpp
import pandas as pd
from surprise import dump

ratings = pd.read_csv('C:/Users/Ziheng/Desktop/COMP 631/631 project/ml-25m/ratings.csv')
movies = pd.read_csv('C:/Users/Ziheng/Desktop/COMP 631/631 project/ml-25m/movies.csv')
movies['release_year'] = movies['title'].str.extract(r'(?:\((\d{4})\))?\s*$', expand=False)
movies = movies.rename(columns={'title': 'movie_names'})

reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader=reader)
svd = SVD(n_factors=50)
trainset = dataset.build_full_trainset()
#svd.fit(trainset)

id_2_names = dict()
for idx, names in zip(movies['movieId'], movies['movie_names']):
    id_2_names[idx] = names


def Build_Anti_Testset4User(user_id):
    fill = trainset.global_mean
    anti_testset = list()
    u = trainset.to_inner_uid(user_id)

    # ur == users ratings
    user_items = set([item_inner_id for (item_inner_id, rating) in trainset.ur[u]])

    anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                             i in trainset.all_items() if i not in user_items]

    return anti_testset

def TopNRecs_SVD(user_id, num_recommender=10, latest=False):

    testSet = Build_Anti_Testset4User(user_id)
    predict = svd.test(testSet)

    recommendation = list()

    for userID, movieID, actualRating, estimatedRating, _ in predict:
        intMovieID = int(movieID)
        recommendation.append((intMovieID, estimatedRating))
        recommendation.sort(key=lambda x: x[1], reverse=True)

    movie_names = []
    movie_ratings = []

    for name, ratings in recommendation[:20]:
        movie_names.append(id_2_names[name])
        movie_ratings.append(ratings)

    movie_dataframe = pd.DataFrame({'movie_names': movie_names,
                                    'rating': movie_ratings}).merge(movies[['movie_names', 'release_year']],
                                                                            on='movie_names', how='left')


    if latest == True:
        return movie_dataframe.sort_values('release_year', ascending=False)[['movie_names', 'rating']].head(
            num_recommender)

    else:
        return movie_dataframe.drop('release_year', axis=1).head(num_recommender)


def TopNRecs_SVD_0(user_id, num_recommender=10, latest=False):

    testSet = Build_Anti_Testset4User(user_id)
    predict = loaded_algo.test(testSet)

    recommendation = list()

    for userID, movieID, actualRating, estimatedRating, _ in predict:
        intMovieID = int(movieID)
        recommendation.append((intMovieID, estimatedRating))
        recommendation.sort(key=lambda x: x[1], reverse=True)

    movie_names = []
    movie_ratings = []

    for name, ratings in recommendation[:20]:
        movie_names.append(id_2_names[name])
        movie_ratings.append(ratings)

    movie_dataframe = pd.DataFrame({'movie_names': movie_names,
                                    'rating': movie_ratings}).merge(movies[['movie_names', 'release_year']],
                                                                            on='movie_names', how='left')


    if latest == True:
        return movie_dataframe.sort_values('release_year', ascending=False)[['movie_names', 'rating']].head(
            num_recommender)

    else:
        return movie_dataframe.drop('release_year', axis=1).head(num_recommender)

# Save the model to a file
#file_name = '631Project_svd_model'
#dump.dump(file_name, algo=svd)

# Load the saved model
file_name = '631Project_svd_model'
_, loaded_algo = dump.load(file_name)

print(TopNRecs_SVD_0(20000, num_recommender=10))