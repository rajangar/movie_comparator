# movie_comparer

Compare the prices from 2 movie Databases and provide the cheapest price

Run Server with Docker:

-   Provide .env file in server folder with following variables:

        API_TOKEN="<X-Access-Token>"
        API_URL_BASE="https://webjetapitest.azurewebsites.net"

-   To run it with Docker:

        cd server
        docker build -t movieserver:1.0 .
        docker run -d -p 80:80 movieserver:1.0


Run client with Docker:

-   Provide .env file in client folder with following variables:

        API_URL_BASE="http://<Server IP or Domain Name>"

-   To run it with Docker:

        cd client
        docker build -t movieclient:1.0 .
        docker run -ti --name movie_client movieclient:1.0

-   To run test cases on client:

        cd client
    
        -   With Docker:
                In Dockerfile, change
                CMD ["python", "movie_client.py"]
                as
                CMD ["python", "test.py"]
                Then run docker build and run as previous

        -   Without Docker:
                pip install -r requirements.txt
		        python test.py

-   Used multiprocessing to call the APIs for different databases parallely

-   Used exponential backoff on client, if timeout occurs while retrieving result from a query
