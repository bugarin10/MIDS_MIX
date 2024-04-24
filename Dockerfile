# Use an official Python runtime as a parent image
FROM python:3.9.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py", "--host=0.0.0.0","--port=5000"]