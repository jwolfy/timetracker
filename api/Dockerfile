FROM python:3.9.6-slim-buster

ENV PROJECT_PIPENV_VERSION=2021.5.29

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir "pipenv==$PROJECT_PIPENV_VERSION" && \
    pipenv install --system --deploy --ignore-pipfile --keep-outdated --clear && \
    pip uninstall pipenv -y && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY ./ ./

ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0", "--port=5000"]
