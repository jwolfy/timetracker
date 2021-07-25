FROM python:3.9-alpine3.14

ENV PROJECT_PIPENV_VERSION=2021.5.29

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache --virtual .build-deps gcc g++ && \
    pip install --upgrade pip && \
    pip install --no-cache-dir "pipenv==$PROJECT_PIPENV_VERSION" && \
    pipenv install --system --deploy --ignore-pipfile --keep-outdated --clear && \
    pip uninstall pipenv -y && \
    apk --purge del .build-deps && \
    rm -rf /var/cache/apk/*

COPY ./ ./

EXPOSE 5000

ENTRYPOINT [ "flask" ]
CMD ["run", "--host=0.0.0.0", "--port=5000"]
