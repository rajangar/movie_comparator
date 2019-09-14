FROM python:3.7

COPY . /

RUN pip install requests

RUN pip install python-dotenv

CMD ["python", "test.py"]
