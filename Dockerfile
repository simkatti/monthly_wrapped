FROM python:3.12

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get -y install curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN poetry config virtualenvs.create false 
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000 8501

CMD ["poetry", "run", "poe", "dev"]

