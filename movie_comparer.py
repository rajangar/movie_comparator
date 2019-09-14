import json
import os
import requests
from collections import defaultdict
from multiprocessing import Pool
import sys
import time
from dotenv import load_dotenv

class MovieComparer:
    """ To provide apis results and price comparison from 2 Databases
    """
    def __init__(self):
        """ Show movie list by fetching 2 databases parallely
        """
        load_dotenv()
        self.api_url_base = os.getenv('API_URL_BASE')
        self.token = os.getenv('API_TOKEN')

        exp = 1
        while True:
            cinemaworld_movies, filmworld_movies = self.get_movies()
            if cinemaworld_movies is None:
                print("Error in fetching movies list")
                self.exponential_backoff(exp)
                exp *= 2
            else:
                break

        self.title_map = self.get_title_map(cinemaworld_movies, filmworld_movies)
        self.title_list = sorted(list(self.title_map.keys()))

        self.show_all_movies()

    def exponential_backoff(self, exp_secs):
        print("Trying again in {} seconds".format(exp_secs))
        time.sleep(exp_secs)

    def get_url_parameters(self):
        """ Get URL parameters and token from environment variable
        """
        headers = {'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'x-access-token',
            'x-access-token': '{}'.format(self.token)}
        return headers

    def get_dict_from_apis(self, api_url):
        """ Call APIs here
        """
        headers = self.get_url_parameters()

        try:
            response = requests.get(api_url, headers=headers, timeout=1)
        except requests.exceptions.Timeout as e:
            print("{}, Try again".format(e))
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            exit()

        if response.status_code == 200:
            data_dict = json.loads(response.content.decode('utf-8'))
            return data_dict
        return None


    def get_movies_list(self, world):
        """ Provide Movies dictionary with world as key
        """
        api_url = self.api_url_base + '/api/{}/movies'.format(world)
        movies_dict = self.get_dict_from_apis(api_url)
        ret_dict = {world: None}
        if movies_dict is not None:
            ret_dict[world] = movies_dict['Movies']
        return ret_dict

    def get_movie_from_id(self, pick_info):
        """ Provide movie data from different databases, by searching through ID
        """
        world = pick_info['world']
        _id = pick_info['id']
        api_url = self.api_url_base + '/api/{}/movie/{}'.format(world, _id)
        exp = 1
        while True:
            movie_data = self.get_dict_from_apis(api_url)
            if movie_data is None:
                print("Error in fetching movie with id:{}".format(_id))
                self.exponential_backoff(exp)
                exp *= 2
            else:
                movie_data['world'] = world
                break

        return movie_data

    def get_movies(self):
        """ Providing multi processing functionality to get movies list
        """
        worlds = ['cinemaworld',
                  'filmworld']

        pool = Pool(2)
        movies_world = pool.map(self.get_movies_list, worlds)
        pool.close()
        pool.join()

        for m_world in movies_world:
            world_type = list(m_world)[0]
            if m_world[world_type] == None:
                return None, None
            if world_type == "cinemaworld":
                cinemaworld_movies = m_world[world_type]
            elif world_type == "filmworld":
                filmworld_movies = m_world[world_type]

        return cinemaworld_movies, filmworld_movies

    def titles_generator(self, movies_world, world):
        """ Provide generator object of all movies in a world
        """
        for movie in movies_world:
            movie['world'] = world
            yield movie

    def  get_title_map(self, cinemaworld_movies, filmworld_movies):
        """ Returning title map as title as key and movie info as value
        """
        title_map = defaultdict(list)

        cinema_gen = self.titles_generator(cinemaworld_movies, "cinemaworld")
        for movie in cinema_gen:
            title_map[movie['Title'].strip().lower()].append(movie)
        film_gen = self.titles_generator(filmworld_movies, "filmworld")
        for movie in film_gen:
            title_map[movie['Title'].strip().lower()].append(movie)

        return title_map

    def  show_all_movies(self):
        """ Print all unique movies from 2 databases
        """
        print("All Movies List:\n----------------------------")
        for index, title in enumerate(self.title_list):
            movie = self.title_map[title][0]
            print(" Index: {0}\n Title: {1}\n Year: {2}\n Type: {3}\n Poster: {4}"
                .format(index + 1, title, movie['Year'], movie['Type'], movie['Poster']))
            print("-------------------------------------------------------------\n")

    def get_cheapest(self, pick):
        """ Provide the cheapest price by comparing from multiple databases
        """
        pool = Pool(2)
        pick_list = []

        try:
            for movie_info in self.title_map[self.title_list[pick - 1]]:
                movie_id = movie_info['ID']
                movie_world = movie_info['world']
                pick_list.append({'id': movie_id, 'world': movie_world})
        except IndexError:
            print("Please provide valid index")
            return None
        except TypeError:
            print("Please provide valid index")
            return None

        movies_list = pool.map(self.get_movie_from_id, pick_list)
        pool.close()
        pool.join()

        # Set price as maximum float value in start to find minimum value
        price = sys.float_info.max
        print("\nMovie info from different worlds:\n")
        for movie in movies_list:
            print("[{}]".format(movie['world']))
            for key, value in movie.items():
                print(" {} = {}".format(key, value))
            print("\n")
            movie_price = float(movie['Price'])
            if movie_price < price:
                price = movie_price

        return price
        
if __name__ == '__main__':
    try:
        movie_comparer = MovieComparer()

        while True:
            # Pick a movie from index
            movie_picked = input("Pick a movie by index (0 for exit): ")

            try:
                pick = int(movie_picked)
            except ValueError:
                print("Please provide valid index")
                continue

            if pick == 0:
                exit()
            price = movie_comparer.get_cheapest(pick)
            if price is not None:
                print("***Cheapest Price: {}\n".format(price))

    except Exception as e:
        print("An error occured, error = {}".format(e))
