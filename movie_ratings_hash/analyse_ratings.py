#!/usr/bin/env python

import pandas as pd
from movie_ratings_hash import HashTable

# Load and return the movie ratings dataset
def load_data():
        try:
            # Load in the ratings and movies datasets
            ratings_df = pd.read_csv("ratings.csv")
            movies_df = pd.read_csv("movies.csv")

            # Merge both datasets
            data = ratings_df.drop(["timestamp", "userId"], axis=1).merge(movies_df.drop("genres", axis=1), how="inner", on="movieId")

            # Drop irrelevant columns and group the combined dataset by the common movie
            grouped_data = data.groupby(["movieId", "title"]).median().reset_index().drop("movieId", axis=1)

            return grouped_data
        except FileNotFoundError:
            print("An error has occurred. We could not find the data file(s).")
        except:
            print("An error has occurred. Please try again")

# Class to analyse movie ratings
class MovieRatings:
    def __init__(self):
        # Load in movie ratings data and initialise has table
        self.data = load_data()
        self.ratings_db = HashTable(len(self.data))

    # Method to get data from file given a file name
    # If the file is not in the cache, fetch from disk
    def _store_data(self):
        data = self.data

        for index in range(len(data)):
            self.ratings_db.set(data.iloc[index]["title"], data.iloc[index]["rating"])


    # Request user to enter a movie title and get the average rating for that movie
    def _get_average_movie_rating(self, message):
        title_input = input(message).strip()
        self._get_average_rating(title_input)
        

    # Display menu foor user to make a selection
    def get_user_selection(self):
        try:
            # Store the dataset in a hash table
            self._store_data()

            message = """\n Please select the number corresponding to one of the following options (e.g. enter 1 for option 1):\n
                    1. Get average rating for a movie
                    2. Get the highest rated movie
                    3. Get the lowest rated movie\n
                    """
            
            # Initialise a breaker for the menu loop
            is_selection_valid = False

            while not is_selection_valid:
                # Obtain the user's menu selection
                selection = int(input(message))

                # Proceed if the user selects one of the available options
                if 0 < selection < 4:
                    # Break from the loop after this iteration
                    is_selection_valid = True

                    # Request a movie title if a user chooses to get the average rating of a movie
                    if selection == 1:
                        self._get_average_movie_rating("Please enter a full or partial movie title: \n")
                    # Get the lowest rated movie if the user chooses this option
                    elif selection == 2:
                        self._get_movie(False)
                    # Get the highest rated movie if the user chooses this option
                    else:
                        self._get_movie(True)

                    return selection
                else: 
                    # Display an error message if the user selects a number that isn't on the menu
                    print("\n That is not a valid option. Please try again.")
        except ValueError:
            print("You have entered a non-numerical value. Please restart the app and try again.")


    # Get the average rating of a movie
    def _get_average_rating(self, movie_title):
        # Get the movie by its title
        movie = self.ratings_db.get(movie_title)

        # Display the average movie rating if a movie matching that title is found
        if movie:
            print(f"The average rating for {movie.key} is {round(movie.value, 2)}")
        # Ask the user to enter a different movie title if the movie is not found
        else:
            self._get_average_movie_rating("Movie not found. Please adjust your search and try again:\n")


    # Get highest or lowest rated movie
    def _get_movie(self, is_lowest_rated):
        # Get lowest rated movie
        if is_lowest_rated:
            movie = self.ratings_db.get_lowest_value_item()
            print (f"\n The lowest rated movie is '{movie.key}' with a rating of {movie.value}.")
        # Get highest rated movie
        else:
            movie = self.ratings_db.get_highest_value_item()
            print (f"\n The highest rated movie is '{movie.key}' with a rating of {movie.value}.")

movie_ratings = MovieRatings()
movie_ratings.get_user_selection()