FROM python:3.10

WORKDIR /app

COPY requirements.txt ./requirements.txt


ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt update

RUN apt install ffmpeg -y

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

#ENTRYPOINT ["./docker-entrypoint.sh"]
