FROM surnet/alpine-python-wkhtmltopdf:3.9.9-0.12.6-small

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk add zip
RUN pip install -r requirements.txt

COPY . /app

USER nobody

ENTRYPOINT [ "python" ]

CMD ["app.py" ]