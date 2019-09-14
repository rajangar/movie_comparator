# movie_comparer

Compare the prices from 2 movie Databases and provide the cheapest price

-   Provide .env file with following variables:

        API_TOKEN="<X-Access-Token>"
        API_URL_BASE="https://webjetapitest.azurewebsites.net"

-   To run it with Docker:

        docker build -t moviecomparer:1.0 .
        docker run -ti --name comparer moviecomparer:1.0

    It will run the test cases written in test.py with unittest

-   To run it with movie_comparer.py directly on python 3.7:

        pip install requests
        pip install python-dotenv
        python movie_comparer.py

    It will show the unique movie names in a list, choose the movie you want to compare the price

-   Used multiprocessing to call the APIs for different databases parallely

-   Used exponential backoff, if timeout occurs while retrieving result from a query
