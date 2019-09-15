import json
import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()
api_url_base = os.getenv('API_URL_BASE')

def get_response_from_apis(api_url):
    """ Actual REST Api calling
    """
    try:
        response = requests.get(api_url)
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

def get_response(api_url):
    """ Use Exponential backoff, if there is an error happen while retrieving
    """
    exp_secs = 1
    while True:
        res = get_response_from_apis(api_url)
        if res is None:
            print("Error in fetching movies list")
            print("Trying again in {} seconds".format(exp_secs))
            time.sleep(exp_secs)
            exp_secs *= 2
        else:
            break

    return res

def show_all_movies():
    """ Printing all movies list by getting response from server
    """
    movies_map = get_response(api_url_base)

    title_list = sorted(list(movies_map.keys()))

    print("\nAll Movies List:\n----------------------------\n")
    for index, title in enumerate(title_list):
        movie = movies_map[title][0]
        print(" Index: {0}\n Title: {1}\n Year: {2}\n Type: {3}\n Poster: {4}"
            .format(index + 1, movie['Title'], movie['Year'], movie['Type'], movie['Poster']))
        print("\n-------------------------------------------------------------\n")

def find_cheapest_price(title):
    """ Return cheapest price by calling rest api
    """
    api_url = api_url_base + "/cheapestprice?title={}".format(urllib.parse.quote(title))

    ret_dict = get_response(api_url)

    if "Cheapest Price" in ret_dict.keys():
        return ret_dict['Cheapest Price']
    else:
        return None

if __name__ == '__main__':
    try:
        while True:
            print("Choose one option:\n--------------")
            print("1. All movies list")
            print("2. Find the cheapest price of a movie")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == '0':
                break
            elif choice == '1':
                show_all_movies()
            elif choice == '2':
                title = input("Movie name: ")
                price = find_cheapest_price(title)

                if price is not None:
                    print("\nCheapest Price: {}\n".format(price))
                else:
                    print("\nMovie ({}) not found\n".format(title))
            else:
                print("Invalid option, try again")

    except Exception as e:
        print("An error occured, error = {}".format(e))
