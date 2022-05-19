FROM python:3.8

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

EXPOSE 5000

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]