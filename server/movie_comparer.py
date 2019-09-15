import json
import os
import requests
from collections import defaultdict
from multiprocessing import Pool
import sys
import time
from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__)

class MovieComparer:
    """ To provide apis results and price comparison from 2 Databases
    """
    def __init__(self):
        """ Show movie list by fetching 2 databases parallely
        """
        load_dotenv()
        self.api_url_base = os.getenv('API_URL_BASE')
        self.token = os.getenv('API_TOKEN')
        self.title_map = defaultdict(list)

    def get_all_movies(self):
        """ Find dictionary of movies
        """
        cinemaworld_movies, filmworld_movies = self.get_movies()

        if cinemaworld_movies is not None:
            self.get_title_map(cinemaworld_movies, "cinemaworld")
        if filmworld_movies is not None:
            self.get_title_map(filmworld_movies, "filmworld")

        return self.title_map

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
            response = requests.get(api_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout as e:
            print(e)
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            return None

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

        movie_data = self.get_dict_from_apis(api_url)
        if movie_data is not None:
            movie_data['world'] = world

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

    def  get_title_map(self, world_movies, world):
        """ Returning title map as title as key and movie info as value
        """
        title_gen = self.titles_generator(world_movies, world)
        for movie in title_gen:
            self.title_map[movie['Title'].strip().lower()].append(movie)

    def get_cheapest_price(self, movie_title):
        """ Provide the cheapest price by comparing from multiple databases
        """
        self.get_all_movies()
        movie_list = self.title_map.get(movie_title.strip().lower(), [])

        if movie_list is None:
            return None

        pick_list = []
        for movie_info in movie_list:
            try:
                movie_id =  movie_info['ID']
                movie_world = movie_info['world']
            except KeyError as e:
                print("Price is not available for {}".format(movie_title))
                continue
            pick_list.append({'id': movie_id, 'world': movie_world})

        if pick_list is None:
            return None

        pool = Pool(2)
        movies_list = pool.map(self.get_movie_from_id, pick_list)
        pool.close()
        pool.join()

        # Set price as maximum float value in start to find minimum value
        price = sys.float_info.max
        print("\nMovie info from different worlds:\n")
        for movie in movies_list:
            if movie is None:
                continue
            print("[{}]".format(movie['world']))
            for key, value in movie.items():
                print(" {} = {}".format(key, value))
            print("\n")
            try:
                movie_price = float(movie['Price'])
            except KeyError as e:
                print("Price is not available for {}".format(movie_title))
                continue
            if movie_price < price:
                price = movie_price

        if price == sys.float_info.max:
            return None

        return str(price)

@app.route('/')
def get_all_available_movies():
    """ GET method to provide available movies list
    """
    movies_list = MovieComparer().get_all_movies()
    return json.dumps(movies_list, sort_keys=True)

@app.route('/cheapestprice')
def get_chepest_price_from_title():
    """ GET method to provide cheapest price from movie name
    """
    movie_title = request.args.get('title', type=str)

    price = MovieComparer().get_cheapest_price(movie_title)

    if price is None:
        return json.dumps({"Message": "Movie: {} not found in Database".format(movie_title)})

    return json.dumps({"Cheapest Price": price})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
