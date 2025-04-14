import customtkinter as ctk
from SearchFrame import SearchFrame
from ResultFrame import ResultFrame
from UserFrame import UserFrame
import pysolr
import pandas as pd
from surprise import dump
import csv
from surprise import Reader, Dataset, SVD, SVDpp



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # initialization of the model for recommendation
        self.ratings = pd.read_csv('C:/Users/Ziheng/Desktop/COMP 631/631 project/ml-25m/ratings.csv')
        self.movies = pd.read_csv('C:/Users/Ziheng/Desktop/COMP 631/631 project/ml-25m/movies.csv')
        self.movies['release_year'] = self.movies['title'].str.extract(r'(?:\((\d{4})\))?\s*$', expand=False)
        self.movies = self.movies.rename(columns={'title': 'movie_names'})

        self.reader = Reader(rating_scale=(1, 5))
        self.dataset = Dataset.load_from_df(self.ratings[['userId', 'movieId', 'rating']], reader=self.reader)
        #svd = SVD(n_factors=50)
        self.trainset = self.dataset.build_full_trainset()

        # Load the saved model
        self.file_name = '631Project_svd_model'
        _, self.loaded_algo = dump.load(self.file_name)

        self.id_2_names = dict()
        for idx, names in zip(self.movies['movieId'], self.movies['movie_names']):
            self.id_2_names[idx] = names

        # window
        self.geometry("800x1000")
        self.title("Movie Search")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=10)

        # widgets
        self.user_frame = UserFrame(self, header_name="User Login")
        self.user_frame.grid(row=0, column=0, padx=(20,20), pady=(50, 10), sticky="nswe")

        self.search_frame = SearchFrame(self, header_name="SearchFrame")
        self.search_frame.grid(row=1, column=0, padx=(20,20), pady=(10, 10), sticky="nswe")

        self.search_frame_button = ctk.CTkButton(self, text="Search", width=50, command=self.search, font=("Helvetica bold", 20))
        self.search_frame_button.grid(row=2, column=0, padx=20, pady=5, sticky="nswe")

        self.result_frame = ResultFrame(self, header_name="ResultFrame")
        self.result_frame.grid(row=3, column=0, padx=(20,20), pady=(10, 50), sticky="nswe")

    def query_search(self):
        query_input = self.search_frame.get_value()
        if query_input[0] or query_input[1] or query_input[2]:
            solr_movies = pysolr.Solr('http://localhost:8983/solr/631Project_movies', timeout=10)
            solr_tags = pysolr.Solr('http://localhost:8983/solr/631Project_tags', timeout=10)

            # Define the query parameters
            movie_params = {
                'q': 'title: *' + self.search_frame.get_value()[0] + '* AND genres: *' + self.search_frame.get_value()[
                    2] + '*',  # Query string
                'rows': 10000,  # Number of results to return
                'fl': 'movieId, title',  # Fields to return
            }

            # Execute the query and get the results
            results1 = solr_movies.search(**movie_params)

            tag_params = {
                'q': 'tag: *' + self.search_frame.get_value()[1] + '*',  # Query string
                'rows': 10000,  # Number of results to return
                'fl': 'movieId, tag',  # Fields to return
            }

            results2 = solr_tags.search(**tag_params)

            # display the results
            movies_in_results1 = {}
            movieIds_in_results1 = []
            movieIds_in_results2 = []
            for result in results1:
                movieIds_in_results1.append(result['movieId'][0])
                movies_in_results1[result['movieId'][0]] = result['title'][0]

            for result in results2:
                movieIds_in_results2.append(result['movieId'][0])

            Id_intersection = list(set(movieIds_in_results1).intersection(movieIds_in_results2))
            movie_names = []
            for movieId in Id_intersection:
                movie_names.append(movies_in_results1[movieId])

            self.display_search_results(movie_names)
        else:
            # Clear the listbox
            self.result_frame.listbox.delete(0, ctk.END)

    def recommend(self):
        if self.search_frame.switch_var.get() == 'on':
            userId = self.search_frame.get_value()
            self.display_recommendation_results(self, userId)

    def Build_Anti_Testset4User(self, user_id):
        fill = self.trainset.global_mean
        anti_testset = list()
        u = self.trainset.to_inner_uid(user_id)

        # ur == users ratings
        user_items = set([item_inner_id for (item_inner_id, rating) in self.trainset.ur[u]])

        anti_testset += [(self.trainset.to_raw_uid(u), self.trainset.to_raw_iid(i), fill) for
                         i in self.trainset.all_items() if i not in user_items]

        return anti_testset

    def TopNRecs_SVD_0(self, user_id, num_recommender=10, latest=False):

        testSet = self.Build_Anti_Testset4User(user_id)
        predict = self.loaded_algo.test(testSet)

        recommendation = list()

        for userID, movieID, actualRating, estimatedRating, _ in predict:
            intMovieID = int(movieID)
            recommendation.append((intMovieID, estimatedRating))
            recommendation.sort(key=lambda x: x[1], reverse=True)

        movie_names = []
        movie_ratings = []

        for name, ratings in recommendation[:20]:
            movie_names.append(self.id_2_names[name])
            movie_ratings.append(ratings)

        movie_dataframe = pd.DataFrame({'movie_names': movie_names,
                                        'rating': movie_ratings}).merge(self.movies[['movie_names', 'release_year']],
                                                                        on='movie_names', how='left')

        if latest == True:
            return movie_dataframe.sort_values('release_year', ascending=False)[['movie_names', 'rating']].head(
                num_recommender)

        else:
            return movie_dataframe.drop('release_year', axis=1).head(num_recommender)

    def search(self):
        """function to process the search request"""
        print(self.search_frame.switch_var.get())
        print(self.user_frame.get_value())

        self.query_search()
        self.recommend()
        self.result_frame.move_selected_item(self.result_frame.listbox, self.result_frame.listbox2, self.result_frame.listbox3)

    def display_recommendation_results(self, userId):
        self.Build_Anti_Testset4User(userId)
        recommend_df = self.TopNRecs_SVD_0(userId)
        for index, row in recommend_df.iterrows():
            # concat the row values
            row_string = ','.join(row.astype(str))
            self.result_frame.listbox2.insert(ctk.END, row_string)

    def display_search_results(self, movie_names):
        # Clear the listbox
        self.result_frame.listbox.delete(0, ctk.END)

        # Add the results to the Listbox
        # no more than 20 records
        if len(movie_names) > 20:
            for i in range(20):
                self.result_frame.listbox.insert(ctk.END, movie_names[i])
        else:
            for result in movie_names:
                self.result_frame.listbox.insert(ctk.END, result)

if __name__ == "__main__":
    app = App()
    app.mainloop()